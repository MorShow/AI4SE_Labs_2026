import argparse
import logging
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from reqflow.config import Settings
from reqflow.corpus import load_corpus
from reqflow.llm import OpenAIClient
from reqflow.schemas import RequirementSet
from reqflow.workflow import build_graph, initial_state, write_json


def parse_args() -> argparse.Namespace:
    defaults = Settings()
    parser = argparse.ArgumentParser(description="Refine a text corpus into source-grounded requirements using LangGraph.")
    parser.add_argument("--input-dir", required=True, type=Path, help="Recursively read UTF-8 .txt and textual .eml files.")
    parser.add_argument("--output", type=Path, help="Explicit output file; otherwise create a separate run directory.")
    parser.add_argument("--approved-requirements", type=Path, help="Resume at Architect using a saved approved-requirements.json.")
    parser.add_argument("--inspect", action="store_true", help="Inspect sources and configuration without an API key or LLM calls.")
    parser.add_argument("--extractor-model", default=defaults.extractor_model)
    parser.add_argument("--consolidator-model", default=defaults.consolidator_model)
    parser.add_argument("--reviewer-model", default=defaults.reviewer_model)
    parser.add_argument("--architect-model", default=defaults.architect_model)
    parser.add_argument("--max-revisions", type=int, default=defaults.max_revisions, help="Maximum returns from Reviewer to Consolidator.")
    parser.add_argument("--chunk-chars", type=int, default=defaults.chunk_chars)
    parser.add_argument("--max-input-chars", type=int, default=defaults.max_input_chars, help="Approximate per-call input guard, not a token guarantee.")
    parser.add_argument("--no-cache", action="store_true", help="Disable persistent extraction cache.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    failure: Path | None = None
    try:
        if not args.inspect:
            print("OpenAI credit balance: unavailable via a standard API key. "
                  "Check https://platform.openai.com/settings/organization/billing/overview", flush=True)
        settings = Settings(
            extractor_model=args.extractor_model, consolidator_model=args.consolidator_model,
            reviewer_model=args.reviewer_model, architect_model=args.architect_model,
            max_revisions=args.max_revisions, chunk_chars=args.chunk_chars,
            max_input_chars=args.max_input_chars, use_cache=not args.no_cache,
        )
        corpus = args.input_dir.resolve(strict=True)
        output_root = Path(__file__).resolve().parent / "output"
        if args.output is None:
            run_name = datetime.now(timezone.utc).strftime("run-%Y%m%d-%H%M%S-%f")
            output = output_root / run_name / "final-requirements.md"
        else:
            output = args.output.resolve()
        if output.suffix.lower() != ".md":
            raise ValueError("--output must end in .md.")
        if output.parent.is_relative_to(corpus):
            raise ValueError("Keep output outside the input corpus.")
        sources = load_corpus(corpus, settings.chunk_chars)
        print(f"Documents: {len({source.document for source in sources})}; chunks: {len(sources)}")
        print(f"Models: {settings.models()}")
        if args.inspect:
            for document in sorted({source.document for source in sources}):
                print(f"  {document}")
            return 0
        failure = output.parent / "failure.json"
        failure.unlink(missing_ok=True)
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("Set OPENAI_API_KEY in your environment, or use --inspect without API calls.")
        state = initial_state(sources, RequirementSet.model_validate_json(
            args.approved_requirements.read_text(encoding="utf-8")
        ) if args.approved_requirements else None)
        if args.approved_requirements:
            print(f"Resuming at Architect from: {args.approved_requirements.resolve()}", flush=True)
            write_json(output.parent / "approved-requirements.json", state["draft"])
        elif args.output is None and settings.use_cache:
            previous = sorted(output_root.glob("run-*/candidates"))
            if previous:
                shutil.copytree(previous[-1], output.parent / "candidates")
        print(f"Results: {output.parent}", flush=True)
        client = OpenAIClient(settings.max_input_chars)
        graph = build_graph(client, settings, corpus, output, output.parent)
        result = graph.invoke(state, {"recursion_limit": 12 + 2 * settings.max_revisions})
        if result["status"] != "complete":
            write_json(failure, {
                "type": "ReviewRejected", "issues": result["review"].issues,
                "checks": result["review"].checks, "requirement_set": result["draft"],
            })
            print(f"Review was not approved; see {failure}.", file=sys.stderr)
            return 2
        print(f"Requirements written to {result['final_path']}")
        return 0
    except Exception as error:
        if failure is not None:
            write_json(failure, {"type": type(error).__name__, "message": str(error)})
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
