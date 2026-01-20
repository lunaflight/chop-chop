import re

from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "Braces should be preceded by a caret (^) or at sign (@)."


OKAY_IF_AFTER_CHARACTERS = ["@", "^"]
escaped_chars = "".join(re.escape(char) for char in OKAY_IF_AFTER_CHARACTERS)
PREFIXLESS_BRACE_REGEX = rf"(?<![{escaped_chars}])\{{(.*)\}}"


def lint(entry_: entry.T) -> rule_result.T:
    sentences = entry.self_written_sentences(entry_)

    for sentence in sentences:
        match = re.search(PREFIXLESS_BRACE_REGEX, sentence)
        if match:
            prefixless_brace = match.group(0)
            return rule_result.warning(
                f'Found "{prefixless_brace}", '
                'did you forget a leading "^" or "@"?'
            )

    return rule_result.ok()
