import re

from src.linter import entry, rule_result

HASH_BRACE_CAPTURE = r"#\{(.*?)\}"

POSSIBLE_CONTENTS = ["likely", "poss", "dubious", "warn"]


def lint(entry_: entry.T) -> rule_result.T:
    def error_finding(finding: str) -> rule_result.T:
        return rule_result.error(
            f'Found "{finding}", hash braces only accept '
            f"[{', '.join(POSSIBLE_CONTENTS)}]"
        )

    sentences = entry.all_strings(entry_)

    for sentence in sentences:
        contents = re.findall(HASH_BRACE_CAPTURE, sentence)
        for content in contents:
            if content not in POSSIBLE_CONTENTS:
                return error_finding(content)

    return rule_result.ok()
