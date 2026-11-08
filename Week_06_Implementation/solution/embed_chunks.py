"""Embed repository chunks with a local Ollama model and store them in NumPy.

Run `ollama pull qwen3-embedding:0.6b` first. Use --prepare-only to inspect
the exact embedding inputs without contacting Ollama. No API key is needed.
"""

from __future__ import annotations

import argparse
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = "qwen3-embedding:0.6b"
OLLAMA_URL = "http://localhost:11434"


class OllamaClient:
    """Minimal client for Ollama's native batch embedding endpoint."""

    def __init__(self, base_url: str = OLLAMA_URL, timeout: float = 300.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def embed(self, *, model: str, input: list[str]) -> dict[str, Any]:
        payload = json.dumps({"model": model, "input": input, "truncate": False}).encode("utf-8")
        request = Request(
            f"{self.base_url}/api/embed", data=payload,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ValueError(
                f"Ollama returned HTTP {exc.code}: {detail}. "
                f"Check the model with: ollama pull {model}"
            ) from exc
        except (URLError, TimeoutError) as exc:
            raise ValueError(
                f"Cannot reach Ollama at {self.base_url}: {exc}. "
                "Start Ollama (ollama serve) and retry."
            ) from exc


def render_chunk(chunk: dict[str, Any]) -> str:
    """Render semantic attributes as labelled text, preserving original code."""
    file = chunk["metadata"]["file"]
    owner = chunk["metadata"]["class"]
    sections = [
        f"Chunk type: {chunk['chunk_type']}",
        f"Symbol kind: {chunk['symbol_kind']}",
        f"Symbol: {chunk['qualified_name']}",
        f"Placeholder body: {chunk['is_stub']}",
        f"File: {file['path']}",
    ]

    def add(label: str, value: str | None) -> None:
        if value:
            sections.append(f"{label}:\n{value}")

    add("File docstring", file["docstring"])
    add("Imports", "\n".join(file["imports"]))
    add("Module globals", "\n".join(file["globals"]))
    if owner is not None:
        sections.append(f"Class: {owner['name']}")
        add("Class docstring", owner["docstring"])
        add("Base classes", ", ".join(owner["bases"]))
        add("Class decorators", "\n".join(f"@{item}" for item in owner["decorators"]))
        add("Class variables", "\n".join(owner["class_variables"]))
        if owner["constructor"] is not None:
            add("Constructor", owner["constructor"]["content"])
        for fixture in owner["fixtures"]:
            add(f"Test fixture {fixture['name']}", fixture["content"])
    add("Source code", chunk["content"])
    return "\n\n".join(sections)


def prepare_chunks(chunks: list[dict[str, Any]]) -> dict[str, np.ndarray]:
    """Keep row-aligned IDs and texts; full records stay in chunks.json."""
    if not chunks:
        raise ValueError("The input contains no chunks")
    ids = [chunk["id"] for chunk in chunks]
    if len(set(ids)) != len(ids):
        raise ValueError("Chunk IDs must be unique")
    # Unicode arrays load with allow_pickle=False.
    return {
        "chunk_ids": np.asarray(ids, dtype=np.str_),
        "texts": np.asarray([render_chunk(chunk) for chunk in chunks], dtype=np.str_),
    }


def embed_texts(texts: list[str], client: Any, batch_size: int = 32, model: str = MODEL) -> np.ndarray:
    """Call the embedding API in batches and preserve input order."""
    if batch_size < 1 or batch_size > 2048:
        raise ValueError("Batch size must be between 1 and 2048")
    if not texts or any(not text.strip() for text in texts):
        raise ValueError("Embedding inputs must be non-empty")
    batches = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        response = client.embed(model=model, input=batch)
        vectors = np.asarray(response["embeddings"], dtype=np.float32)
        if vectors.ndim != 2 or vectors.shape[0] != len(batch) or vectors.shape[1] == 0 or not np.isfinite(vectors).all():
            raise ValueError("Embedding response contains invalid vectors")
        if batches and vectors.shape[1] != batches[0].shape[1]:
            raise ValueError("Embedding vector lengths differ between batches")
        batches.append(vectors)
        print(f"Embedded {start + len(batch)}/{len(texts)} chunks", flush=True)
    return np.concatenate(batches, axis=0)


def save_archive(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """Write named NumPy arrays, with no object arrays or pickle dependency."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # An open file prevents NumPy from silently appending another extension.
    with path.open("wb") as stream:
        np.savez_compressed(stream, **arrays)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "chunks.json")
    parser.add_argument("--output", type=Path, help="Defaults to embeddings.npz (or embedding_inputs.npz with --prepare-only)")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--ollama-url", default=os.environ.get("OLLAMA_HOST", OLLAMA_URL))
    parser.add_argument("--prepare-only", action="store_true", help="Save chunk IDs and texts without calling Ollama")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 2048:
        parser.error("--batch-size must be between 1 and 2048")
    output = args.output or HERE / ("embedding_inputs.npz" if args.prepare_only else "embeddings.npz")
    if output.suffix.lower() != ".npz":
        parser.error("--output must have the .npz extension")
    if output.resolve() == args.input.resolve():
        parser.error("Input and output must be different files")
    try:
        chunks = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(chunks, list):
            raise ValueError("Input must be a JSON array of chunks")
        arrays = prepare_chunks(chunks)
        if not args.prepare_only:
            client = OllamaClient(args.ollama_url)
            arrays["embeddings"] = embed_texts(arrays["texts"].tolist(), client, args.batch_size, args.model)
        save_archive(output, arrays)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    if args.prepare_only:
        print(f"Prepared {len(chunks)} chunks in {output}; no embeddings or API calls.")
    else:
        print(f"Saved {len(chunks)} chunk-embedding pairs to {output}")


if __name__ == "__main__":
    main()
