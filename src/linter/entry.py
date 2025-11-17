import json
from typing import Any, TypedDict


class T(TypedDict):
    word: str
    trieId: str
    sense: str
    etyNotes: str


def create_exn(dict_: dict[str, Any]) -> T:
    for field, expected_type in T.__annotations__.items():
        if field not in dict_:
            msg = f"Missing field in JSON data: '{field}'"
            raise KeyError(msg)
        if not isinstance(dict_[field], expected_type):
            msg = f"Field '{field}' must be of type {expected_type.__name__}."
            raise TypeError(msg)

    return T(
        word=dict_["word"],
        trieId=dict_["trieId"],
        sense=dict_["sense"],
        etyNotes=dict_["etyNotes"],
    )


def create_for_testing(**kwargs: str) -> T:
    default_data = {
        "word": "Test Word",
        "trieId": "test word",
        "sense": "0",
        "etyNotes": "Etymology notes.",
    }
    default_data.update(kwargs)
    return create_exn(default_data)


def create_from_json_exn(json_data: str) -> T:
    json_dict = json.loads(json_data)
    return create_exn(json_dict)


# The below function only shallowly checks string types, i.e. arr[str] does
# not count, even though it should.
def all_strings(t: T) -> list[str]:
    return [value for key, value in t.items() if isinstance(value, str)]
