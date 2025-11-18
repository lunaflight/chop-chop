import json
from typing import Any, TypedDict


class Attestation(TypedDict):
    eg: str
    src: str


class DefinitionEntry(TypedDict):
    definition: str
    example: list[Attestation]
    synonyms: list[str]
    antonyms: list[str]


PartOfSpeech = list[DefinitionEntry]


# TODO: These fields may be empty -- this is well-defined behaviour and
# should be supported
class T(TypedDict):
    word: str
    trieId: str
    sense: str
    etyNotes: str
    meanings: dict[str, PartOfSpeech]
    usage: str
    category: list[str]


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
    return [t["etyNotes"], t["usage"]]
