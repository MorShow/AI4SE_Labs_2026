import csv
import json
import sqlite3
import sys
from collections import defaultdict, deque
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
SOLUTION_DIR = TASK_DIR.parent
DATA_DIR = SOLUTION_DIR / "data"
sys.path.insert(0, str(SOLUTION_DIR))

from task2.evaluate_retrieval_predictions import load_database, row_multiset, unwrap_sql


def soft_scores(expected, predicted):
    """Paper's membership-based Precision, Recall, F1 for one result column."""
    if not expected and not predicted:
        return 1.0, 1.0, 1.0
    if not expected or not predicted:
        return 0.0, 0.0, 0.0
    expected_values = set(expected)
    predicted_values = set(predicted)
    precision = sum(value in expected_values for value in predicted) / len(predicted)
    recall = sum(value in predicted_values for value in expected) / len(expected)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def load_labels():
    csv.field_size_limit(1_000_000_000)
    with (DATA_DIR / "restaurants_dataset.csv").open(encoding="utf-8-sig", newline="") as source:
        return [(row["question"], [item[1] for item in json.loads(row["result"])])
                for row in csv.DictReader(source)]


def evaluate_file(path, labels, connection):
    expected_by_question = defaultdict(deque)
    for question, expected in labels:
        expected_by_question[question].append(expected)

    totals = [0.0, 0.0, 0.0]
    answered = exact = errors = 0
    with path.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            question = row["question"]
            if not expected_by_question[question]:
                raise ValueError(f"No matching label for {question!r} in {path}")
            expected = expected_by_question[question].popleft()
            try:
                cursor = connection.execute(unwrap_sql(row["predicted_sql"]))
                if cursor.description is None or len(cursor.description) != 1:
                    raise ValueError("Expected one result column")
                predicted_rows = cursor.fetchall()
                scores = soft_scores(expected, [value for (value,) in predicted_rows])
                exact += row_multiset(predicted_rows) == row_multiset((value,) for value in expected)
            except (sqlite3.Error, ValueError):
                scores = (0.0, 0.0, 0.0)
                errors += 1
            for index, score in enumerate(scores):
                totals[index] += score
            answered += 1
    if not answered:
        raise ValueError(f"No predictions in {path}")
    return {
        "name": path.stem.split("_", 1)[0], "file": path.name,
        "answered": answered, "exact": exact, "errors": errors,
        "precision": totals[0] / answered, "recall": totals[1] / answered,
        "f1": totals[2] / answered,
    }


def write_report(results, total_questions):
    lines = [
        "# Task 3 — Soft Execution F1",
        "",
        "## Metric",
        "",
        "We use the single-column version of [Soft Execution F1](https://arxiv.org/html/2506.13785v1#S2.SS1.SSS2). "
        "For each question, the predicted SQL runs against the same SQLite data as in Task 2. "
        "The reference is the restaurant-name column in the dataset result. "
        "Each predicted value contributes to Precision if it occurs anywhere in the reference column; "
        "each reference value contributes to Recall if it occurs anywhere in the predicted column. "
        "F1 is their harmonic mean.",
        "",
        "`Precision = matching predicted values / predicted values`  ",
        "`Recall = matching reference values / reference values`  ",
        "`F1 = 2 × Precision × Recall / (Precision + Recall)`",
        "",
        "Both empty results receive 1 for all three scores; one empty result receives 0. "
        "SQL errors and outputs with other than one column receive 0. These are explicit conventions "
        "for this dataset because the paper does not specify empty-result handling. "
        "The reported values are averages over answered questions, not pooled counts across all rows. "
        "Thus the displayed F1 is not necessarily the harmonic mean of the displayed Precision and Recall.",
        "",
        "## Comparison",
        "",
        "| Prompt | Precision | Recall | F1 | Exact accuracy | Answered | SQL/shape errors | Prediction CSV |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f'| {result["name"]} | {result["precision"]:.1%} | {result["recall"]:.1%} '
            f'| {result["f1"]:.1%} | {result["exact"] / result["answered"]:.1%} '
            f'| {result["answered"]}/{total_questions} | {result["errors"]} '
            f'| `{result["file"]}` |'
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "F1 complements exact execution accuracy: accuracy requires the complete result to match, "
        "while F1 gives partial credit for retrieved names and penalizes irrelevant names. "
        "It does not replace accuracy because a high F1 can still hide missing or extra rows. "
        "The metric tests results on this database, not equivalence of SQL logic on all databases.",
        "",
        "The paper's membership test does not enforce duplicate counts: for example, `[A, A]` "
        "and `[A]` score 1 even though exact accuracy rejects them. This matters because restaurant "
        "names are not guaranteed unique. Row order is ignored.",
        "",
    ]
    output = TASK_DIR / "report.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def main():
    labels = load_labels()
    files = sorted((SOLUTION_DIR / "predictions").glob("*.csv"))
    if not files:
        raise ValueError("No prediction CSV files found")
    connection = load_database()
    try:
        connection.execute("PRAGMA query_only = ON")
        results = [evaluate_file(path, labels, connection) for path in files]
    finally:
        connection.close()
    print(write_report(results, len(labels)))


if __name__ == "__main__":
    main()
