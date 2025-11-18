from pathlib import Path

from src.linter import rule, rule_result


def for_stdout(
    rule_: rule.T, rule_result_: rule_result.T, file_path: Path
) -> str:
    rule_result_str = rule_result.to_string(rule_result_)
    rule_str = rule.to_string(rule_)
    rule_code = rule.to_code(rule_)
    return (
        f'{rule_result_str} (rule "{rule_str}" '
        f'[{rule_code}] in file "{file_path}")'
    )
