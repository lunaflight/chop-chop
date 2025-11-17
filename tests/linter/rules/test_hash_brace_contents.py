from expecttest import assert_expected_inline

from src.linter import entry, rule_result
from src.linter.rules import hash_brace_contents


def lint_and_get_result(entry_: entry.T) -> str:
    return rule_result.to_string(hash_brace_contents.lint(entry_))


def test_ok() -> None:
    good_etyNotes_list = [
        "None.",
        "#{likely}",
        "#{poss}",
        "#{dubious}",
        "#{warn}",
    ]

    result = ", ".join(
        lint_and_get_result(entry.create_for_testing(etyNotes=etyNotes))
        for etyNotes in good_etyNotes_list
    )
    assert_expected_inline(
        result,
        """OK, OK, OK, OK, OK""",
    )


def test_multiple_braces() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="Using multiple markers are okay! #{warn} #{dubious} #{poss} #{likely}"
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """OK""",
    )


def test_empty_brace() -> None:
    entry_ = entry.create_for_testing(etyNotes="#{}")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_bad_content() -> None:
    entry_ = entry.create_for_testing(etyNotes="#{unknown word}")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "unknown word", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_weird_capitalisation() -> None:
    entry_ = entry.create_for_testing(etyNotes="#{Likely}")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "Likely", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_bad_content_in_multiple() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="#{warn} #{warn} #{warn} #{unknown word}"
    )
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "unknown word", hash braces only accept [likely, poss, dubious, warn]""",
    )


def test_detected_in_usage_notes() -> None:
    entry_ = entry.create_for_testing(usage="#{unknown word}")
    assert_expected_inline(
        lint_and_get_result(entry_),
        """ERROR: Found "unknown word", hash braces only accept [likely, poss, dubious, warn]""",
    )
