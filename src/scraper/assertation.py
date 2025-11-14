import json
from dataclasses import dataclass

from src import sanitizer


@dataclass
class T:
    post: str
    credit: str


def create(post: str, credit: str) -> T:
    return T(
        post=sanitizer.clean_unicode_for_output(post),
        credit=sanitizer.clean_unicode_for_output(credit),
    )


def to_json(t: T) -> str:
    return json.dumps(t.__dict__, indent=4)
