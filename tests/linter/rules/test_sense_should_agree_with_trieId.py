from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import sense_should_agree_with_trieId


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(sense_should_agree_with_trieId.lint(entry_))


def test_ok() -> None:
    entry_ = entry.create_for_testing(sense="0", trieId="word")
    assert_expected_inline(lint_and_get_result(entry_), """OK""")
    entry_ = entry.create_for_testing(sense="1", trieId="word#1")
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_missing_hash() -> None:
    entry_ = entry.create_for_testing(sense="1", trieId="word")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Expected '#' in trieId because sense is not 0.""",
    )


def test_does_not_agree() -> None:
    entry_ = entry.create_for_testing(sense="1", trieId="word#2")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Expected sense '1' and trieId 'word#2' to match because sense is not 0.""",
    )
    entry_ = entry.create_for_testing(sense="0", trieId="word#2")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Expected sense '0' and trieId 'word#2' to match because sense is not 0.""",
    )
