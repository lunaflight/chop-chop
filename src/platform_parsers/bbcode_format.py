from __future__ import annotations


def join_with_br(strings: list[str]) -> str:
    strings = [s.replace("\n", "<br>") for s in strings]
    return "<br>".join(strings)
