from pydantic import BaseModel, ConfigDict


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    link: str | None = None


def get_linked_words(_t: T) -> list[str]:
    # Assuming that no linked words are in reference entries.
    return []


def self_written_sentences(_t: T) -> list[str]:
    # Assuming that no linked words are in reference entries.
    return []


def all_strings(t: T) -> list[str]:
    return [t.name, *([t.link] if t.link is not None else [])]
