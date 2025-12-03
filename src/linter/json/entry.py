import json
from itertools import chain
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from src.linter.json import (
    etymology_entry,
    part_of_speech_entry,
    particle_entry,
    reference_entry,
    specs,
)

# This is required because Pydantic will not recognise a underscore-prefixed
# field as a public field.
FIELD_ALIASES = {"_id": "id"}


class T(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Fields added after prod
    forms: list[str] | None = None
    formsClean: list[str] | None = None

    id: int | None = None
    word: str
    trieId: str
    sense: str
    etyNotes: str | None = None
    origin: list[etymology_entry.T]
    origlink: list[str] | None = None
    meanings: dict[str, part_of_speech_entry.T]
    usage: str | None = None
    particles: list[particle_entry.T] | None = None
    related: list[str] | None = None
    category: list[str] | None = None
    references: list[reference_entry.T] | None = None
    credits: list[str] | None = None


def create(dict_: dict[str, Any]) -> T | ValidationError:
    try:
        processed_dict = dict_.copy()
        for old_key, new_key in FIELD_ALIASES.items():
            if old_key in processed_dict:
                processed_dict[new_key] = processed_dict.pop(old_key)

        return T(**processed_dict)
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
        "origlink": [],
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
                "link": "https://www.reddit.com",
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
    return [
        *([t.etyNotes] if t.etyNotes is not None else []),
        *([t.usage] if t.usage is not None else []),
        *chain.from_iterable(
            part_of_speech_entry.self_written_sentences(e)
            for e in t.meanings.values()
        ),
        *chain.from_iterable(
            etymology_entry.self_written_sentences(e) for e in t.origin
        ),
        *chain.from_iterable(
            particle_entry.self_written_sentences(e)
            for e in (t.particles or [])
        ),
        *chain.from_iterable(
            reference_entry.self_written_sentences(e)
            for e in (t.references or [])
        ),
    ]


def get_linked_words(t: T) -> list[str]:
    return [
        *specs.get_linked_words(t.etyNotes or ""),
        *specs.get_linked_words(t.usage or ""),
        *chain.from_iterable(
            part_of_speech_entry.get_linked_words(e)
            for e in t.meanings.values()
        ),
        *chain.from_iterable(
            etymology_entry.get_linked_words(e) for e in t.origin
        ),
        *chain.from_iterable(
            particle_entry.get_linked_words(e) for e in (t.particles or [])
        ),
        *(t.related or []),
        *chain.from_iterable(
            reference_entry.get_linked_words(e) for e in (t.references or [])
        ),
    ]


def all_strings(t: T) -> list[str]:
    return [
        t.word,
        t.trieId,
        t.sense,
        *([t.etyNotes] if t.etyNotes is not None else []),
        *chain.from_iterable(etymology_entry.all_strings(e) for e in t.origin),
        *(t.origlink or []),
        *chain.from_iterable(
            part_of_speech_entry.all_strings(e) for e in t.meanings.values()
        ),
        *([t.usage] if t.usage is not None else []),
        *chain.from_iterable(
            particle_entry.all_strings(e) for e in (t.particles or [])
        ),
        *(t.related or []),
        *(t.category or []),
        *chain.from_iterable(
            reference_entry.all_strings(e) for e in (t.references or [])
        ),
        *(t.credits or []),
    ]
