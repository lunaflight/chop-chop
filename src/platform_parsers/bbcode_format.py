from __future__ import annotations

from src import sanitizer


def join_with_br(strings: list[str]) -> str:
    all_parts: list[str] = []

    for string in strings:
        new_string = sanitizer.clean_unicode_for_output(string)

        parts = [part.strip() for part in new_string.split("\n")]
        all_parts.extend(part for part in parts if part)

    return "<br>".join(all_parts)
