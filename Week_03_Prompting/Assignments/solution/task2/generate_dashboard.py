import argparse
import csv
import html
import json
import math
import sqlite3
import sys
from collections import defaultdict, deque
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
SOLUTION_DIR = TASK_DIR.parent
sys.path.insert(0, str(SOLUTION_DIR))

from task2.evaluate_retrieval_predictions import LABELS_PATH, load_database, row_multiset, unwrap_sql



def load_labels():
    csv.field_size_limit(1_000_000_000)
    with LABELS_PATH.open(encoding="utf-8-sig", newline="") as source:
        return [
            (row["question"], [(item[1],) for item in json.loads(row["result"])])
            for row in csv.DictReader(source)
        ]


def evaluate_csv(path, labels, connection):
    positions = defaultdict(deque)
    for index, (question, _expected) in enumerate(labels):
        positions[question].append(index)
    answers = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            question = row["question"]
            if not positions[question]:
                raise ValueError(f"No matching label for {question!r} in {path}")
            index = positions[question].popleft()
            sql = unwrap_sql(row["predicted_sql"])
            try:
                cursor = connection.execute(sql)
                if cursor.description is None:
                    raise ValueError("SQL returned no columns")
                correct = row_multiset(cursor.fetchall()) == row_multiset(labels[index][1])
            except (sqlite3.Error, ValueError):
                correct = False
            raw_time = row.get("total_time")
            elapsed = float(raw_time) if raw_time else None
            if elapsed is not None and (not math.isfinite(elapsed) or elapsed < 0):
                raise ValueError(f"Invalid total_time for {question!r} in {path}")
            answers[index] = (correct, sql, elapsed)
    return answers


def prediction_files(directory):
    files = []
    for path in sorted(directory.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as source:
            fields = csv.DictReader(source).fieldnames or []
        if {"question", "predicted_sql"} <= set(fields):
            files.append(path)
    return files


def make_html(labels, results):
    escape = html.escape
    total = len(labels)
    parts = ["""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Text2SQL — Report</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#1d313b;background:#f3f7f8}
body{max-width:1200px;margin:auto;padding:32px 20px 60px}h1{font-size:1.9rem;margin:0 0 4px}
h2{font-size:1.15rem;margin:32px 0 12px}.muted{color:#61737c}.lead{margin:0 0 26px}
.card{background:white;border:1px solid #dce6e9;border-radius:12px;padding:18px;box-shadow:0 2px 10px #16303b09}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%}th,td{padding:10px 12px;border-bottom:1px solid #e8eef0;text-align:left}
th{color:#53656e;font-size:.85rem;white-space:nowrap}tbody tr:last-child td{border-bottom:0}
.number{text-align:center;font-variant-numeric:tabular-nums}.question{min-width:300px}.yes{color:#12835c;font-weight:800}
.no{color:#c34c53;font-weight:800}.missing{color:#9ba9af}.map{margin:0;padding-left:24px;line-height:1.9}
.map li{overflow-wrap:anywhere}.tag{display:inline-block;background:#e4f2f0;color:#15645f;border-radius:6px;padding:1px 7px;font-weight:650}
.pager{display:flex;align-items:center;justify-content:flex-end;gap:12px;margin-top:14px}
button{border:1px solid #c7d7dc;background:white;border-radius:8px;padding:6px 12px;font-size:1rem;cursor:pointer}
button:disabled{opacity:.4;cursor:default}button:focus-visible{outline:2px solid #16817b;outline-offset:2px}
.answer-button{border:0;background:none;color:inherit;font-size:1.2rem;font-weight:800;padding:2px 8px}
.answer-button:hover{text-decoration:underline}dialog{width:min(720px,calc(100% - 40px));border:1px solid #c7d7dc;border-radius:12px;padding:24px;box-shadow:0 18px 60px #16303b33;color:#1d313b}
dialog::backdrop{background:#102b3a88}.dialog-label{font-weight:700;margin:18px 0 6px}#modal-question{margin:0}
#modal-sql{background:#f3f7f8;border-radius:8px;padding:14px;white-space:pre-wrap;overflow-wrap:anywhere;max-height:50vh;overflow:auto}
.dialog-actions{text-align:right}
.agreement-table{table-layout:fixed}.agreement-table tbody tr{height:72px}
.agreement-cell{font-variant-numeric:tabular-nums;background:#fafcfc}
.agreement-cell strong{display:block;font-size:1rem;margin-bottom:4px}.agreement-cell small{color:#61737c}
.agreement-cell .same{color:#147d56}.agreement-cell .different{color:#a85b23}
.agreement-cases{white-space:nowrap}
[hidden]{display:none!important}@media(max-width:650px){body{padding:20px 12px}.card{padding:12px}.question{min-width:240px}}
</style></head><body><h1>Text2SQL — Report</h1>"""]
    parts.append(f'<p class="lead muted">Questions: {total} · Configurations: {len(results)}. '
                 'Accuracy is calculated over the predictions present in each CSV.</p>')
    parts.append('<h2>Accuracy</h2><div class="card scroll"><table><thead><tr>'
                 '<th>No.</th><th>Prompt</th><th>Accuracy</th><th>Correct / answered</th>'
                 '<th>Coverage</th><th>Mean latency (s)</th>'
                 '</tr></thead><tbody>')
    for number, (path, answers) in enumerate(results, 1):
        correct = sum(answer[0] for answer in answers.values())
        accuracy = f"{correct / len(answers):.1%}" if answers else "—"
        times = [answer[2] for answer in answers.values() if answer[2] is not None]
        mean_latency = f"{sum(times) / len(times):.2f}" if times else "—"
        name = path.stem.split("_", 1)[0]
        parts.append(f'<tr><td class="number">{number}</td><td>{escape(name)}</td>'
                     f'<td>{accuracy}</td><td>{correct} / {len(answers)}</td>'
                     f'<td>{len(answers)} / {total}</td><td>{mean_latency}</td></tr>')
    parts.append('</tbody></table></div><h2>Correctness agreement</h2>'
                 '<p class="muted">Each cell compares the row prompt with the column prompt on questions answered by both. '
                 '✓✗ includes both directions of disagreement.</p>'
                 f'<div class="card scroll"><table class="agreement-table" style="min-width:{(len(results) + 1) * 220}px">'
                 '<thead><tr><th>Row / column</th>')
    for number, (path, _answers) in enumerate(results, 1):
        name = path.stem.split("_", 1)[0]
        parts.append(f'<th>{number} {escape(name)}</th>')
    parts.append('</tr></thead><tbody>')
    for row_number, (row_path, row_answers) in enumerate(results, 1):
        row_name = row_path.stem.split("_", 1)[0]
        parts.append(f'<tr><th>{row_number} {escape(row_name)}</th>')
        for col_number, (_col_path, col_answers) in enumerate(results, 1):
            if row_number >= col_number:
                parts.append('<td></td>')
                continue
            shared = row_answers.keys() & col_answers.keys()
            if not shared:
                parts.append('<td class="agreement-cell missing">—<br><small>No shared answers</small></td>')
                continue
            both_correct = sum(row_answers[i][0] and col_answers[i][0] for i in shared)
            both_wrong = sum(not row_answers[i][0] and not col_answers[i][0] for i in shared)
            different = len(shared) - both_correct - both_wrong
            agreement = (both_correct + both_wrong) / len(shared)
            parts.append(f'<td class="agreement-cell"><strong>{agreement:.1%} <small>({len(shared)} shared)</small></strong>'
                         f'<div class="agreement-cases"><span class="same">✓✓ {both_correct} · ✗✗ {both_wrong}</span>'
                         f' · <span class="different">✓✗ {different}</span></div></td>')
        parts.append('</tr>')
    parts.append('</tbody></table></div><h2>Configuration mapping</h2><div class="card"><ol class="map">')
    for path, _answers in results:
        name = path.stem.split("_", 1)[0]
        parts.append(f'<li><span class="tag">{escape(name)}</span> — {escape(path.name)}</li>')
    parts.append('</ol></div><h2>Results by question</h2><div class="card"><div class="scroll"><table>'
                 '<thead><tr><th class="question">question</th>')
    for path, _answers in results:
        name = path.stem.split("_", 1)[0]
        parts.append(f'<th class="number" title="{escape(path.name, quote=True)}">{escape(name)}</th>')
    parts.append('</tr></thead><tbody id="questions">')
    for index, (question, _expected) in enumerate(labels):
        parts.append(f'<tr><td class="question">{escape(question)}</td>')
        for _path, answers in results:
            if index not in answers:
                parts.append('<td class="number missing" title="No prediction">—</td>')
            else:
                correct, sql, _elapsed = answers[index]
                status = "Correct" if correct else "Incorrect"
                icon = "✓" if correct else "✗"
                style = "yes" if correct else "no"
                parts.append(f'<td class="number {style}"><button class="answer-button" '
                             f'type="button" aria-label="{status}: show SQL answer" '
                             f'title="Show SQL answer">{icon}</button>'
                             f'<pre class="sql-source" hidden>{escape(sql)}</pre></td>')
        parts.append('</tr>')
    parts.append('''</tbody></table></div><div class="pager">
<button id="prev" type="button" aria-label="Previous 10 questions">←</button>
<span id="page" aria-live="polite"></span>
<button id="next" type="button" aria-label="Next 10 questions">→</button>
</div></div><p class="muted">✓ — correct · ✗ — incorrect · — — no prediction in CSV</p>
<dialog id="answer-dialog" aria-label="SQL answer">
<p class="dialog-label">Question:</p><p id="modal-question"></p>
<p class="dialog-label">SQL answer:</p><pre id="modal-sql"></pre>
<form method="dialog" class="dialog-actions"><button type="submit">Close</button></form>
</dialog>
<script>
const rows = [...document.querySelectorAll('#questions tr')];
const pages = Math.max(1, Math.ceil(rows.length / 10));
let current = 0;
function show() {
  rows.forEach((row, index) => { row.hidden = Math.floor(index / 10) !== current; });
  document.getElementById('page').textContent = `${current + 1} / ${pages}`;
  document.getElementById('prev').disabled = current === 0;
  document.getElementById('next').disabled = current === pages - 1;
}
document.getElementById('prev').addEventListener('click', () => { current--; show(); });
document.getElementById('next').addEventListener('click', () => { current++; show(); });
document.getElementById('questions').addEventListener('click', (event) => {
  const button = event.target.closest('.answer-button');
  if (!button) return;
  document.getElementById('modal-question').textContent = button.closest('tr').querySelector('.question').textContent;
  document.getElementById('modal-sql').textContent = button.closest('td').querySelector('.sql-source').textContent;
  document.getElementById('answer-dialog').showModal();
});
show();
</script></body></html>''')
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-dir", type=Path, default=SOLUTION_DIR / "predictions")
    parser.add_argument("--output", type=Path, default=TASK_DIR / "report.html")
    args = parser.parse_args()

    labels = load_labels()
    files = prediction_files(args.predictions_dir)
    connection = load_database()
    try:
        connection.execute("PRAGMA query_only = ON")
        results = [(path, evaluate_csv(path, labels, connection)) for path in files]
    finally:
        connection.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(make_html(labels, results), encoding="utf-8")
    print(f"Report: {args.output} ({len(files)} prediction CSV files)")


if __name__ == "__main__":
    main()
