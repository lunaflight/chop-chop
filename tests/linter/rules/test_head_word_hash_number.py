from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import head_word_hash_number


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(head_word_hash_number.lint(entry_))


def test_ok() -> None:
    entry_ = entry.create_for_testing(word="Normal Word")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """OK""",
    )


def test_bad() -> None:
    entry_ = entry.create_for_testing(word="Normal Word#2147483647")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: You likely mistook "word" for the "trieId" since it ends in "#2147483647\"""",
    )
