from enum import Enum, auto

from src.linter import entry, rule_result
from src.linter.rules import sense_is_int


class T(Enum):
    SENSE_IS_INT = auto()


def to_string(t: T) -> str:
    return t.name.lower().replace("_", " ")


ALL: list[T] = list(T)


def lint(t: T, entry: entry.T) -> rule_result.T:
    match t:
        case T.SENSE_IS_INT:
            return sense_is_int.lint(entry)
