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
    if t.example:
        linked_words.extend(specs.get_linked_words(t.example))
    return linked_words


def self_written_sentences(t: T) -> list[str]:
    return [t.meaning]


def all_strings(t: T) -> list[str]:
    arr: list[str | None] = [
        t.particle,
        t.effect,
        t.meaning,
        t.example,
        t.exampleSource,
    ]
    return [s for s in arr if s]
