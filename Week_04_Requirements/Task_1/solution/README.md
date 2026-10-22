# Requirements refinement

Four LLM nodes: Extractor → Consolidator ⇄ Reviewer → Architect.
A deterministic node builds the final Markdown. Every agent receives the shared
[OS1–OS9 contract](./prompts/output_specs.md).

From this directory, using Python 3.11+ and an activated environment:

```powershell
python -m pip install -r requirements.txt
python main.py --input-dir ../data/corpus --inspect
$env:OPENAI_API_KEY = 'your-key'
python main.py --input-dir ../data/corpus
```

The key must be in the environment; `.env` is not loaded automatically.
The input directory is scanned recursively for UTF-8 `.txt` and textual `.eml` files.

Generated files:

```text
output/
  run-<UTC timestamp>/
    final-requirements.md
    candidates.json
    candidates/                 # one JSON per source document
    approved-requirements.json
    failure.json                # only if this attempt failed
```

The final Markdown contains all requirement categories, IDs, business priorities,
the Business and Overall Priority scales, both priorities and their rationales next
to each requirement, source links and blacklist. Architect combines business value
with a developer perspective to assign High/Medium/Low Overall Priority. There is
no execution sequence or dependency graph; assessment order has no meaning.
The architect only receives requirements already accepted by Reviewer.
Each default run has its own folder. It reuses matching candidates from the previous
run without modifying that run. No separate cache is created. Failures are explained
in `failure.json`. An explicit `--output path/to/file.md` writes to that exact path
instead of creating an automatic run folder.
If review fails, that run's `failure.json` includes the issues, checklist and last
rejected requirement set. Issues are also printed to the console.
Each issue has Critical, Medium or Low severity. Review returns to Consolidator
only for at least one Critical or three Medium issues, subject to --max-revisions.
Low issues and up to two Medium issues allow approval. Structural errors (such as
broken source references) are Critical. Routing uses these counts, not a separate
model veto or the checklist flags.

To resume an approved run directly at Architect, select its saved file explicitly:

```powershell
python main.py --input-dir ../data/corpus --approved-requirements output/run-<timestamp>/approved-requirements.json --architect-model gpt-5.4-nano
```

This skips Extractor, Consolidator and Reviewer and preserves the saved requirements
and final business priorities. Use the original corpus and chunk size for source links;
this mode trusts the saved approval and does not recheck source meaning or freshness.
The default output is a new run folder containing the approved set, final Markdown
on success, or failure.json on failure. Candidates remain in the original run folder.
Later rejected runs do not affect the selected approved file.

Options: `--output`, `--max-revisions` (default 2), `--chunk-chars` (14000),
`--max-input-chars` (400000), `--no-cache`, and `--<role>-model` for each LLM node.
Defaults: `gpt-4.1-nano` for extraction, `gpt-5-mini` for consolidation and architecture,
`gpt-4o-mini` for review. At least three distinct models are required.

[main.py](./main.py) starts the pipeline; [workflow.py](./reqflow/workflow.py) defines
the graph; [prompts/](./prompts) contains agent instructions.
The assignment's design explanation is in [report.md](./report.md).

Focused offline verification:

```powershell
python -m unittest discover -s tests -v
```

The checks cover severity thresholds, the feedback/output flow, failed review, paraphrased evidence
and complete overall-priority coverage. Real-model quality requires a run with an API key.
