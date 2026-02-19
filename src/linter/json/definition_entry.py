from itertools import chain

from pydantic import BaseModel, ConfigDict

from src.linter.json import attestation_entry, image_entry, specs


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definition: str
    example: list[attestation_entry.T] | None = None
    synonyms: list[str] | None = None
    antonyms: list[str] | None = None
    image: list[image_entry.T] | None = None


def get_linked_words(t: T) -> list[str]:
    return [
        *specs.get_linked_words(t.definition),
        *chain.from_iterable(
            attestation_entry.get_linked_words(e) for e in (t.example or [])
        ),
        *(t.synonyms or []),
        *(t.antonyms or []),
        *chain.from_iterable(
            image_entry.get_linked_words(e) for e in (t.image or [])
        ),
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
        *chain.from_iterable(
            image_entry.all_strings(e) for e in (t.image or [])
        ),
    ]


def get_attestations(t: T) -> list[attestation_entry.T]:
    return t.example if t.example is not None else []
