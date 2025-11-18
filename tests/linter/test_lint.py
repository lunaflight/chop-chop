from pathlib import Path

from expecttest import assert_expected_inline

from src.linter import entry, main, rule, rule_level


def lint_and_get_result(
    entries_and_file_names: list[tuple[entry.T, Path]],
    minimum_rule_level: rule_level.T,
    trieId_ignored_rule_codes_map: dict[str, list[rule.T]] | None,
    rules: list[rule.T],
) -> str:
    lint_result = main.lint(
        entries_and_file_names=entries_and_file_names,
        minimum_rule_level=minimum_rule_level,
        trieId_ignored_rule_codes_map=trieId_ignored_rule_codes_map,
        rules=rules,
    )

    return f"""\
output:
    {lint_result["output_strings"]}
has_error:
    {lint_result["has_error"]}"""


FAKE_PATH_FOR_PRINTING = Path("fake/path/to/word.json")
FIXED_TRIE_ID = "fixed trieId"
FIXED_SECOND_TRIE_ID = "fixed second trieId"


def append_fake_file_names(
    entries: list[entry.T],
) -> list[tuple[entry.T, Path]]:
    return [(entry_, FAKE_PATH_FOR_PRINTING) for entry_ in entries]


def test_good_entry_returns_all_ok() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing()]
        ),
        minimum_rule_level=rule_level.T.SUGGESTION,
        trieId_ignored_rule_codes_map={},
        rules=rule.ALL,
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    []
has_error:
    False""",
    )


def test_bad_entry_returns_error() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing(sense="non-number")]
        ),
        minimum_rule_level=rule_level.T.SUGGESTION,
        trieId_ignored_rule_codes_map={},
        rules=[rule.T.SENSE_IS_INT],
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    ['ERROR: Found "non-number", expecting number (rule "sense is int" [SII] in file "fake/path/to/word.json")']
has_error:
    True""",
    )


def test_ignoring_rule_for_bad_entry_is_ok() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing(trieId=FIXED_TRIE_ID, sense="non-number")]
        ),
        minimum_rule_level=rule_level.T.OK,
        trieId_ignored_rule_codes_map={FIXED_TRIE_ID: [rule.T.SENSE_IS_INT]},
        rules=[rule.T.SENSE_IS_INT],
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    []
has_error:
    False""",
    )


def test_ignoring_unrelated_details_for_bad_entry() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing(trieId=FIXED_TRIE_ID, sense="non-number")]
        ),
        minimum_rule_level=rule_level.T.OK,
        trieId_ignored_rule_codes_map={
            FIXED_TRIE_ID: [rule.T.SENSE_SHOULD_AGREE_WITH_TRIEID],
            FIXED_SECOND_TRIE_ID: [rule.T.SENSE_IS_INT],
        },
        rules=[rule.T.SENSE_IS_INT],
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    ['ERROR: Found "non-number", expecting number (rule "sense is int" [SII] in file "fake/path/to/word.json")']
has_error:
    True""",
    )
