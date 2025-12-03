from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import no_todos

PURPOSELY_EMPTY = "empty for testing"


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(no_todos.lint(entry_))


def test_clean_entry_is_ok() -> None:
    entry_ = entry.create_for_testing()
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_todo_triggers_error() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [{"definition": "TODO undone"}],
        }
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """WARNING: found TODO in "TODO undone" -- this entry is unfinished.""",
    )


def test_todo_in_key_triggers_error() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "TODO undone": [{"definition": PURPOSELY_EMPTY}],
        }
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """WARNING: found TODO in "TODO undone" -- this entry is unfinished.""",
    )
