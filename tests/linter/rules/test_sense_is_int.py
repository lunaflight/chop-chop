from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import sense_is_int


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(sense_is_int.lint(entry_))


def test_ok() -> None:
    entry_ = entry.create_for_testing(sense="0")
    assert_expected_inline(lint_and_get_result(entry_), """OK""")
    entry_ = entry.create_for_testing(sense="1")
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_negative() -> None:
    entry_ = entry.create_for_testing(sense="-1")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "-1", expecting non-negative integer""",
    )


def test_non_int() -> None:
    entry_ = entry.create_for_testing(sense="string")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "string", expecting number""",
    )
