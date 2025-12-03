from itertools import chain

from pydantic import BaseModel, ConfigDict

from src.linter.json import attestation_entry, specs


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definition: str
    example: list[attestation_entry.T] | None = None
    synonyms: list[str] | None = None
    antonyms: list[str] | None = None


def get_linked_words(t: T) -> list[str]:
    return [
        *specs.get_linked_words(t.definition),
        *chain.from_iterable(
            attestation_entry.get_linked_words(e) for e in (t.example or [])
        ),
        *(t.synonyms or []),
        *(t.antonyms or []),
    ]


def self_written_sentences(t: T) -> list[str]:
    return [t.definition]


def all_strings(t: T) -> list[str]:
    return [
        t.definition,
        *chain.from_iterable(
            attestation_entry.all_strings(e) for e in (t.example or [])
        ),
        *(t.synonyms or []),
        *(t.antonyms or []),
    ]
