from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import quotation_brace_has_caret


def lint_and_get_result(string: str) -> str:
    entry_ = entry.create_for_testing(etyNotes=string)
    return rule_result.to_string(quotation_brace_has_caret.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(
            string="Correct.^{1} Also correct,^{2} Also correct!^{2147483647}"
        ),
        """OK""",
    )


def test_hyperlinks_are_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(
            string="@{96} people normally do not sign @{1206}."
        ),
        """OK""",
    )


def test_after_space_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(
            string="Quoting a mathematical construct like {2147483643}."
        ),
        """OK""",
    )


def test_missing_caret() -> None:
    assert_expected_inline(
        lint_and_get_result(string="Genuine mistake.{1}"),
        """WARNING: Found "{1}", did you forget a "^" for a citation?""",
    )
