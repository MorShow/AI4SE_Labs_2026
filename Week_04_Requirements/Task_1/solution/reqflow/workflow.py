import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from .config import Settings
from .llm import OpenAIClient
from .renderer import render_markdown, write_markdown
from .schemas import Candidate, OverallPriorities, Extraction, PriorityAssessment, RequirementSet, Review, SourceChunk
from .validation import gate_review, validate_priorities, validate_set

LOG = logging.getLogger(__name__)
PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                               default=lambda record: record.model_dump(mode="json")), encoding="utf-8")


class WorkflowState(TypedDict):
    sources: list[SourceChunk]
    candidates: list[Candidate]
    draft: RequirementSet | None
    review: Review | None
    overall_priorities: OverallPriorities | None
    round: int
    status: str
    final_path: str | None


def initial_state(sources: list[SourceChunk], approved: RequirementSet | None = None) -> WorkflowState:
    review = None
    if approved is not None:
        errors = validate_set(approved, sources)
        if errors:
            raise ValueError("Cannot resume approved requirements: " + "; ".join(item.message for item in errors))
        # Final reviewer priorities were already stored on the approved requirements.
        review = Review(approved=True, checks=[], issues=[], priority_assessments=[
            PriorityAssessment(requirement_id=req.id, business_priority=req.business_priority,
                               rationale=req.priority_reason) for req in approved.requirements
        ])
    return {
        "sources": sources, "candidates": [], "draft": approved, "review": review,
        "overall_priorities": None, "round": 0, "status": "approved" if approved is not None else "running", "final_path": None,
    }


def source_payload(source: SourceChunk) -> dict[str, Any]:
    return {**source.model_dump(exclude={"text"}), "text": source.numbered_text()}


def build_graph(
    client: OpenAIClient, settings: Settings, corpus: Path, output: Path, output_dir: Path,
):
    common = (PROMPTS / "output_specs.md").read_text(encoding="utf-8")
    prompts = {
        role: common + "\n\n" + (PROMPTS / f"{role}.md").read_text(encoding="utf-8")
        for role in settings.models()
    }

    def extract(state: WorkflowState) -> dict[str, Any]:
        candidates: list[Candidate] = []
        by_document: dict[str, list[SourceChunk]] = {}
        for source in state["sources"]:
            by_document.setdefault(source.document, []).append(source)
        for document, chunks in by_document.items():
            path = output_dir / "candidates" / (document + ".json")
            fingerprint = hashlib.sha256(json.dumps({
                "model": settings.extractor_model, "prompt": prompts["extractor"],
                "sources": [source.model_dump() for source in chunks],
                "schema": Extraction.model_json_schema(), "max_output_tokens": 8_000,
            }, sort_keys=True).encode()).hexdigest()
            cached = json.loads(path.read_text(encoding="utf-8")) if settings.use_cache and path.exists() else {}
            if cached.get("fingerprint") == fingerprint:
                LOG.info("Reusing candidates for %s", document)
                candidates.extend(Candidate.model_validate(item) for item in cached["candidates"])
                continue
            extracted: list[Candidate] = []
            empty_chunks = []
            for source in chunks:
                LOG.info("Extracting %s (lines %s-%s)", document, source.start_line, source.end_line)
                result = client.generate(
                    "extractor", settings.extractor_model, prompts["extractor"],
                    {"source": source_payload(source)}, Extraction, max_output_tokens=8_000,
                )
                extracted.extend(
                    Candidate(id=f"C-{source.id}-{number:03d}", **item.model_dump())
                    for number, item in enumerate(result.candidates, 1)
                )
                if not result.candidates:
                    empty_chunks.append({"source_id": source.id, "reason": result.no_requirements_reason})
            write_json(path, {"document": document, "fingerprint": fingerprint,
                              "candidates": extracted, "empty_chunks": empty_chunks})
            candidates.extend(extracted)
        # The folder should represent this corpus, including when documents were removed.
        expected = {output_dir / "candidates" / (document + ".json") for document in by_document}
        for path in (output_dir / "candidates").rglob("*.json"):
            if path not in expected:
                path.unlink()
        write_json(output_dir / "candidates.json", candidates)
        if not candidates:
            raise ValueError("Extractor found no candidate requirements; see per-document extraction records.")
        return {"candidates": candidates}

    def consolidate(state: WorkflowState) -> dict[str, Any]:
        iteration = state["round"] + 1
        previous = state["draft"]
        review = state["review"]
        result = client.generate(
            "consolidator", settings.consolidator_model, prompts["consolidator"],
            {
                "sources": [source_payload(source) for source in state["sources"]],
                "candidates": [candidate.model_dump() for candidate in state["candidates"]],
                "previous_set": previous.model_dump() if previous else None,
                "feedback": [item.model_dump() for item in review.issues] if review else [],
            }, RequirementSet, max_output_tokens=24_000,
        )
        return {"draft": result, "round": iteration, "status": "reviewing", "review": None}

    def review_requirements(state: WorkflowState) -> dict[str, Any]:
        draft = state["draft"]
        if draft is None:
            raise ValueError("Reviewer requires a requirement set.")
        structural = validate_set(draft, state["sources"])
        raw = client.generate(
            "reviewer", settings.reviewer_model, prompts["reviewer"],
            {
                "sources": [source_payload(source) for source in state["sources"]],
                "requirement_set": draft.model_dump(),
                "structural_errors": [item.model_dump() for item in structural],
            }, Review, max_output_tokens=8_000,
        )
        result = gate_review(raw, draft, structural)
        status = "approved" if result.approved else (
            "needs_revision" if state["round"] <= settings.max_revisions else "review_failed"
        )
        if result.approved:
            draft = draft.model_copy(update={"requirements": [
                req.model_copy(update={
                    "business_priority": assessment.business_priority,
                    "priority_reason": assessment.rationale,
                }) for req, assessment in zip(draft.requirements, result.priority_assessments)
            ]})
            write_json(output_dir / "approved-requirements.json", draft)
        LOG.info("Review round %s: %s (%s issues)", state["round"], status, len(result.issues))
        for item in result.issues:
            LOG.info("%s %s: %s", item.severity, item.spec, item.message)
        return {"draft": draft, "review": result, "status": status}

    def after_review(state: WorkflowState) -> Literal["consolidator", "architect", "stop"]:
        if state["status"] == "approved":
            return "architect"
        return "consolidator" if state["status"] == "needs_revision" else "stop"

    def architect(state: WorkflowState) -> dict[str, Any]:
        draft, review = state["draft"], state["review"]
        if draft is None or review is None or not review.approved:
            raise ValueError("Architect can only receive an approved requirement set.")
        errors: list[str] = []
        priorities: OverallPriorities | None = None
        for attempt in range(2):
            priorities = client.generate(
                "architect", settings.architect_model, prompts["architect"],
                {
                    "approved_requirements": [req.model_dump() for req in draft.requirements],
                    "priority_assessments": [item.model_dump() for item in review.priority_assessments],
                    "previous_assessments": priorities.model_dump() if priorities is not None else None,
                    "validation_errors": errors,
                }, OverallPriorities, max_output_tokens=12_000,
            )
            errors = validate_priorities(priorities, draft)
            if not errors:
                return {"overall_priorities": priorities}
            LOG.warning("Architect attempt %s: %s", attempt + 1, "; ".join(errors))
        raise ValueError("Architect priority assessments have invalid or missing IDs: " + "; ".join(errors))

    def render(state: WorkflowState) -> dict[str, Any]:
        draft, review, priorities = state["draft"], state["review"], state["overall_priorities"]
        if draft is None or review is None or priorities is None or not review.approved:
            raise ValueError("Rendering requires approved requirements, review and overall priorities.")
        content = render_markdown(draft, review, priorities, state["sources"], corpus, output)
        write_markdown(output, content)
        return {"status": "complete", "final_path": str(output)}

    graph = StateGraph(WorkflowState)
    graph.add_node("extractor", extract)
    graph.add_node("consolidator", consolidate)
    graph.add_node("reviewer", review_requirements)
    graph.add_node("architect", architect)
    graph.add_node("render_markdown", render)
    graph.add_conditional_edges(START, lambda state: "architect" if state["status"] == "approved" else "extractor",
                                {"architect": "architect", "extractor": "extractor"})
    graph.add_edge("extractor", "consolidator")
    graph.add_edge("consolidator", "reviewer")
    graph.add_conditional_edges("reviewer", after_review, {
        "consolidator": "consolidator", "architect": "architect", "stop": END,
    })
    graph.add_edge("architect", "render_markdown")
    graph.add_edge("render_markdown", END)
    return graph.compile()
