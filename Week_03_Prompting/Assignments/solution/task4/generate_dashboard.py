import argparse
import csv
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
SOLUTION_DIR = TASK_DIR.parent
sys.path.insert(0, str(SOLUTION_DIR))

from task3.generate_dashboard import (  # noqa: E402
    evaluate_csv,
    prediction_files,
)


COLORS = ["#52d6be", "#f5ad63", "#9ea8ff", "#f17e9a", "#74baff", "#d4bc72"]


def load_questions():
    csv.field_size_limit(1_000_000_000)
    path = SOLUTION_DIR / "data" / "restaurants_dataset.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    questions = [
        {"text": row["question"], "gold": json.loads(row["result"])}
        for row in rows
    ]
    labels = [
        (question["text"], [(item[1],) for item in question["gold"]])
        for question in questions
    ]
    return questions, labels


def mean(answers, index):
    return sum(answer[index] for answer in answers.values()) / len(answers) if answers else None


def build_data(files):
    questions, labels = load_questions()
    for question in questions:
        question["runs"] = []

    database = SOLUTION_DIR / "data" / "restaurants_ready.sqlite"
    connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    names = Counter()
    configs = []
    try:
        connection.execute("PRAGMA query_only = ON")
        for path in files:
            answers = evaluate_csv(path, labels, connection)
            base_name = path.stem.split("_", 1)[0]
            names[base_name] += 1
            name = base_name if names[base_name] == 1 else f"{base_name} #{names[base_name]}"
            times = [answer[2] for answer in answers.values() if answer[2] is not None]
            configs.append({
                "name": name,
                "file": path.name,
                "color": COLORS[(len(configs)) % len(COLORS)],
                "answered": len(answers),
                "correct": sum(answer[0] for answer in answers.values()),
                "accuracy": mean(answers, 0),
                "precision": mean(answers, 3),
                "recall": mean(answers, 4),
                "f1": mean(answers, 5),
                "jaccard": mean(answers, 6),
                "latency": sum(times) / len(times) if times else None,
            })
            for index, question in enumerate(questions):
                answer = answers.get(index)
                question["runs"].append(
                    {"correct": answer[0], "latency": answer[2]} if answer else None
                )
    finally:
        connection.close()
    return {"questions": questions, "configs": configs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--predictions", nargs="+", type=Path,
        help="Prediction CSV files; defaults to all CSV files in solution/predictions",
    )
    parser.add_argument("--output", type=Path, default=TASK_DIR / "report.html")
    args = parser.parse_args()

    files = args.predictions or prediction_files(SOLUTION_DIR / "predictions")
    if not files:
        parser.error("No prediction CSV files selected")
    data = build_data(files)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = (TASK_DIR / "template.html").read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(template.replace("__DASHBOARD_DATA__", payload), encoding="utf-8")
    file_word = "file" if len(files) == 1 else "files"
    print(f"Report: {args.output} ({len(files)} prediction CSV {file_word}, {len(data['questions'])} questions)")
    for config in data["configs"]:
        print(
            f"{config['name']}: accuracy={config['accuracy']:.1%}, "
            f"F1={config['f1']:.1%}, latency={config['latency']:.2f}s"
        )


if __name__ == "__main__":
    main()
