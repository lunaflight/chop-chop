from pathlib import Path

from expecttest import assert_expected_inline

from src.linter import ignored_rules_map, main, rule, rule_level
from src.linter.json import entry


def lint_and_get_result(
    entries_and_file_names: list[tuple[entry.T, Path]],
    minimum_rule_level: rule_level.T,
    ignored_rules_dict: dict[str, list[rule.T]] | None,
    rules: list[rule.T],
) -> str:
    lint_result = main.lint(
        entries_and_file_names=entries_and_file_names,
        is_known_word=None,
        minimum_rule_level=minimum_rule_level,
        trieId_ignored_rule_codes_map=ignored_rules_map.create_from_dict(
            ignored_rules_dict
        )
        if ignored_rules_dict is not None
        else None,
        rules=rules,
    )

    return f"""\
output:
    {lint_result["output_strings"]}
has_error:
    {lint_result["has_error"]}"""


# Adding [/]s to the path will make the Windows CI fail since both platforms
# expect something different: Linux wants /; Windows wants \\. The [expecttest]
# setup will then need to be reconsidered.
# Since this is not an important detail, a simple filename will suffice.
FAKE_PATH_FOR_PRINTING = Path("word.json")
FIXED_TRIE_ID = "fixed trieId"
FIXED_SECOND_TRIE_ID = "fixed second trieId"
ALL = ignored_rules_map.ALL_RESERVED_WORD


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
        ignored_rules_dict={},
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
        ignored_rules_dict={},
        rules=[rule.T.SENSE_IS_INT],
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    ['ERROR: Found "non-number", expecting number (rule "sense is int" [SII] in file "word.json")']
has_error:
    True""",
    )


def test_ignoring_rule_for_bad_entry_is_ok() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing(trieId=FIXED_TRIE_ID, sense="non-number")]
        ),
        minimum_rule_level=rule_level.T.OK,
        ignored_rules_dict={FIXED_TRIE_ID: [rule.T.SENSE_IS_INT]},
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


def test_ignoring_all_for_bad_entry_is_ok() -> None:
    lint_result_str = lint_and_get_result(
        entries_and_file_names=append_fake_file_names(
            [entry.create_for_testing(trieId=FIXED_TRIE_ID, sense="non-number")]
        ),
        minimum_rule_level=rule_level.T.OK,
        ignored_rules_dict={ALL: [rule.T.SENSE_IS_INT]},
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
        ignored_rules_dict={
            FIXED_TRIE_ID: [rule.T.SENSE_SHOULD_AGREE_WITH_TRIEID],
            FIXED_SECOND_TRIE_ID: [rule.T.SENSE_IS_INT],
        },
        rules=[rule.T.SENSE_IS_INT],
    )
    assert_expected_inline(
        lint_result_str,
        """\
output:
    ['ERROR: Found "non-number", expecting number (rule "sense is int" [SII] in file "word.json")']
has_error:
    True""",
    )
