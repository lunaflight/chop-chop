from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import no_repeat_definitions


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(no_repeat_definitions.lint(entry_))


def test_same_definition_across_different_part_of_speech_is_ok() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [{"definition": "the same definition"}],
            "verb": [{"definition": "the same definition"}],
        }
    )
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_same_definition_in_same_part_of_speech_is_bad() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [
                {"definition": "the same definition"},
                {"definition": "the same definition"},
            ],
        }
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found repeat definition: the same definition""",
    )
