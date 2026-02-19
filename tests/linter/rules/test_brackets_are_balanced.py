from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import brackets_are_balanced


def lint_and_get_result(string: str) -> str:
    entry_ = entry.create_for_testing(etyNotes=string)
    return rule_result.to_string(brackets_are_balanced.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(string="([]{[]})"),
        """OK""",
    )


def test_blank_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(string=""),
        """OK""",
    )


def test_starts_in_smiley() -> None:
    assert_expected_inline(
        lint_and_get_result(string="(: my sentence"),
        """OK""",
    )


def test_ends_in_smiley() -> None:
    assert_expected_inline(
        lint_and_get_result(string="my sentence :)"),
        """OK""",
    )


def test_ends_in_smiley_and_quote() -> None:
    assert_expected_inline(
        lint_and_get_result(string='"quoted my sentence :)"'),
        """OK""",
    )


def test_fake_smiley() -> None:
    assert_expected_inline(
        lint_and_get_result(string="they (plural);"),
        """OK""",
    )


def test_unclosed_bracket_sequence() -> None:
    assert_expected_inline(
        lint_and_get_result(string="("),
        """WARNING: The string "(" does not have a balanced bracket sequence.""",
    )


def test_unopened_bracket_sequence() -> None:
    assert_expected_inline(
        lint_and_get_result(string=")"),
        """WARNING: The string ")" does not have a balanced bracket sequence.""",
    )


def test_unmatched_bracket_sequence() -> None:
    assert_expected_inline(
        lint_and_get_result(string="[}"),
        """WARNING: The string "[}" does not have a balanced bracket sequence.""",
    )
