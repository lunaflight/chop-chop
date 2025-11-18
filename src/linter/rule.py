from enum import Enum

from src.linter import entry, rule_result
from src.linter.rules import (
    hash_brace_contents,
    head_word_hash_number,
    no_repeat_definitions,
    quotation_brace_has_caret,
    sense_is_int,
    sense_should_agree_with_trieId,
)


class T(Enum):
    HASH_BRACE_CONTENTS = "HBC"
    HEAD_WORD_HASH_NUMBER = "HWH"
    NO_REPEAT_DEFINITIONS = "NRD"
    SENSE_IS_INT = "SII"
    SENSE_SHOULD_AGREE_WITH_TRIEID = "SSA"
    QUOTATION_BRACE_HAS_CARET = "QBH"


def to_string(t: T) -> str:
    return t.name.lower().replace("_", " ")


def to_code(t: T) -> str:
    return t.value


def of_code(code: str) -> T:
    for member in T:
        if member.value.lower() == code.lower():
            return member

    msg = f"'{code}' is not a valid code for enum T."
    raise ValueError(msg)


def description(t: T) -> str:
    match t:
        case T.HASH_BRACE_CONTENTS:
            return hash_brace_contents.description()
        case T.HEAD_WORD_HASH_NUMBER:
            return head_word_hash_number.description()
        case T.NO_REPEAT_DEFINITIONS:
            return no_repeat_definitions.description()
        case T.QUOTATION_BRACE_HAS_CARET:
            return quotation_brace_has_caret.description()
        case T.SENSE_IS_INT:
            return sense_is_int.description()
        case T.SENSE_SHOULD_AGREE_WITH_TRIEID:
            return sense_should_agree_with_trieId.description()


ALL: list[T] = list(T)


def lint(t: T, entry: entry.T) -> rule_result.T:
    match t:
        case T.HASH_BRACE_CONTENTS:
            return hash_brace_contents.lint(entry)
        case T.HEAD_WORD_HASH_NUMBER:
            return head_word_hash_number.lint(entry)
        case T.NO_REPEAT_DEFINITIONS:
            return no_repeat_definitions.lint(entry)
        case T.QUOTATION_BRACE_HAS_CARET:
            return quotation_brace_has_caret.lint(entry)
        case T.SENSE_IS_INT:
            return sense_is_int.lint(entry)
        case T.SENSE_SHOULD_AGREE_WITH_TRIEID:
            return sense_should_agree_with_trieId.lint(entry)
