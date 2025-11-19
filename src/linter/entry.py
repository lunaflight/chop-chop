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


class ReferenceEntry(BaseModel):
    name: str
    link: str | None = None


class EtymologyEntry(BaseModel):
    etyPath: list[str]
    etyScheme: list[str] | None = None
    etyType: list[str] | None = None
    special: list[str] | None = None
    etyScript: list[str] | None = None
    etyTrad: list[str] | None = None
    etyRoman: list[str]
    etyLit: list[str]


PartOfSpeech: TypeAlias = list[DefinitionEntry]


class T(BaseModel):
    word: str
    trieId: str
    sense: str
    etyNotes: str | None = None
    origin: list[EtymologyEntry]
    origLink: list[str] | None = None
    meanings: dict[str, PartOfSpeech]
    usage: str | None = None
    related: list[str] | None = None
    category: list[str] | None = None
    references: list[ReferenceEntry] | None = None
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
        "related": ["word", "another word"],
        "category": ["locations"],
        "references": [{
            "name": "1970 Jan 1, Name. Reddit, \"Title\"",
            "url": "https://www.reddit.com"
            }],
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
