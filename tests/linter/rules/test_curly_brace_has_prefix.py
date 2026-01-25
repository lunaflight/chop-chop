from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import curly_brace_has_prefix
from tests.linter.commons import IRRELEVANT


def lint_and_get_result(quoted_str: str | None = None) -> str:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [
                {
                    "definition": IRRELEVANT,
                    "example": [{"eg": quoted_str or ""}],
                }
            ]
        },
    )
    return rule_result.to_string(curly_brace_has_prefix.lint(entry_))


def test_has_at_sign() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_str="@{word}"),
        """OK""",
    )


def test_has_caret() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_str="Sentence.^{381}"),
        """OK""",
    )


def test_has_pound() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_str="#{likely}"),
        """OK""",
    )


def test_no_prefix() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_str="{word}"),
        """WARNING: Found "{word}", did you forget a leading "^" or "@"?""",
    )


def test_no_prefix_in_sentence() -> None:
    assert_expected_inline(
        lint_and_get_result(quoted_str="Sentence quoting {word}."),
        """WARNING: Found "{word}", did you forget a leading "^" or "@"?""",
    )
