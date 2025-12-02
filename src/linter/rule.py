from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import (
    hash_brace_contents,
    head_word_hash_number,
    linked_words_are_known,
    no_repeat_definitions,
    quotation_brace_has_caret,
    sense_is_int,
    sense_should_agree_with_trieId,
)


class T(Enum):
    HASH_BRACE_CONTENTS = "HBC"
    HEAD_WORD_HASH_NUMBER = "HWH"
    LINKED_WORDS_ARE_KNOWN = "LWA"
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


def description(t: T) -> str:  # noqa: PLR0911
    match t:
        case T.HASH_BRACE_CONTENTS:
            return hash_brace_contents.description()
        case T.HEAD_WORD_HASH_NUMBER:
            return head_word_hash_number.description()
        case T.LINKED_WORDS_ARE_KNOWN:
            return linked_words_are_known.description()
        case T.NO_REPEAT_DEFINITIONS:
            return no_repeat_definitions.description()
        case T.QUOTATION_BRACE_HAS_CARET:
            return quotation_brace_has_caret.description()
        case T.SENSE_IS_INT:
            return sense_is_int.description()
        case T.SENSE_SHOULD_AGREE_WITH_TRIEID:
            return sense_should_agree_with_trieId.description()


ALL: list[T] = list(T)


@dataclass
class LintRunError:
    message: str


def lint(  # noqa: PLR0911
    t: T, entry_: entry.T, is_known_word: Callable[[str], bool] | None
) -> rule_result.T | LintRunError:
    match t:
        case T.HASH_BRACE_CONTENTS:
            return hash_brace_contents.lint(entry_)
        case T.HEAD_WORD_HASH_NUMBER:
            return head_word_hash_number.lint(entry_)
        case T.LINKED_WORDS_ARE_KNOWN:
            if is_known_word is None:
                return LintRunError(
                    "missing [is_known_word]; unable to run "
                    f'"{to_string(t)}" against "{entry_.trieId}"'
                )

            return linked_words_are_known.lint(entry_, is_known_word)
        case T.NO_REPEAT_DEFINITIONS:
            return no_repeat_definitions.lint(entry_)
        case T.QUOTATION_BRACE_HAS_CARET:
            return quotation_brace_has_caret.lint(entry_)
        case T.SENSE_IS_INT:
            return sense_is_int.lint(entry_)
        case T.SENSE_SHOULD_AGREE_WITH_TRIEID:
            return sense_should_agree_with_trieId.lint(entry_)
