from enum import Enum, auto

from src.linter import entry, rule_result
from src.linter.rules import (
    hash_brace_contents,
    head_word_hash_number,
    sense_is_int,
)


class T(Enum):
    HASH_BRACE_CONTENTS = auto()
    HEAD_WORD_HASH_NUMBER = auto()
    SENSE_IS_INT = auto()


def to_string(t: T) -> str:
    return t.name.lower().replace("_", " ")


ALL: list[T] = list(T)


def lint(t: T, entry: entry.T) -> rule_result.T:
    match t:
        case T.HASH_BRACE_CONTENTS:
            return hash_brace_contents.lint(entry)
        case T.HEAD_WORD_HASH_NUMBER:
            return head_word_hash_number.lint(entry)
        case T.SENSE_IS_INT:
            return sense_is_int.lint(entry)
