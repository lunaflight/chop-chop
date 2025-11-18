import json
from typing import Any, TypedDict


class Attestation(TypedDict):
    eg: str
    src: str | None


class DefinitionEntry(TypedDict):
    definition: str
    example: list[Attestation] | None
    synonyms: list[str] | None
    antonyms: list[str] | None


PartOfSpeech = list[DefinitionEntry]


class T(TypedDict):
    word: str
    trieId: str
    sense: str
    etyNotes: str | None
    meanings: dict[str, PartOfSpeech]
    usage: str | None
    category: list[str] | None


def create_exn(dict_: dict[str, Any]) -> T:
    for field in T.__annotations__:
        if field not in dict_:
            msg = f"Missing field in JSON data: '{field}'"
            raise KeyError(msg)

    return T(
        word=dict_["word"],
        trieId=dict_["trieId"],
        sense=dict_["sense"],
        etyNotes=dict_["etyNotes"],
        meanings=dict_["meanings"],
        usage=dict_["usage"],
        category=dict_["category"],
    )


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
    return create_exn(default_data)


def create_from_json_exn(json_data: str) -> T:
    json_dict = json.loads(json_data)
    return create_exn(json_dict)


def self_written_sentences(t: T) -> list[str]:
    self_written_sentences = []

    if t["etyNotes"] is not None:
        self_written_sentences.append(t["etyNotes"])
    if t["usage"] is not None:
        self_written_sentences.append(t["usage"])
    for part_of_speech in t["meanings"].values():
        self_written_sentences.extend(
            definition_entry["definition"]
            for definition_entry in part_of_speech
        )

    return self_written_sentences
