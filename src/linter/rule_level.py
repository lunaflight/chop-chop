from enum import Enum


class T(Enum):
    OK = 0
    SUGGESTION = 1
    WARNING = 2
    ERROR = 3


def to_string(t: T) -> str:
    return t.name


def greater_than_or_equal_to(src: T, target: T) -> bool:
    return src.value >= target.value
