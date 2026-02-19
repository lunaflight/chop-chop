from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import sense_is_int


def lint_and_get_result(sense: int | str) -> str:
    sense = str(sense)
    entry_ = entry.create_for_testing(sense=sense)
    return rule_result.to_string(sense_is_int.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(lint_and_get_result(sense=0), """OK""")
    assert_expected_inline(lint_and_get_result(sense=1), """OK""")


def test_negative() -> None:
    assert_expected_inline(
        lint_and_get_result(sense=-1),
        """ERROR: Found "-1", expecting non-negative integer""",
    )


def test_non_int() -> None:
    assert_expected_inline(
        lint_and_get_result(sense="string"),
        """ERROR: Found "string", expecting number""",
    )
