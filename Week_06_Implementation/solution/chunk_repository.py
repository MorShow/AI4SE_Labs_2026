"""Split Python source into semantic chunks with file and class context.

Run without arguments to rebuild chunks.json for the cloned playground.
Only the Python standard library is required; source files are never executed.
"""

from __future__ import annotations

import argparse
import ast
import json
import tokenize
from collections import Counter
from pathlib import Path
from typing import Any

FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)
ASSIGNMENTS = (ast.Assign, ast.AnnAssign, ast.AugAssign)
FIXTURES = frozenset({"setUp", "tearDown", "setUpClass", "tearDownClass"})
EXCLUDED_DIRS = frozenset({".git", ".venv", "venv", "__pycache__", "node_modules"})
HERE = Path(__file__).resolve().parent


class Source:
    """Keep original source text alongside its parsed syntax tree."""

    def __init__(self, path: Path) -> None:
        # Honour Python encoding declarations rather than assuming UTF-8 input.
        with tokenize.open(path) as stream:
            self.text = stream.read()
        self.lines = self.text.splitlines()
        self.tree = ast.parse(self.text, filename=str(path))

    def span(self, node: ast.AST) -> tuple[int, int]:
        """Include decorators and adjacent comments belonging to the definition."""
        decorators = getattr(node, "decorator_list", [])
        start = min([node.lineno] + [item.lineno for item in decorators])
        end = node.end_lineno
        if end is None:
            raise ValueError("AST node has no source end position")
        # Attach consecutive leading comments at the definition's indentation.
        while start > 1:
            previous = self.lines[start - 2]
            indent = len(previous) - len(previous.lstrip())
            if not previous.lstrip().startswith("#") or indent != node.col_offset:
                break
            start -= 1
        # AST end positions omit trailing comment-only lines in function bodies.
        if isinstance(node, (*FUNCTIONS, ast.ClassDef)):
            for index in range(end, len(self.lines)):
                line = self.lines[index]
                if not line.strip():
                    continue
                indent = len(line) - len(line.lstrip())
                if line.lstrip().startswith("#") and indent > node.col_offset:
                    end = index + 1
                else:
                    break
        return start, end

    def extract(self, node: ast.AST) -> str:
        start, end = self.span(node)
        return "\n".join(self.lines[start - 1:end])

    def definition(self, node: ast.AST) -> dict[str, Any]:
        start, end = self.span(node)
        return {
            "name": node.name,
            "start_line": start,
            "end_line": end,
            "content": self.extract(node),
        }


def is_stub(node: ast.AST) -> bool:
    """Identify syntactic placeholders, not whether a symbol needs fixing."""
    body = list(getattr(node, "body", []))
    if body and isinstance(body[0], ast.Expr):
        value = body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            body = body[1:]
    return not body or all(
        isinstance(statement, ast.Pass)
        or (
            isinstance(statement, ast.Expr)
            and isinstance(statement.value, ast.Constant)
            and statement.value.value is Ellipsis
        )
        for statement in body
    )


def scope_statements(nodes: list[ast.stmt]):
    """Visit statements in a scope, including guards, without entering definitions."""
    for node in nodes:
        if isinstance(node, (*FUNCTIONS, ast.ClassDef)):
            continue
        yield node
        # Include assignments/imports inside if, try, and other scope-level blocks.
        for _field, value in ast.iter_fields(node):
            if isinstance(value, list):
                yield from scope_statements([item for item in value if isinstance(item, ast.stmt)])
                for item in value:
                    if isinstance(item, ast.ExceptHandler):
                        yield from scope_statements(item.body)


def class_metadata(source: Source, node: ast.ClassDef, current: ast.AST) -> dict[str, Any]:
    methods = [item for item in node.body if isinstance(item, FUNCTIONS)]
    constructor = next((item for item in methods if item.name == "__init__"), None)
    return {
        "name": node.name,
        "docstring": ast.get_docstring(node, clean=False),
        "bases": [ast.get_source_segment(source.text, base) for base in node.bases],
        "decorators": [ast.get_source_segment(source.text, dec) for dec in node.decorator_list],
        "constructor": source.definition(constructor)
        if constructor is not None and constructor is not current else None,
        "class_variables": [
            source.extract(item) for item in scope_statements(node.body)
            if isinstance(item, ASSIGNMENTS)
        ],
        "fixtures": [
            source.definition(item) for item in methods
            if item.name in FIXTURES and item is not current
        ],
    }


def chunk_file(path: Path, source_root: Path) -> list[dict[str, Any]]:
    """Create chunks for one file, preserving complete methods and functions."""
    source = Source(path)
    relative = path.relative_to(source_root)
    file_path = relative.as_posix()
    chunk_type = "test" if (
        "tests" in relative.parts[:-1]
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
    ) else "code"
    statements = list(scope_statements(source.tree.body))
    file_context = {
        "path": file_path,
        "docstring": ast.get_docstring(source.tree, clean=False),
        "imports": [source.extract(item) for item in statements if isinstance(item, (ast.Import, ast.ImportFrom))],
        "globals": [source.extract(item) for item in statements if isinstance(item, ASSIGNMENTS)],
    }
    chunks = []

    def add(node: ast.AST, kind: str, owner: ast.ClassDef | None = None) -> None:
        qualified_name = f"{owner.name}.{node.name}" if owner is not None and kind == "method" else node.name
        start, end = source.span(node)
        chunks.append({
            "schema_version": 1,
            "id": f"{file_path}::{qualified_name}",
            "chunk_type": chunk_type,
            "symbol_kind": kind,
            "qualified_name": qualified_name,
            "name": node.name,
            "start_line": start,
            "end_line": end,
            "is_stub": is_stub(node),
            "content": source.extract(node),
            "metadata": {
                "file": file_context,
                "class": class_metadata(source, owner, node) if owner is not None else None,
            },
        })

    for node in source.tree.body:
        if isinstance(node, FUNCTIONS):
            add(node, "function")
        elif isinstance(node, ast.ClassDef):
            methods = [item for item in node.body if isinstance(item, FUNCTIONS)]
            if methods:
                for method in methods:
                    add(method, "method", node)
            else:
                add(node, "class", node)

    if not chunks and source.text.strip():
        chunks.append({
            "schema_version": 1,
            "id": f"{file_path}::<module>",
            "chunk_type": chunk_type,
            "symbol_kind": "module",
            "qualified_name": "<module>",
            "name": path.stem,
            "start_line": 1,
            "end_line": len(source.lines),
            "is_stub": False,
            "content": "\n".join(source.lines),
            "metadata": {"file": file_context, "class": None},
        })
    return chunks


def chunk_repository(source_root: Path) -> list[dict[str, Any]]:
    """Read files deterministically; nested definitions remain in their parent."""
    source_root = source_root.resolve(strict=True)
    if not source_root.is_dir():
        raise ValueError(f"Source root is not a directory: {source_root}")
    chunks = []
    for path in sorted(source_root.rglob("*.py")):
        if not EXCLUDED_DIRS.intersection(path.relative_to(source_root).parts[:-1]):
            chunks.extend(chunk_file(path, source_root))
    # Property getters/setters or repeated definitions can share a qualified name.
    counts = Counter(chunk["id"] for chunk in chunks)
    for chunk in chunks:
        if counts[chunk["id"]] > 1:
            chunk["id"] += f"@{chunk['start_line']}"
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=HERE / "AI4SE_Playground" / "playground")
    parser.add_argument("--output", type=Path, default=HERE / "chunks.json")
    args = parser.parse_args()
    chunks = chunk_repository(args.source)
    if not chunks:
        parser.error("No non-empty Python source files found")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(chunks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(chunks)} chunks to {args.output}")
    print("Types:", dict(Counter(chunk["chunk_type"] for chunk in chunks)))
    print("Symbols:", dict(Counter(chunk["symbol_kind"] for chunk in chunks)))
    print(f"Largest chunk body: {max(chunk['end_line'] - chunk['start_line'] + 1 for chunk in chunks)} lines")


if __name__ == "__main__":
    main()
