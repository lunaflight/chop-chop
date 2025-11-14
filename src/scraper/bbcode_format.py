from __future__ import annotations


def join_with_br(strings: list[str]) -> str:
    all_parts: list[str] = []

    for string in strings:
        parts = [part.strip() for part in string.split("\n")]
        all_parts.extend(part for part in parts if part)

    return "<br>".join(all_parts)
