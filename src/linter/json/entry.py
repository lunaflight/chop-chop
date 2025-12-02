import json
from typing import Any

from pydantic import BaseModel, ValidationError

from src.linter.json import (
    etymology_entry,
    part_of_speech_entry,
    particle_entry,
    reference_entry,
    specs,
)


class T(BaseModel):
    word: str
    trieId: str
    sense: str
    etyNotes: str | None = None
    origin: list[etymology_entry.T]
    origLink: list[str] | None = None
    meanings: dict[str, part_of_speech_entry.T]
    usage: str | None = None
    particles: list[particle_entry.T] | None = None
    related: list[str] | None = None
    category: list[str] | None = None
    references: list[reference_entry.T] | None = None
    credits: list[str] | None = None


def create(dict_: dict[str, Any]) -> T | ValidationError:
    try:
        return T(**dict_)
    except ValidationError as e:
        return e


def create_for_testing(**kwargs: Any) -> T:  # noqa: ANN401
    default_data = {
        "word": "Test Word",
        "trieId": "test word",
        "sense": "0",
        "etyNotes": "Etymology notes.",
        "origin": [
            {
                "etyPath": ["language"],
                "etyRoman": ["original word"],
                "etyLit": ["its meaning"],
            }
        ],
        "origLink": [],
        "meanings": {"noun": [{"definition": "noun definition"}]},
        "usage": "Usage notes.",
        "particles": [
            {
                "particle": "lah",
                "effect": "reassurance",
                "meaning": "noun definition with nuance",
            }
        ],
        "related": [],
        "category": ["locations"],
        "references": [
            {
                "name": '1970 Jan 1, Name. Reddit, "Title"',
                "url": "https://www.reddit.com",
            }
        ],
        "credits": ["Name for the suggestion."],
    }
    default_data.update(kwargs)
    t = create(default_data)
    if isinstance(t, ValidationError):
        raise t

    return t


def create_from_json(json_data: str) -> T | ValidationError:
    json_dict = json.loads(json_data)
    return create(json_dict)


def self_written_sentences(t: T) -> list[str]:
    self_written_sentences = []

    if t.etyNotes is not None:
        self_written_sentences.append(t.etyNotes)
    if t.usage is not None:
        self_written_sentences.append(t.usage)
    for part_of_speech in t.meanings.values():
        self_written_sentences.extend(
            definition_entry.definition for definition_entry in part_of_speech
        )

    return self_written_sentences


def get_linked_words(t: T) -> list[str]:
    linked_words = []

    linked_words.extend(specs.get_linked_words(t.etyNotes or ""))
    linked_words.extend(specs.get_linked_words(t.usage or ""))
    for part_of_speech_entry_ in t.meanings.values():
        linked_words.extend(
            part_of_speech_entry.get_linked_words(part_of_speech_entry_)
        )
    for etymology_entry_ in t.origin or []:
        linked_words.extend(etymology_entry.get_linked_words(etymology_entry_))
    for particle_entry_ in t.particles or []:
        linked_words.extend(particle_entry.get_linked_words(particle_entry_))
    linked_words.extend(t.related or [])
    for reference_entry_ in t.references or []:
        linked_words.extend(reference_entry.get_linked_words(reference_entry_))

    return linked_words
