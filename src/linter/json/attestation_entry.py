from pydantic import BaseModel

from src.linter.json import specs


class T(BaseModel):
    eg: str
    src: str | None = None


def get_linked_words(t: T) -> list[str]:
    return specs.get_linked_words(t.eg)


def self_written_sentences(_t: T) -> list[str]:
    return []


def all_strings(t: T) -> list[str]:
    return [t.eg, *([t.src] if t.src is not None else [])]
