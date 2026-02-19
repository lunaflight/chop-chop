import re

from src.linter import rule_result
from src.linter.json import entry
from src.linter.json.specs import CERTAINTY_LEVELS


def description() -> str:
    return "The contents of #{} should spelled correctly."


HASH_BRACE_CAPTURE_REGEX = r"#\{(.*?)\}"


def lint(entry_: entry.T) -> rule_result.T:
    sentences = entry.self_written_sentences(entry_)

    for sentence in sentences:
        contents = re.findall(HASH_BRACE_CAPTURE_REGEX, sentence)
        for content in contents:
            if content not in CERTAINTY_LEVELS:
                return rule_result.error(
                    f'Found "{content}", hash braces only accept '
                    f"[{', '.join(CERTAINTY_LEVELS)}]"
                )

    return rule_result.ok()
