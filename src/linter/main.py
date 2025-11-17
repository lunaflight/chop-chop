import argparse
from pathlib import Path

from src.linter import entry, rule, rule_format


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "json_file_paths", nargs="+", type=str, help="Paths to the JSON files"
    )
    args = parser.parse_args()

    entries_and_file_names: list[tuple[entry.T, Path]] = []

    for file_path in args.json_file_paths:
        with Path(file_path).open(encoding="utf-8") as json_file:
            entry_ = entry.create_from_json_exn(json_file.read())
            entries_and_file_names.append((entry_, Path(file_path)))

    for entry_, file_path in entries_and_file_names:
        for rule_ in rule.ALL:
            rule_result_ = rule.lint(rule_, entry_)
            output = rule_format.for_stdout(rule_, rule_result_, file_path)
            print(output)  # noqa: T201


if __name__ == "__main__":
    main()
