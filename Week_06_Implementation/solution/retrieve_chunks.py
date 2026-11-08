"""Retrieve 20 chunks by cosine similarity, then select 5 with cosine-based MMR.

Accept a text/JSON --query, an --input file, piped input, or an interactive
multiline paste. For a JSON task array, select one task with --task-index.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path
from typing import Any

import numpy as np

from embed_chunks import HERE, MODEL, OLLAMA_URL, OllamaClient

QUERY_INSTRUCTION = (
    "Given a Python programming task, retrieve repository code and tests "
    "needed to implement it."
)


def parse_task(raw: str, task_index: int | None = None) -> str | dict[str, Any]:
    """Accept plain text or JSON, selecting exactly one task from an array."""
    raw = raw.strip()
    if not raw:
        raise ValueError("The task must not be empty")
    try:
        task = json.loads(raw)
    except json.JSONDecodeError as exc:
        if raw.startswith(("{", "[")):
            raise ValueError(f"Invalid task JSON: {exc}") from exc
        task = raw
    if isinstance(task, list):
        if task_index is None:
            if len(task) != 1:
                raise ValueError("For a JSON task array, use --task-index (zero-based) to select one task")
            task_index = 0
        if not 0 <= task_index < len(task):
            raise ValueError(f"Task index must be between 0 and {len(task) - 1}")
        task = task[task_index]
    elif task_index is not None:
        raise ValueError("--task-index only applies to JSON task arrays")
    if not isinstance(task, (str, dict)):
        raise ValueError("A task must be text or a JSON object")
    return task


def task_to_text(task: str | dict[str, Any]) -> str:
    """Render task fields as labelled text without using an LLM."""
    if isinstance(task, str):
        result = task.strip()
    else:
        labels = {"file": "File", "class": "Class", "method": "Method", "docstring": "Description"}
        lines = []

        def visit(value: Any, label: str) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    visit(item, f"{label}.{key}" if label else str(key))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    visit(item, f"{label}[{index}]")
            elif value is not None:
                text = str(value).strip()
                if text.startswith(('"""', "'''")) and text.endswith(text[:3]) and len(text) >= 6:
                    text = text[3:-3]
                text = textwrap.dedent(text).strip()
                if text:
                    lines.append(f"{label}: {text}")

        keys = [key for key in labels if key in task]
        keys.extend(key for key in task if key not in labels)
        for key in keys:
            visit(task[key], labels.get(key, key))
        result = "\n".join(lines)
    if not result:
        raise ValueError("The task contains no text to embed")
    return result


def build_query(text: str) -> str:
    """Use Qwen's retrieval-query instruction format; documents stay unchanged."""
    return f"Instruct: {QUERY_INSTRUCTION}\nQuery: {text}"


def load_index(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load ID/vector pairs from the existing archive without pickle."""
    with np.load(path, allow_pickle=False) as archive:
        if not {"chunk_ids", "embeddings"}.issubset(archive.files):
            raise ValueError("The archive must contain chunk_ids and embeddings; use embeddings.npz")
        ids = archive["chunk_ids"]
        vectors = np.asarray(archive["embeddings"], dtype=np.float64)
    if ids.ndim != 1 or ids.dtype.kind not in "US" or len(set(ids.tolist())) != len(ids):
        raise ValueError("Chunk IDs must be a one-dimensional array of unique strings")
    if vectors.ndim != 2 or vectors.shape[0] != len(ids) or not len(ids) or not vectors.shape[1]:
        raise ValueError("Stored embeddings must have one non-empty vector per chunk ID")
    if not np.isfinite(vectors).all():
        raise ValueError("Stored embeddings contain non-finite values")
    return ids, vectors


def cosine_top_k(
    query: np.ndarray, ids: np.ndarray, vectors: np.ndarray, top_k: int = 20
) -> list[tuple[str, float]]:
    """Rank all vectors by exact cosine similarity, with stable tie ordering."""
    if top_k < 1:
        raise ValueError("top_k must be positive")
    query = np.asarray(query, dtype=np.float64)
    if query.ndim != 1 or vectors.ndim != 2 or query.shape[0] != vectors.shape[1]:
        raise ValueError("Query and stored vectors have different shapes; use the same embedding model")
    if len(ids) != len(vectors) or not len(ids):
        raise ValueError("There must be one ID for each stored vector")
    if not np.isfinite(query).all() or not np.isfinite(vectors).all():
        raise ValueError("Vectors must contain finite numbers")
    query_norm = np.linalg.norm(query)
    vector_norms = np.linalg.norm(vectors, axis=1)
    if query_norm == 0 or np.any(vector_norms == 0):
        raise ValueError("Cosine similarity is undefined for zero vectors")
    scores = (vectors @ query) / (vector_norms * query_norm)
    scores = np.clip(scores, -1.0, 1.0)
    selected = np.argsort(-scores, kind="stable")[:top_k]
    return [(str(ids[index]), float(scores[index])) for index in selected]


def retrieve(
    query: str,
    archive_path: Path = HERE / "embeddings.npz",
    top_k: int = 20,
    client: Any = None,
) -> list[tuple[str, float]]:
    """Embed one prepared query with the same model used for the chunk index."""
    if top_k < 1:
        raise ValueError("top_k must be positive")
    ids, vectors = load_index(archive_path)
    return cosine_top_k(embed_query(query, client), ids, vectors, top_k)


def embed_query(query: str, client: Any = None) -> np.ndarray:
    """Embed a single prepared query using the chunk index's Ollama model."""
    if client is None:
        client = OllamaClient()
    response = client.embed(model=MODEL, input=[query])
    query_vectors = np.asarray(response["embeddings"], dtype=np.float64)
    if query_vectors.ndim != 2 or query_vectors.shape[0] != 1:
        raise ValueError("Ollama must return exactly one query embedding")
    return query_vectors[0]


def mmr_select(
    relevance: np.ndarray, vectors: np.ndarray, count: int = 5, weight: float = 0.2,
) -> list[dict[str, float | int]]:
    """Balance raw query cosine against maximum non-negative chunk overlap."""
    if count < 1 or not 0 <= weight <= 1:
        raise ValueError("Selection count must be positive and MMR lambda must be in [0, 1]")
    relevance = np.asarray(relevance, dtype=np.float64)
    vectors = np.asarray(vectors, dtype=np.float64)
    if vectors.ndim != 2 or relevance.ndim != 1 or len(vectors) != len(relevance) or not len(relevance) or not vectors.shape[1]:
        raise ValueError("There must be one non-empty candidate vector per cosine score")
    if not np.isfinite(vectors).all() or not np.isfinite(relevance).all():
        raise ValueError("MMR inputs must be finite")
    norms = np.linalg.norm(vectors, axis=1)
    if np.any(norms == 0):
        raise ValueError("MMR cannot compare zero vectors")
    unit = vectors / norms[:, None]
    similarities = np.clip(unit @ unit.T, 0.0, 1.0)
    chosen = []
    remaining = list(range(len(relevance)))
    while remaining and len(chosen) < count:
        selected = [int(item["index"]) for item in chosen]
        overlap = np.max(similarities[:, selected], axis=1) if selected else np.zeros(len(relevance))
        utilities = weight * relevance - (1 - weight) * overlap
        # Seed with the most relevant candidate, also when lambda is zero.
        best = max(remaining, key=lambda index: utilities[index] if selected else relevance[index])
        chosen.append({"index": best, "mmr_score": float(utilities[best]), "overlap": float(overlap[best])})
        remaining.remove(best)
    return chosen


def retrieve_context(
    task: str | dict[str, Any],
    archive_path: Path = HERE / "embeddings.npz",
    candidate_count: int = 20,
    final_count: int = 5,
    mmr_lambda: float = 0.2,
    client: Any = None,
) -> dict[str, Any]:
    """Return cosine candidates and diverse final chunk texts for generation."""
    if not 1 <= final_count <= candidate_count or not 0 <= mmr_lambda <= 1:
        raise ValueError("Require 1 <= final count <= candidate count and MMR lambda in [0, 1]")
    text = task_to_text(task)
    query = build_query(text)
    ids, vectors = load_index(archive_path)
    with np.load(archive_path, allow_pickle=False) as archive:
        if "texts" not in archive.files:
            raise ValueError("The archive must contain texts for context selection")
        texts = archive["texts"]
        if texts.ndim != 1 or len(texts) != len(ids) or texts.dtype.kind not in "US":
            raise ValueError("Archive texts must align with chunk IDs")
    candidates = cosine_top_k(embed_query(query, client), ids, vectors, candidate_count)
    positions = {str(chunk_id): index for index, chunk_id in enumerate(ids)}
    rows = [positions[chunk_id] for chunk_id, _score in candidates]
    cosine = np.asarray([score for _chunk_id, score in candidates])
    details = [{"id": chunk_id, "cosine": float(score)} for chunk_id, score in candidates]
    selection = mmr_select(cosine, vectors[rows], final_count, mmr_lambda)
    selected = []
    for item in selection:
        index = int(item["index"])
        selected.append({
            **details[index], "mmr_score": item["mmr_score"], "overlap": item["overlap"],
            "text": str(texts[rows[index]]),
        })
    return {"task_text": text, "embedding_input": query, "candidates": details, "selected": selected}


def read_paste() -> str:
    """Keep multiline JSON and text intact; END terminates interactive input."""
    if not sys.stdin.isatty():
        return sys.stdin.read()
    print("Paste a text task or JSON. Finish with a line containing END:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--query", help="Plain text or a JSON task object")
    source.add_argument("--input", type=Path, help="UTF-8 text or JSON file")
    parser.add_argument("--task-index", type=int, help="Zero-based task index for a JSON array")
    parser.add_argument("--top-k", "--candidates", dest="candidate_count", type=int, default=20, help="Cosine candidate count (default: 20)")
    parser.add_argument("--final", type=int, default=5, help="Final MMR selection count (default: 5)")
    parser.add_argument("--mmr-lambda", type=float, default=0.2, help="0 favours diversity; 1 favours cosine relevance")
    parser.add_argument("--index", type=Path, default=HERE / "embeddings.npz")
    parser.add_argument("--ollama-url", default=os.environ.get("OLLAMA_HOST", OLLAMA_URL))
    args = parser.parse_args()
    if not 1 <= args.final <= args.candidate_count or not 0 <= args.mmr_lambda <= 1:
        parser.error("Require 1 <= --final <= --top-k and --mmr-lambda in [0, 1]")
    try:
        if args.input is not None:
            raw = args.input.read_text(encoding="utf-8-sig")
        else:
            raw = args.query if args.query is not None else read_paste()
        task = parse_task(raw, args.task_index)
        query = build_query(task_to_text(task))
        print(f"Embedding input:\n{query}\n", flush=True)
        result = retrieve_context(task, args.index, args.candidate_count, args.final, args.mmr_lambda, OllamaClient(args.ollama_url))
        print(f"Top {len(result['candidates'])} chunk IDs (descending cosine similarity):")
        for rank, item in enumerate(result["candidates"], 1):
            print(f"{rank:02d}. {item['id']}  (cosine={item['cosine']:.6f})")
        print(f"\nFinal {len(result['selected'])} chunk IDs (MMR selection order):")
        for rank, item in enumerate(result["selected"], 1):
            print(f"{rank:02d}. {item['id']} cosine={item['cosine']:.6f} overlap={item['overlap']:.6f} mmr={item['mmr_score']:.6f}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
