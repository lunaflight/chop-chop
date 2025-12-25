from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import ety_lengths_equal


def lint_and_get_result(
    etyPath_len: int, etyRoman_len: int, etyLit_len: int
) -> str:
    entry_ = entry.create_for_testing(
        origin=[
            {
                "etyPath": [str(n) for n in range(etyPath_len)],
                "etyRoman": [str(n) for n in range(etyRoman_len)],
                "etyLit": [str(n) for n in range(etyLit_len)],
            }
        ]
    )
    return rule_result.to_string(ety_lengths_equal.lint(entry_))


def test_all_equal_lengths_is_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(etyPath_len=2, etyRoman_len=2, etyLit_len=2),
        """OK""",
    )


def test_etyRoman_different_length() -> None:
    assert_expected_inline(
        lint_and_get_result(etyPath_len=2, etyRoman_len=1, etyLit_len=2),
        """ERROR: Found mismatched lengths in the etymology of 0: etyPath (length: 2), etyRoman (length: 1), etyLit (length: 2)""",
    )


def test_etyPath_different_length() -> None:
    assert_expected_inline(
        lint_and_get_result(etyPath_len=1, etyRoman_len=2, etyLit_len=2),
        """ERROR: Found mismatched lengths in the etymology of 0: etyPath (length: 1), etyRoman (length: 2), etyLit (length: 2)""",
    )


def test_etyLit_different_length() -> None:
    assert_expected_inline(
        lint_and_get_result(etyPath_len=2, etyRoman_len=2, etyLit_len=1),
        """ERROR: Found mismatched lengths in the etymology of 0: etyPath (length: 2), etyRoman (length: 2), etyLit (length: 1)""",
    )
