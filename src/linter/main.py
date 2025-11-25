import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import TypedDict

from src import logging_format
from src.linter import (
    argument_parser,
    entry,
    ignored_rules_map,
    rule,
    rule_format,
    rule_level,
    rule_result,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class LintResult(TypedDict):
    output_strings: list[str]
    has_error: bool


def lint(
    entries_and_file_names: list[tuple[entry.T, Path]],
    is_known_word: Callable[[str], bool] | None,
    minimum_rule_level: rule_level.T,
    trieId_ignored_rule_codes_map: ignored_rules_map.T | None,
    rules: list[rule.T],
) -> LintResult:
    output_strings: list[str] = []
    has_error = False

    for (entry_, file_path), rule_ in product(entries_and_file_names, rules):
        trieId = entry_.trieId
        if (
            trieId_ignored_rule_codes_map is not None
            and ignored_rules_map.is_ignored(
                trieId_ignored_rule_codes_map, trieId, rule_
            )
        ):
            continue

        rule_result_ = rule.lint(rule_, entry_, is_known_word)
        if isinstance(rule_result_, rule.LintRunError):
            LOGGER.error(rule_result_.message)
            continue

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


def main() -> None:
    parse_result = argument_parser.parse_arguments()

    logging.basicConfig(
        level=logging.WARNING,
        format=logging_format.DEFAULT,
    )

    if isinstance(parse_result, argument_parser.Error):
        LOGGER.error(parse_result.message)
        sys.exit(1)

    if isinstance(parse_result, argument_parser.ListAllRules):
        for rule_ in rule.ALL:
            print(f"{rule.to_string(rule_)}[{rule.to_code(rule_)}]")  # noqa: T201
            print(f"    {rule.description(rule_)}")  # noqa: T201
        sys.exit(0)

    for validation_error, path in parse_result["unparseable_jsons"]:
        LOGGER.error(
            "Could not parse file -- see validation error. %s",
            {"path": path, "validation_error": validation_error},
        )

    lint_result = lint(
        entries_and_file_names=parse_result["entries_and_file_names"],
        is_known_word=parse_result["is_known_word"],
        minimum_rule_level=parse_result["minimum_rule_level"],
        trieId_ignored_rule_codes_map=parse_result[
            "trieId_ignored_rule_codes_map"
        ],
        rules=rule.ALL,
    )

    for output in lint_result["output_strings"]:
        print(output)  # noqa: T201

    has_error = (
        lint_result["has_error"] or len(parse_result["unparseable_jsons"]) > 0
    )
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
