import argparse
import sys
from itertools import product
from pathlib import Path
from typing import TypedDict

import yaml

from src.linter import entry, rule, rule_format, rule_level, rule_result


def get_entries_and_file_names(
    json_file_paths: list[Path],
) -> list[tuple[entry.T, Path]]:
    entries_and_file_names: list[tuple[entry.T, Path]] = []

    for file_path in json_file_paths:
        with file_path.open(encoding="utf-8") as json_file:
            entry_ = entry.create_from_json_exn(json_file.read())
            entries_and_file_names.append((entry_, Path(file_path)))

    return entries_and_file_names


class LintResult(TypedDict):
    output_strings: list[str]
    has_error: bool


# TODO: Make [entries_and_file_names] not take a Path so this can be tested
def lint_against_all_rules(
    entries_and_file_names: list[tuple[entry.T, Path]],
    minimum_rule_level: rule_level.T,
    trieId_ignored_rule_codes_map: dict[str, list[rule.T]] | None,
) -> LintResult:
    output_strings: list[str] = []
    has_error = False

    for (entry_, file_path), rule_ in product(entries_and_file_names, rule.ALL):
        trieId = entry_["trieId"]
        if (
            trieId_ignored_rule_codes_map is not None
            and trieId in trieId_ignored_rule_codes_map
            and rule_ in trieId_ignored_rule_codes_map[trieId]
        ):
            continue

        rule_result_ = rule.lint(rule_, entry_)
        rule_level_ = rule_result.get_level(rule_result_)

        is_severe_enough_to_log = rule_level.greater_than_or_equal_to(
            rule_level_, minimum_rule_level
        )

        if is_severe_enough_to_log:
            output = rule_format.for_stdout(rule_, rule_result_, file_path)
            output_strings.append(output)

        if is_severe_enough_to_log and rule_level_ is not rule_level.T.OK:
            has_error = True

    return LintResult(output_strings=output_strings, has_error=has_error)


def print_all_rules() -> None:
    for rule_ in rule.ALL:
        print(f"{rule.to_string(rule_)}[{rule.to_code(rule_)}]")  # noqa: T201
        print(f"    {rule.description(rule_)}")  # noqa: T201


def main() -> None:
    # TODO: This argument parser is getting ungodly and should be in its own
    # file.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "json_file_paths", nargs="*", type=str, help="Paths to the JSON files"
    )
    parser.add_argument(
        "--rule-level",
        type=str,
        choices=["all", "suggestion", "warning", "error"],
        default="suggestion",
        help=(
            "Display rules greater than or equal to the given rule level "
            "in terms of severity"
        ),
    )
    parser.add_argument(
        "--ignore-yaml",
        type=str,
        default=None,
        help="Path to an optional yaml file containing rules to ignore.",
    )
    parser.add_argument(
        "--list", action="store_true", help="List all rules and descriptions"
    )

    args = parser.parse_args()

    if not args.list and not args.json_file_paths:
        print(  # noqa: T201
            (
                "Error: When --list is not provided, "
                "at least one JSON file path is required."
            ),
            file=sys.stderr,
        )
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    rule_level_map = {
        "all": rule_level.T.OK,
        "suggestion": rule_level.T.SUGGESTION,
        "warning": rule_level.T.WARNING,
        "error": rule_level.T.ERROR,
    }
    minimum_rule_level = rule_level_map[args.rule_level]

    if args.ignore_yaml:
        with Path(args.ignore_yaml).open(encoding="utf-8") as f:
            ignored_rules_data = yaml.safe_load(f)

        trieId_ignored_rule_codes_map = {
            trie_id: [rule.of_code(code) for code in code_list]
            for trie_id, code_list in ignored_rules_data.items()
        }
    else:
        trieId_ignored_rule_codes_map = None

    if args.list:
        print_all_rules()
        sys.exit(0)

    entries_and_file_names = get_entries_and_file_names(
        [Path(file_path) for file_path in args.json_file_paths]
    )
    lint_result = lint_against_all_rules(
        entries_and_file_names,
        minimum_rule_level,
        trieId_ignored_rule_codes_map,
    )
    for output in lint_result["output_strings"]:
        print(output)  # noqa: T201

    sys.exit(1 if lint_result["has_error"] else 0)


if __name__ == "__main__":
    main()
