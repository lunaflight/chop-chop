from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import quotation_brace_has_caret


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(quotation_brace_has_caret.lint(entry_))


def test_ok() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="Quoting correctly.^{1} This should not be punished,^{2} "
        "as an example!^{2147483647}"
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """OK""",
    )


def test_hyperlinks_are_ok() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="@{96} people normally do not sign @{1206}."
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """OK""",
    )


def test_after_space_is_ok() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="Quoting a mathematical construct like {2147483643}."
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """OK""",
    )


def test_missing_caret() -> None:
    entry_ = entry.create_for_testing(etyNotes="Genuine mistake.{1}")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """WARNING: Found "{1}", did you forget a "^" for a citation?""",
    )
