import argparse
import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict, deque
from pathlib import Path


SOLUTION_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SOLUTION_DIR / "data"
LABELS_PATH = DATA_DIR / "restaurants_dataset.csv"
SCHEMA_PATH = DATA_DIR / "restaurants-schema.csv"
DATABASE_PATH = DATA_DIR / "restaurants-db.txt"


def sqlite_type(schema_type):
    normalized_type = schema_type.strip().lower()
    if normalized_type.startswith("int"):
        return "INTEGER"
    if normalized_type.startswith("decimal") or normalized_type.startswith("float"):
        return "REAL"
    return "TEXT"


def load_database():
    tables = {}
    with SCHEMA_PATH.open(encoding="utf-8", newline="") as schema_file:
        for table, field, primary_key, _foreign_key, column_type in csv.reader(
            schema_file, skipinitialspace=True
        ):
            table = table.strip()
            field = field.strip()
            if table == "-":
                continue
            tables.setdefault(table, []).append(
                (field, sqlite_type(column_type), primary_key.strip().lower() == "y")
            )

    connection = sqlite3.connect(":memory:")
    for table, columns in tables.items():
        definitions = []
        for field, column_type, primary_key in columns:
            definition = f'"{field}" {column_type}'
            if primary_key:
                definition += " PRIMARY KEY"
            definitions.append(definition)
        connection.execute(f'CREATE TABLE "{table}" ({", ".join(definitions)})')

    with DATABASE_PATH.open(encoding="utf-8") as database_file:
        for line_number, line in enumerate(database_file, start=1):
            match = re.fullmatch(r"([A-Z_]+)\((.*)\)", line.rstrip("\r\n"))
            if match is None:
                raise ValueError(f"Invalid database record on line {line_number}")

            table, values_text = match.groups()
            if table not in tables:
                raise ValueError(f"Unknown table {table!r} on line {line_number}")

            values = next(csv.reader([values_text], skipinitialspace=True))
            columns = tables[table]
            if len(values) != len(columns):
                raise ValueError(
                    f"Expected {len(columns)} values for {table} on line "
                    f"{line_number}, got {len(values)}"
                )

            converted_values = []
            for value, (_field, column_type, _primary_key) in zip(values, columns):
                if column_type == "INTEGER":
                    converted_values.append(int(value))
                elif column_type == "REAL":
                    converted_values.append(float(value))
                else:
                    converted_values.append(value)

            placeholders = ", ".join("?" for _ in columns)
            connection.execute(
                f'INSERT INTO "{table}" VALUES ({placeholders})', converted_values
            )

    return connection


def row_multiset(rows):
    return Counter(tuple(row) for row in rows)


def unwrap_sql(text):
    """Remove a complete Markdown SQL fence while keeping the raw CSV intact."""
    sql = text.strip()
    match = re.fullmatch(r"```(?:sql|sqlite)?[ \t]*\r?\n(.*?)\r?\n```", sql,
                         flags=re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else sql


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True,
                        help="CSV from generate_predictions.py")
    parser.add_argument("--labels", type=Path, default=LABELS_PATH,
                        help="Reference CSV with question and result columns")
    parser.add_argument("--details", type=Path,
                        help="Optional CSV with correctness and errors per question")
    args = parser.parse_args()
    csv.field_size_limit(1_000_000_000)
    labels_by_question = defaultdict(deque)
    with args.labels.open(encoding="utf-8-sig", newline="") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=2):
            try:
                result = json.loads(row["result"])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON label result on line {line_number} "
                    f"of {args.labels}"
                ) from error
            if not isinstance(result, list):
                raise ValueError(
                    f"Expected a JSON array label result on line {line_number} "
                    f"of {args.labels}"
                )
            if any(not isinstance(item, list) or len(item) != 2 for item in result):
                raise ValueError(f"Expected [ID, name] rows on line {line_number}")
            labels_by_question[row["question"]].append([(item[1],) for item in result])

    connection = load_database()
    try:
        total = 0
        correct = 0
        errors = 0
        details = []
        with args.predictions.open(encoding="utf-8-sig", newline="") as source:
            for line_number, row in enumerate(csv.DictReader(source), start=2):
                question = row["question"]
                if not labels_by_question[question]:
                    raise ValueError(
                        f"No matching label question for prediction on line "
                        f"{line_number}: {question!r}"
                    )

                expected_rows = labels_by_question[question].popleft()
                predicted_rows = None
                error_message = ""
                try:
                    cursor = connection.execute(unwrap_sql(row["predicted_sql"]))
                    if cursor.description is None:
                        raise ValueError("SQL did not return rows")
                    predicted_rows = cursor.fetchall()
                except sqlite3.Error as error:
                    error_message = str(error)
                except ValueError as error:
                    error_message = str(error)

                total += 1
                is_correct = (
                    predicted_rows is not None
                    and row_multiset(predicted_rows) == row_multiset(expected_rows)
                )
                if is_correct:
                    correct += 1
                if error_message:
                    errors += 1
                    print(f"Line {line_number}: {error_message}")
                details.append({
                    "question": question,
                    "correct": int(is_correct),
                    "error": error_message,
                    "expected_result": json.dumps(expected_rows, ensure_ascii=False),
                    "predicted_result": (
                        json.dumps(predicted_rows, ensure_ascii=False)
                        if predicted_rows is not None else ""
                    ),
                })
    finally:
        connection.close()

    if total == 0:
        raise ValueError(f"No predictions found in {args.predictions}")

    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        with args.details.open("w", encoding="utf-8", newline="") as destination:
            writer = csv.DictWriter(destination, fieldnames=[
                "question", "correct", "error", "expected_result", "predicted_result"
            ])
            writer.writeheader()
            writer.writerows(details)

    accuracy = correct / total
    print(f"Accuracy: {accuracy:.4f} ({accuracy:.2%})")
    print(f"Correct: {correct}/{total}")
    print(f"SQL errors: {errors}")


if __name__ == "__main__":
    main()
