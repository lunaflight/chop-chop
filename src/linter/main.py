import argparse
import sys
from itertools import product
from pathlib import Path

from src.linter import entry, rule, rule_format, rule_level, rule_result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "json_file_paths", nargs="+", type=str, help="Paths to the JSON files"
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
    args = parser.parse_args()

    rule_level_map = {
        "all": rule_level.T.OK,
        "suggestion": rule_level.T.SUGGESTION,
        "warning": rule_level.T.WARNING,
        "error": rule_level.T.ERROR,
    }
    rule_level_for_stdout = rule_level_map[args.rule_level]

    entries_and_file_names: list[tuple[entry.T, Path]] = []

    for file_path in args.json_file_paths:
        with Path(file_path).open(encoding="utf-8") as json_file:
            entry_ = entry.create_from_json_exn(json_file.read())
            entries_and_file_names.append((entry_, Path(file_path)))

    output_strings: list[str] = []
    has_error = False

    for (entry_, file_path), rule_ in product(entries_and_file_names, rule.ALL):
        rule_result_ = rule.lint(rule_, entry_)
        rule_level_ = rule_result.get_level(rule_result_)

        is_severe_enough_to_log = rule_level.greater_than_or_equal_to(
            rule_level_, rule_level_for_stdout
        )

        if is_severe_enough_to_log:
            output = rule_format.for_stdout(rule_, rule_result_, file_path)
            output_strings.append(output)

        if is_severe_enough_to_log and rule_level_ is not rule_level.T.OK:
            has_error = True

    for output in output_strings:
        print(output)  # noqa: T201

    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
