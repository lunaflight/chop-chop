from pydantic import BaseModel

from src.linter.json import attestation_entry, specs


class T(BaseModel):
    definition: str
    example: list[attestation_entry.T] | None = None
    synonyms: list[str] | None = None
    antonyms: list[str] | None = None


def get_linked_words(t: T) -> list[str]:
    linked_words = []
    linked_words.extend(specs.get_linked_words(t.definition))
    if t.example:
        for attestation_entry_ in t.example:
            linked_words.extend(
                attestation_entry.get_linked_words(attestation_entry_)
            )
    if t.synonyms:
        linked_words.extend(t.synonyms)
    if t.antonyms:
        linked_words.extend(t.antonyms)
    return linked_words
