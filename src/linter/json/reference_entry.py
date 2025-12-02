from pydantic import BaseModel


class T(BaseModel):
    name: str
    link: str | None = None


def get_linked_words(_t: T) -> list[str]:
    # Assuming that no linked words are in reference entries.
    return []


def self_written_sentences(_t: T) -> list[str]:
    # Assuming that no linked words are in reference entries.
    return []


def all_strings(t: T) -> list[str]:
    arr: list[str | None] = [t.name, t.link]
    return [s for s in arr if s]
