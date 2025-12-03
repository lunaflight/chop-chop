from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import attestations_contain_word


def lint_and_get_result(
    word: str, alternate_form: str | None, sentence: str
) -> str:
    entry_ = entry.create_for_testing(
        word=word,
        formsClean=[alternate_form] if alternate_form else [],
        meanings={"noun": [{"definition": "", "example": [{"eg": sentence}]}]},
    )
    return rule_result.to_string(attestations_contain_word.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(word="word", alternate_form=None, sentence="word"),
        """OK""",
    )


def test_substring_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(word="word", alternate_form=None, sentence="words"),
        """OK""",
    )


def test_case_insensitive() -> None:
    assert_expected_inline(
        lint_and_get_result(word="word", alternate_form=None, sentence="WORD"),
        """OK""",
    )


def test_alternate_form_in_sentence() -> None:
    assert_expected_inline(
        lint_and_get_result(
            word="word", alternate_form="another form", sentence="another form"
        ),
        """OK""",
    )


# This may or may not be wanted and is added only to demonstrate behaviour.
def test_punctuation_separated_word() -> None:
    assert_expected_inline(
        lint_and_get_result(
            word="a, b", alternate_form="another form", sentence="a b"
        ),
        """SUGGESTION: Found "a b", which does not contain "a, b". Did you forget to add it?""",
    )


# This may or may not be wanted and is added only to demonstrate behaviour.
def test_punctuation_separated_sentence() -> None:
    assert_expected_inline(
        lint_and_get_result(
            word="a b", alternate_form="another form", sentence="a, b"
        ),
        """SUGGESTION: Found "a, b", which does not contain "a b". Did you forget to add it?""",
    )


def test_does_not_contain_word() -> None:
    assert_expected_inline(
        lint_and_get_result(word="word", alternate_form=None, sentence=""),
        """SUGGESTION: Found "", which does not contain "word". Did you forget to add it?""",
    )
