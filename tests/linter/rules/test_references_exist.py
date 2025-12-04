from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import references_exist
from tests.linter.commons import IRRELEVANT


def lint_and_get_result(references_quoted: int, references_sourced: int) -> str:
    usage = "".join(f"^{{{i}}}" for i in range(1, references_quoted + 1))
    references = [{"name": IRRELEVANT} for _ in range(references_sourced)]

    entry_ = entry.create_for_testing(usage=usage, references=references)

    return rule_result.to_string(references_exist.lint(entry_))


def test_equal_quoted_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(references_quoted=0, references_sourced=0), """OK"""
    )
    assert_expected_inline(
        lint_and_get_result(references_quoted=5, references_sourced=5), """OK"""
    )


# Test added to show behaviour, can be tweaked
def test_less_quoted_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(references_quoted=1, references_sourced=2), """OK"""
    )


def test_more_quoted_is_bad() -> None:
    assert_expected_inline(
        lint_and_get_result(references_quoted=2, references_sourced=1),
        """ERROR: The largest reference number found is 2 but insufficient references (1) exist.""",
    )
