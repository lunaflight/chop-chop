from pydantic import BaseModel, ConfigDict


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    speaker: str
    file: str


def get_linked_words(_t: T) -> list[str]:
    return []


def self_written_sentences(_t: T) -> list[str]:
    return []


def all_strings(t: T) -> list[str]:
    return [t.speaker, t.file]
