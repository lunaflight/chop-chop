from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import head_word_hash_number


def lint_and_get_result(word: str) -> str:
    entry_ = entry.create_for_testing(word=word)
    return rule_result.to_string(head_word_hash_number.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(word="Normal Word"),
        """OK""",
    )


def test_bad() -> None:
    assert_expected_inline(
        lint_and_get_result(word="Normal Word#2147483647"),
        """ERROR: You likely mistook "word" for the "trieId" since it ends in "#2147483647\"""",
    )
