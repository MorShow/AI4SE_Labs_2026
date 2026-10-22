import hashlib
from pathlib import Path

from .schemas import SourceChunk


def load_corpus(directory: Path, chunk_chars: int = 14000) -> list[SourceChunk]:
    root = directory.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Input must be a directory: {root}")
    sources: list[SourceChunk] = []
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in {".txt", ".eml"} or not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"Source escapes the input directory: {path}")
        relative = path.relative_to(root).as_posix()
        # These .eml files are textual threads, not a single MIME message.
        # Keep the complete file: parsing only the first email would lose replies.
        text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        lines = text.splitlines(keepends=True)
        if not text.strip():
            continue
        if any(len(line) > chunk_chars for line in lines):
            raise ValueError(f"A line in {relative} exceeds --chunk-chars; increase that limit.")
        document_id = hashlib.sha256(relative.encode()).hexdigest()[:12]
        start = 0
        part = 1
        while start < len(lines):
            end = start
            size = 0
            while end < len(lines) and size + len(lines[end]) <= chunk_chars:
                size += len(lines[end])
                end += 1
            sources.append(SourceChunk(
                id=f"SRC-{document_id}-{part:03d}", document=relative,
                start_line=start + 1, end_line=end, text="".join(lines[start:end]),
            ))
            if end == len(lines):
                break
            start = max(start + 1, end - 6)
            part += 1
    if not sources:
        raise ValueError("No non-empty UTF-8 .txt or textual .eml files found in the input directory.")
    return sources
