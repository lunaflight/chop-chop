from pydantic import BaseModel

from src.linter.json import specs


class T(BaseModel):
    particle: str
    effect: str
    meaning: str
    example: str | None = None
    exampleSource: str | None = None


def get_linked_words(t: T) -> list[str]:
    linked_words = []
    linked_words.extend(specs.get_linked_words(t.meaning))
    linked_words.extend(specs.get_linked_words(t.example or ""))
    return linked_words


def self_written_sentences(t: T) -> list[str]:
    return [t.meaning]


def all_strings(t: T) -> list[str]:
    return [
        t.particle,
        t.effect,
        t.meaning,
        *([t.example] if t.example is not None else []),
        *([t.exampleSource] if t.exampleSource is not None else []),
    ]
