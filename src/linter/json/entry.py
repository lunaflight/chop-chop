import json
import re
from typing import Any, TypeAlias

from pydantic import BaseModel, ValidationError


class AttestationEntry(BaseModel):
    eg: str
    src: str | None = None


class DefinitionEntry(BaseModel):
    definition: str
    example: list[AttestationEntry] | None = None
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


class ParticleEntry(BaseModel):
    particle: str
    effect: str
    meaning: str
    example: str | None = None
    exampleSource: str | None = None


PartOfSpeechEntry: TypeAlias = list[DefinitionEntry]


class T(BaseModel):
    word: str
    trieId: str
    sense: str
    etyNotes: str | None = None
    origin: list[EtymologyEntry]
    origLink: list[str] | None = None
    meanings: dict[str, PartOfSpeechEntry]
    usage: str | None = None
    particles: list[ParticleEntry] | None = None
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


# TODO: C901 should not be ignored because the below function is indeed
# very hard to read. What should be done is a split out of all the entries
# to their own files, and each of the types should implement a
# get_linked_words, get_self_written_sentences among other things.
#
# This would miscellaneously mean that AT_WORD_CAPTURE_REGEX should be
# part of json_specs.
def get_linked_words(t: T) -> list[str]:  # noqa: C901
    at_word_capture_regex = r"@\{(?:[^|}]+\|)?([^}]+)\}"

    sentences_with_at_words: list[str] = []
    linked_words = []

    if t.etyNotes is not None:
        sentences_with_at_words.append(t.etyNotes)
    if t.usage is not None:
        sentences_with_at_words.append(t.usage)
    for part_of_speech in t.meanings.values():
        for definition_entry in part_of_speech:
            sentences_with_at_words.append(definition_entry.definition)
            if definition_entry.example is not None:
                sentences_with_at_words.extend(
                    example.eg for example in definition_entry.example
                )
            if definition_entry.synonyms is not None:
                linked_words.extend(definition_entry.synonyms)
            if definition_entry.antonyms is not None:
                linked_words.extend(definition_entry.antonyms)

    if t.particles is not None:
        sentences_with_at_words.extend(
            particle_entry.example
            for particle_entry in t.particles
            if particle_entry.example is not None
        )
    if t.related is not None:
        linked_words.extend(t.related)

    for sentence_with_at_words in sentences_with_at_words:
        matches = re.findall(at_word_capture_regex, sentence_with_at_words)
        linked_words.extend(matches)

    return linked_words
