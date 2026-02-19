from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import origlink_has_no_plus


def lint_and_get_result(origlink: list[str]) -> str:
    entry_ = entry.create_for_testing(origlink=origlink)
    return rule_result.to_string(origlink_has_no_plus.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(origlink=["", "or", "&"]),
        """OK""",
    )


def test_contains_plus() -> None:
    assert_expected_inline(
        lint_and_get_result(origlink=["+"]),
        """WARNING: Found + in [origlink], consider using an empty string so it is rendered without an underline.""",
    )
