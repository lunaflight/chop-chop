import json
from typing import Any, TypedDict


# TODO: These fields may be empty -- this is well-defined behaviour and
# should be supported
class T(TypedDict):
    word: str
    trieId: str
    sense: str
    etyNotes: str
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
        category=dict_["category"],
    )


def create_for_testing(**kwargs: Any) -> T:  # noqa: ANN401
    default_data = {
        "word": "Test Word",
        "trieId": "test word",
        "sense": "0",
        "etyNotes": "Etymology notes.",
        "category": [],
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
