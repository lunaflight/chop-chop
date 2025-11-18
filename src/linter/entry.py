import json
from typing import Any, TypeAlias

from pydantic import BaseModel, ValidationError


class Attestation(BaseModel):
    eg: str
    src: str | None = None


class DefinitionEntry(BaseModel):
    definition: str
    example: list[Attestation] | None = None
    synonyms: list[str] | None = None
    antonyms: list[str] | None = None


PartOfSpeech: TypeAlias = list[DefinitionEntry]


class T(BaseModel):
    word: str
    trieId: str
    sense: str
    etyNotes: str | None = None
    meanings: dict[str, PartOfSpeech]
    usage: str | None = None
    category: list[str] | None = None


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
        "meanings": {"noun": [{"definition": "noun definition"}]},
        "usage": "Usage notes.",
        "category": [],
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
