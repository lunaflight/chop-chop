import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import TypedDict

from src.linter import (
    argument_parser,
    entry,
    rule,
    rule_format,
    rule_level,
    rule_result,
)


@dataclass
class LintResult(TypedDict):
    output_strings: list[str]
    has_error: bool


def lint(
    entries_and_file_names: list[tuple[entry.T, Path]],
    minimum_rule_level: rule_level.T,
    trieId_ignored_rule_codes_map: dict[str, list[rule.T]] | None,
    rules: list[rule.T],
) -> LintResult:
    output_strings: list[str] = []
    has_error = False

    for (entry_, file_path), rule_ in product(entries_and_file_names, rules):
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


def main() -> None:
    parse_result = argument_parser.parse_arguments()

    if isinstance(parse_result, argument_parser.Error):
        print(parse_result, file=sys.stderr)  # noqa: T201
        sys.exit(1)

    if isinstance(parse_result, argument_parser.ListAllRules):
        for rule_ in rule.ALL:
            print(f"{rule.to_string(rule_)}[{rule.to_code(rule_)}]")  # noqa: T201
            print(f"    {rule.description(rule_)}")  # noqa: T201
        sys.exit(0)

    lint_result = lint(
        entries_and_file_names=parse_result["entries_and_file_names"],
        minimum_rule_level=parse_result["minimum_rule_level"],
        trieId_ignored_rule_codes_map=parse_result[
            "trieId_ignored_rule_codes_map"
        ],
        rules=rule.ALL,
    )
    for output in lint_result["output_strings"]:
        print(output)  # noqa: T201

    sys.exit(1 if lint_result["has_error"] else 0)


if __name__ == "__main__":
    main()
