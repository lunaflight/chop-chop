import argparse
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from pydantic import ValidationError

from src.linter import entry, ignored_rules_map, rule_level


@dataclass(frozen=True)
class Error:
    message: str


@dataclass
class ListAllRules:
    pass


@dataclass
class LintEntries(TypedDict):
    entries_and_file_names: list[tuple[entry.T, Path]]
    is_known_word: Callable[[str], bool] | None
    minimum_rule_level: rule_level.T
    trieId_ignored_rule_codes_map: ignored_rules_map.T | None
    unparseable_jsons: list[tuple[ValidationError, Path]]


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
        "--known-words",
        help="Path to a text file containing known words, each on a new line",
        type=str,
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
                "When --list is not provided, "
                "at least one JSON file path is required."
            )
        )

    json_file_paths = [Path(file_path) for file_path in args.json_file_paths]
    entries_and_file_names: list[tuple[entry.T, Path]] = []
    unparseable_jsons: list[tuple[ValidationError, Path]] = []

    for file_path in json_file_paths:
        path = Path(file_path)
        with file_path.open(encoding="utf-8") as json_file:
            entry_ = entry.create_from_json(json_file.read())
            if isinstance(entry_, ValidationError):
                unparseable_jsons.append((entry_, path))
            else:
                entries_and_file_names.append((entry_, path))

    rule_level_map = {
        "all": rule_level.T.OK,
        "suggestion": rule_level.T.SUGGESTION,
        "warning": rule_level.T.WARNING,
        "error": rule_level.T.ERROR,
    }
    minimum_rule_level = rule_level_map[args.rule_level]

    if args.ignore_yaml:
        trieId_ignored_rule_codes_map = ignored_rules_map.of_yaml(
            Path(args.ignore_yaml)
        )
    else:
        trieId_ignored_rule_codes_map = None

    is_known_word: Callable[[str], bool] | None = None
    if args.known_words:
        with Path(args.known_words).open(encoding="utf-8") as file:
            known_words = file.read().splitlines()

        def is_known_word(word: str) -> bool:
            return word in known_words

    return LintEntries(
        entries_and_file_names=entries_and_file_names,
        is_known_word=is_known_word,
        minimum_rule_level=minimum_rule_level,
        trieId_ignored_rule_codes_map=trieId_ignored_rule_codes_map,
        unparseable_jsons=unparseable_jsons,
    )
