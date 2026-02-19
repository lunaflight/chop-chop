from typing import Any

from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import linked_words_are_known
from tests.linter.commons import FIXED_WORD, IRRELEVANT, get_fixed_word

ANOTHER_FIXED_WORD = get_fixed_word(seed=1)


def lint_and_get_result(
    related_word: str | None = None,
    synonym: str | None = None,
    quoted_word: str | None = None,
    known_words: list[str] | None = None,
) -> str:
    kwargs: dict[str, Any] = {}

    if related_word is not None:
        kwargs["related"] = [related_word]

    if synonym is not None:
        kwargs["meanings"] = {
            "noun": [{"definition": IRRELEVANT, "synonyms": [synonym]}]
        }

    if quoted_word is not None:
        kwargs["usage"] = f"@{{{quoted_word}}}"

    entry_ = entry.create_for_testing(**kwargs)

    def is_known_word(word: str) -> bool:
        return word in (known_words or [])

    return rule_result.to_string(
        linked_words_are_known.lint(entry_, is_known_word)
    )


def test_related() -> None:
    assert_expected_inline(
        lint_and_get_result(related_word=FIXED_WORD, known_words=[FIXED_WORD]),
        """OK""",
    )
    assert_expected_inline(
        lint_and_get_result(related_word=FIXED_WORD, known_words=[]),
        """ERROR: Found "word", which does not link to a valid word.""",
    )


def test_synonyms() -> None:
    assert_expected_inline(
        lint_and_get_result(synonym=FIXED_WORD, known_words=[FIXED_WORD]),
        """OK""",
    )
    assert_expected_inline(
        lint_and_get_result(synonym=FIXED_WORD, known_words=[]),
        """ERROR: Found "word", which does not link to a valid word.""",
    )


def test_quoted() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_word=FIXED_WORD, known_words=[FIXED_WORD]),
        """OK""",
    )
    assert_expected_inline(
        lint_and_get_result(quoted_word=FIXED_WORD, known_words=[]),
        """ERROR: Found "word", which does not link to a valid word.""",
    )


def test_redirected_quote() -> None:
    assert_expected_inline(
        lint_and_get_result(
            quoted_word=f"{ANOTHER_FIXED_WORD}|{FIXED_WORD}",
            known_words=[ANOTHER_FIXED_WORD],
        ),
        """ERROR: Found "word", which does not link to a valid word.""",
    )
    assert_expected_inline(
        lint_and_get_result(
            quoted_word=f"{ANOTHER_FIXED_WORD}|{FIXED_WORD}",
            known_words=[FIXED_WORD],
        ),
        """OK""",
    )
