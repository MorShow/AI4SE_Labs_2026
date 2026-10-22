import html
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import quote

from .schemas import OverallPriorities, Evidence, RequirementSet, Review, SourceChunk

SECTIONS = (
    ("FR", "Functional Requirements"),
    ("NFR", "Non-Functional Requirements"),
    ("IR", "Interface Requirements"),
    ("AR", "Additional Requirements (Operational, Legal and Deployment)"),
)


def md(value: str) -> str:
    value = html.escape(" ".join(value.split()), quote=False)
    return re.sub(r"([\\`*_\[\]|])", r"\\\1", value)


def requirement_link(req_id: str) -> str:
    return f"[{req_id}](#{req_id.lower()})"


def source_link(evidence: Evidence, sources: dict[str, SourceChunk], corpus: Path, output: Path) -> str:
    source = sources[evidence.source_id]
    path = (corpus / source.document).resolve(strict=True)
    if not path.is_relative_to(corpus.resolve()) or not path.is_file():
        raise ValueError(f"Invalid source document path: {source.document}")
    try:
        target = quote(Path(os.path.relpath(path, output.parent)).as_posix(), safe="/.-_~")
    except ValueError:  # Windows input/output on different drives.
        target = path.as_uri()
    return f"[{md(source.document)}]({target})"


def render_markdown(
    draft: RequirementSet, review: Review, priorities: OverallPriorities,
    sources: list[SourceChunk], corpus: Path, output: Path,
) -> str:
    source_map = {source.id: source for source in sources}
    overall = {item.requirement_id: item for item in priorities.items}
    assessments = {item.requirement_id: item for item in review.priority_assessments}
    lines = [f"# {md(draft.title)}", "", md(draft.scope), "", "## Priority Scale", "",
             "Business priority is shown next to every requirement:", "",
             "- **High:** essential/core operation, an explicit critical request, or a source-supported mandatory constraint.",
             "- **Medium:** important improvement with a viable workaround.",
             "- **Low:** optional convenience or enhancement.", "",
             "**Overall priority** combines business priority with the developer perspective on feasibility, complexity, technical risk and readiness:", "",
             "- **High:** warrants strong development focus given business value and technical impact.",
             "- **Medium:** worthwhile development work, with moderate overall urgency or readiness.",
             "- **Low:** optional or deferrable work with limited overall urgency.", "",
             "Priority levels do not prescribe an implementation sequence.", ""]
    for category, title in SECTIONS:
        lines.extend([f"## {title}", ""])
        selected = [req for req in draft.requirements if req.category == category]
        if not selected:
            lines.extend(["No source-supported requirements identified in this category.", ""])
        for req in selected:
            assessment = assessments[req.id]
            lines.extend([f'<a id="{req.id.lower()}"></a>', "",
                          f"### {req.id} — {md(req.name)}", "",
                          f"**Business priority:** {req.business_priority} · **Overall priority:** {overall[req.id].overall_priority}", ""])
            if req.additional_type:
                lines.extend([f"**Type:** {req.additional_type}", ""])
            lines.extend([md(req.description), "", f"**Business priority rationale:** {md(assessment.rationale)}", "",
                          f"**Overall priority rationale:** {md(overall[req.id].rationale)}", ""])
    lines.extend(["## Overall Priority List", "",
                  "| Requirement | Business priority | Overall priority | Developer rationale |",
                  "| --- | --- | --- | --- |"])
    for req in draft.requirements:
        item = overall[req.id]
        lines.append(f"| {requirement_link(req.id)} | {req.business_priority} | {item.overall_priority} | {md(item.rationale)} |")
    lines.extend(["", "## Traceability and Verification", "",
                  "References below point to supplied source documents. Semantic support is checked by Reviewer; related requirement links are supplementary.", "",
                  "| Requirement | Related requirements | Source documents |",
                  "| --- | --- | --- |"])
    for req in draft.requirements:
        related = ", ".join(requirement_link(req_id) for req_id in req.related_requirement_ids) or "—"
        links = dict.fromkeys(source_link(item, source_map, corpus, output) for item in req.evidence)
        lines.append(f"| {requirement_link(req.id)} | {related} | {'; '.join(links)} |")
    lines.extend(["", "## Blacklist", ""])
    if not draft.blacklist:
        lines.extend(["No identified requirements were discarded as conflicting or nonsensical.", ""])
    for item in draft.blacklist:
        links = dict.fromkeys(source_link(e, source_map, corpus, output) for e in item.evidence)
        lines.extend([f"### {item.id} — {md(item.name)}", "", md(item.description), "",
                      f"**Reason discarded:** {md(item.reason)}", "", f"**Sources:** {'; '.join(links)}", ""])
    if draft.decisions:
        lines.extend(["## Source Resolution Decisions", ""])
        lines.extend(f"- {md(decision)}" for decision in draft.decisions)
    return "\n".join(lines).rstrip() + "\n"


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
