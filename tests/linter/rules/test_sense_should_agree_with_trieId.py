from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import sense_should_agree_with_trieId

FIXED_WORD = "word"


def lint_and_get_result(
    sense: int | str, trieId_suffix: int | str | None
) -> str:
    sense = str(sense)
    trieId_suffix = f"#{trieId_suffix!s}" if trieId_suffix else ""

    entry_ = entry.create_for_testing(
        sense=sense, trieId=f"{FIXED_WORD}{trieId_suffix}"
    )
    return rule_result.to_string(sense_should_agree_with_trieId.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(sense=0, trieId_suffix=None), """OK"""
    )
    assert_expected_inline(
        lint_and_get_result(sense=1, trieId_suffix=1),
        """OK""",
    )


def test_sense_0_cannot_accept_suffixes() -> None:
    assert_expected_inline(
        lint_and_get_result(sense=0, trieId_suffix=0), """OK"""
    )


def test_sense_non_0_must_have_suffix() -> None:
    assert_expected_inline(
        lint_and_get_result(sense=1, trieId_suffix=None),
        """ERROR: Expected '#' in trieId because sense is not 0.""",
    )


def test_senses_disagree() -> None:
    assert_expected_inline(
        lint_and_get_result(sense=1, trieId_suffix=2),
        """ERROR: Expected sense '1' and trieId 'word#2' to match because sense is not 0.""",
    )
