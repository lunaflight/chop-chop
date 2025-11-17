import re

from src.linter import entry, rule_result
from src.linter.json_specs import CERTAINTY_LEVELS

HASH_BRACE_CAPTURE = r"#\{(.*?)\}"


def lint(entry_: entry.T) -> rule_result.T:
    sentences = entry.all_strings(entry_)

    for sentence in sentences:
        contents = re.findall(HASH_BRACE_CAPTURE, sentence)
        for content in contents:
            if content not in CERTAINTY_LEVELS:
                return rule_result.error(
                    f'Found "{content}", hash braces only accept '
                    f"[{', '.join(CERTAINTY_LEVELS)}]"
                )

    return rule_result.ok()
