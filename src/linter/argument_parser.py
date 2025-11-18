import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

import yaml

from src.linter import entry, rule, rule_level


@dataclass(frozen=True)
class Error:
    message: str


@dataclass
class ListAllRules:
    pass


@dataclass
class LintEntries(TypedDict):
    entries_and_file_names: list[tuple[entry.T, Path]]
    minimum_rule_level: rule_level.T
    trieId_ignored_rule_codes_map: dict[str, list[rule.T]] | None


def parse_arguments() -> Error | ListAllRules | LintEntries:
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

    if args.list:
        return ListAllRules()

    if not args.list and not args.json_file_paths:
        return Error(
            message=(
                "Error: When --list is not provided, "
                "at least one JSON file path is required."
            )
        )

    json_file_paths = [Path(file_path) for file_path in args.json_file_paths]
    entries_and_file_names: list[tuple[entry.T, Path]] = []

    for file_path in json_file_paths:
        with file_path.open(encoding="utf-8") as json_file:
            entry_ = entry.create_from_json_exn(json_file.read())
            entries_and_file_names.append((entry_, Path(file_path)))

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

    return LintEntries(
        entries_and_file_names=entries_and_file_names,
        minimum_rule_level=minimum_rule_level,
        trieId_ignored_rule_codes_map=trieId_ignored_rule_codes_map,
    )
