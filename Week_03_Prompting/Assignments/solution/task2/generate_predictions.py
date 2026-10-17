import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SOLUTION_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SOLUTION_DIR / "data"
DEFAULT_QUESTIONS = DATA_DIR / "restaurants_dataset.csv"
PROMPTS_PATH = SOLUTION_DIR / "task1" / "prompts.yml"


def load_prompts(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    prompts = {}
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"([A-Za-z0-9_]+):", lines[index])
        if not match:
            raise ValueError(f"Invalid prompt name on line {index + 1} of {path}")
        name = match.group(1)
        index += 1
        if index >= len(lines) or lines[index] != "  prompt: |-":
            raise ValueError(f"Expected '  prompt: |-' after {name} in {path}")
        index += 1
        block = []
        while index < len(lines) and not re.fullmatch(r"[A-Za-z0-9_]+:", lines[index]):
            line = lines[index]
            if line and not line.startswith("    "):
                raise ValueError(f"Invalid indentation on line {index + 1} of {path}")
            block.append(line[4:] if line else "")
            index += 1
        template = "\n".join(block).rstrip("\n")
        if template.count("{{question}}") != 1:
            raise ValueError(f"Prompt {name} must contain {{question}} exactly once")
        prompts[name] = template
    return prompts


def read_questions(path):
    csv.field_size_limit(1_000_000_000)
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or "question" not in reader.fieldnames:
            raise ValueError(f"{path} must contain a 'question' column")
        questions = [row["question"] for row in reader]
    if not questions or any(not question for question in questions):
        raise ValueError(f"{path} must contain nonempty questions")
    return questions


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_") or "model"


def generate(url, api_key, model, prompt, timeout):
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url.rstrip("/") + "/api/generate", payload, headers)
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace").strip()
        try:
            detail = json.loads(detail).get("error", detail)
        except json.JSONDecodeError:
            pass
        raise RuntimeError(f"Ollama HTTP {error.code}: {detail or error.reason}") from error
    elapsed = time.perf_counter() - started
    if not isinstance(result.get("response"), str):
        raise ValueError("Ollama response has no text in 'response'")
    return result["response"].strip(), elapsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Model name shown by ollama list")
    parser.add_argument("--prompt", required=True, help="Prompt name from prompts.yml")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS,
                        help="CSV with a question column; can contain your test subset")
    parser.add_argument("--output-dir", type=Path, default=SOLUTION_DIR / "predictions")
    parser.add_argument("--url", default=os.getenv("OLLAMA_URL", "http://localhost:11434"),
                        help="Ollama server URL (default: local server)")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per question")
    args = parser.parse_args()

    prompts = load_prompts(PROMPTS_PATH)
    if args.prompt not in prompts:
        parser.error(f"Unknown prompt {args.prompt!r}; choose: {', '.join(prompts)}")
    questions = read_questions(args.questions)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_path = args.output_dir / (
        f"{safe_name(args.prompt)}_{safe_name(args.model)}_{timestamp}.csv"
    )
    api_key = os.getenv("OLLAMA_API_KEY")
    try:
        with output_path.open("x", encoding="utf-8", newline="") as destination:
            writer = csv.DictWriter(
                destination, fieldnames=["question", "predicted_sql", "total_time"]
            )
            writer.writeheader()
            for number, question in enumerate(questions, start=1):
                prompt = prompts[args.prompt].replace("{{question}}", question)
                sql, elapsed = generate(
                    args.url, api_key, args.model, prompt, args.timeout
                )
                writer.writerow({
                    "question": question,
                    "predicted_sql": sql,
                    "total_time": f"{elapsed:.6f}",
                })
                destination.flush()
                print(f"{number}/{len(questions)}: {elapsed:.2f}s", flush=True)
    except (RuntimeError, URLError, TimeoutError, ValueError) as error:
        print(f"Generation stopped: {error}. Completed rows remain in {output_path}",
              file=sys.stderr)
        return 1

    print(f"Predictions: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
