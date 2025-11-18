# Quick Start
Run `./scripts/lint.sh json_file [json_files...]` to run the script.

It runs a set of rules on the JSON files and catches mistakes to the best of
its ability. It does not guarantee that the JSON file is perfect.

## Flags
<!-- TODO: Think about how to suppress errors -->
| Flag | Description |
|------|-------------|
| `--rule-level` | Set the minimum severity level for rules to be displayed. Choices: `all`, `suggestion`, `warning`, `error`. Default: `suggestion`. Shows rules greater than or equal to the specified level. |
| `--list` | List all the linter rules with their codes and descriptions. |
