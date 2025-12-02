from expecttest import assert_expected_inline

from src.linter import rule_result
from src.linter.json import entry
from src.linter.rules import category_is_known


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(category_is_known.lint(entry_))


def test_ok() -> None:
    entry_ = entry.create_for_testing(category=["cuisine", "locations", "ns"])
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_empty_is_ok() -> None:
    entry_ = entry.create_for_testing(category=[])
    assert_expected_inline(lint_and_get_result(entry_), """OK""")


def test_unknown_category() -> None:
    entry_ = entry.create_for_testing(category=["unknown"])
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "unknown", known categories are [abbreviations, brands & companies, childish, conserved english, cuisine, cultural, drinks, education, games, insults, kueh, locations, meme-derived, nature, ns, online slang, onomatopoeia, particles, rhyming slang, sayings, snowclones, terms of address, units of measure, vulgar]""",
    )
