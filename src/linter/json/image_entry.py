from pydantic import BaseModel, ConfigDict

from src.linter.json import specs


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    src: str
    caption: str | None = None


def get_linked_words(t: T) -> list[str]:
    return specs.get_linked_words(t.caption or "")


def self_written_sentences(_t: T) -> list[str]:
    return []


def all_strings(t: T) -> list[str]:
    return [t.src, *([t.caption] if t.caption is not None else [])]
