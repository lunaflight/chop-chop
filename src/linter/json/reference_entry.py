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
