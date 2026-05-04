from __future__ import annotations

from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    """Load the small YAML subset used by this repository's config files."""
    text = Path(path).read_text(encoding="utf-8")
    return _parse_yaml_subset(text)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    try:
        return int(value)
    except ValueError:
        return value


def _parse_yaml_subset(text: str) -> dict[str, Any]:
    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for raw in lines:
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if stripped.startswith("- "):
            item = stripped[2:]
            if not isinstance(parent, list):
                raise ValueError(f"List item without list parent: {raw}")
            if ": " in item or item.endswith(":"):
                key, _, value = item.partition(":")
                child: dict[str, Any] = {}
                parent.append(child)
                if value.strip():
                    child[key] = _parse_scalar(value)
                else:
                    grandchild: dict[str, Any] = {}
                    child[key] = grandchild
                    stack.append((indent, child))
                    stack.append((indent + 2, grandchild))
                    continue
                stack.append((indent, child))
            else:
                parent.append(_parse_scalar(item))
            continue

        key, sep, value = stripped.partition(":")
        if not sep:
            raise ValueError(f"Unsupported YAML line: {raw}")
        if value.strip():
            parent[key] = _parse_scalar(value)
            continue

        next_is_list = _next_content_is_list(lines, raw)
        child = [] if next_is_list else {}
        parent[key] = child
        stack.append((indent, child))

    return root


def _next_content_is_list(lines: list[str], current: str) -> bool:
    index = lines.index(current)
    current_indent = len(current) - len(current.lstrip(" "))
    for next_line in lines[index + 1 :]:
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        if next_indent <= current_indent:
            return False
        return next_line.strip().startswith("- ")
    return False
