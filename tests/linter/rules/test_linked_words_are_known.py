from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import linked_words_are_known


def lint_and_get_result(entry_: entry.T, known_words: list[str]) -> str:
    def is_known_word(word: str) -> bool:
        return word in known_words

    return rule_result.to_string(
        linked_words_are_known.lint(entry_, is_known_word)
    )


def test_related() -> None:
    entry_ = entry.create_for_testing(related=["some word"])
    known_words = ["some word"]
    assert_expected_inline(lint_and_get_result(entry_, known_words), """OK""")
    known_words = []
    assert_expected_inline(
        lint_and_get_result(entry_, known_words),
        """ERROR: Found "some word", which does not link to a valid word.""",
    )


def test_synonyms() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [{"definition": "definition", "synonyms": ["some word"]}]
        }
    )
    known_words = ["some word"]
    assert_expected_inline(lint_and_get_result(entry_, known_words), """OK""")
    known_words = []
    assert_expected_inline(
        lint_and_get_result(entry_, known_words),
        """ERROR: Found "some word", which does not link to a valid word.""",
    )


def test_quoted() -> None:
    entry_ = entry.create_for_testing(
        meanings={
            "noun": [
                {
                    "definition": "definition",
                    "example": [{"eg": "@{some word}"}],
                }
            ]
        }
    )
    known_words = ["some word"]
    assert_expected_inline(lint_and_get_result(entry_, known_words), """OK""")
    known_words = []
    assert_expected_inline(
        lint_and_get_result(entry_, known_words),
        """ERROR: Found "some word", which does not link to a valid word.""",
    )
