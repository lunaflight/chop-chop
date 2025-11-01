from __future__ import annotations

EMPTY_INTERPRETABLE = ["\xa0"]


def join_with_br(strings: list[str]) -> str:
    all_parts: list[str] = []

    for s in strings:
        for empty_interpretable in EMPTY_INTERPRETABLE:
            new_s = s.replace(empty_interpretable, "")

        parts = [part.strip() for part in new_s.split("\n")]
        all_parts.extend(part for part in parts if part)

    return "<br>".join(all_parts)
