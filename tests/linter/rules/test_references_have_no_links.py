from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import references_have_no_links


def lint_and_get_result(reference_name: str) -> str:
    entry_ = entry.create_for_testing(references=[{"name": reference_name}])

    return rule_result.to_string(references_have_no_links.lint(entry_))


def test_no_http_link() -> None:
    assert_expected_inline(
        lint_and_get_result(reference_name="no https link"), """OK"""
    )


def test_has_https_link() -> None:
    assert_expected_inline(
        lint_and_get_result(reference_name="https://www.google.com"),
        """WARNING: Found "https://www.google.com" in references, the [link] field should be used to provide a HTTPS link""",
    )


def test_has_http_link() -> None:
    assert_expected_inline(
        lint_and_get_result(reference_name="http://www.google.com"),
        """WARNING: Found "http://www.google.com" in references, the [link] field should be used to provide a HTTPS link""",
    )
