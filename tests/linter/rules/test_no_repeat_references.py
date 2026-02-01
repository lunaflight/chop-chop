from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import no_repeat_references
from tests.linter.commons import IRRELEVANT


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(no_repeat_references.lint(entry_))


def test_no_references_ok() -> None:
    entry_ = entry.create_for_testing(references=None)
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_different_references_ok() -> None:
    entry_ = entry.create_for_testing(
        references=[
            {"name": "name 1", "link": "https://link.one"},
            {"name": "name 2", "link": "https://link.two"},
        ]
    )
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_same_name() -> None:
    entry_ = entry.create_for_testing(
        references=[
            {"name": IRRELEVANT, "link": "https://link.one"},
            {"name": IRRELEVANT, "link": "https://link.two"},
        ]
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found repeat reference name: empty for testing""",
    )


def test_same_link() -> None:
    entry_ = entry.create_for_testing(
        references=[
            {"name": "name 1", "link": IRRELEVANT},
            {"name": "name 1", "link": IRRELEVANT},
        ]
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found repeat reference name: name 1""",
    )
