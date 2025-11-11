import json
from dataclasses import dataclass


@dataclass
class T:
    post: str
    credit: str


def create(post: str, credit: str) -> T:
    return T(post=post, credit=credit)


def to_json(t: T) -> str:
    return json.dumps(t.__dict__, indent=4)
