from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import category_is_known


def lint_and_get_result(categories: list[str]) -> str:
    entry_ = entry.create_for_testing(category=categories)
    return rule_result.to_string(category_is_known.lint(entry_))


def test_ok() -> None:
    assert_expected_inline(
        lint_and_get_result(categories=["cuisine", "locations", "ns"]), """OK"""
    )


def test_not_case_sensitive() -> None:
    assert_expected_inline(lint_and_get_result(categories=["Ns"]), """OK""")


def test_empty_is_ok() -> None:
    assert_expected_inline(lint_and_get_result(categories=[]), """OK""")


def test_unknown_category() -> None:
    assert_expected_inline(
        lint_and_get_result(categories=["unknown"]),
        """ERROR: Found "unknown", known categories are [abbreviations, brands & companies, childish, conserved english, cuisine, cultural, drinks, education, games, healthcare, insults, kueh, lgbtq+, locations, meme-derived, nature, ns, online slang, onomatopoeia, particles, politics, rhyming slang, sayings, snowclones, terms of address, units of measure, vulgar]""",
    )
