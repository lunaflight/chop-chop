from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import hash_brace_contents


def lint_and_get_result(string: str) -> str:
    entry_ = entry.create_for_testing(etyNotes=string)
    return rule_result.to_string(hash_brace_contents.lint(entry_))


def test_none_quoted_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(string="None"),
        """OK""",
    )


def test_recognised_are_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(string="#{likely} #{poss} #{dubious} #{warn}"),
        """OK""",
    )


def test_empty_brace_is_bad() -> None:
    assert_expected_inline(
        lint_and_get_result(string="#{}"),
        """ERROR: Found "", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_bad_content() -> None:
    assert_expected_inline(
        lint_and_get_result(string="#{unknown word}"),
        """ERROR: Found "unknown word", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_bad_capitalisation() -> None:
    assert_expected_inline(
        lint_and_get_result(string="#{Likely}"),
        """ERROR: Found "Likely", hash braces only accept [likely, poss, dubious, warn]""",
    )
