from __future__ import annotations

REPLACEMENTS = {
    "\xa0": "",  # non-breaking space
    "…": "...",
}


def join_with_br(strings: list[str]) -> str:
    all_parts: list[str] = []

    for s in strings:
        for key, val in REPLACEMENTS.items():
            new_s = s.replace(key, val)

        parts = [part.strip() for part in new_s.split("\n")]
        all_parts.extend(part for part in parts if part)

    return "<br>".join(all_parts)
