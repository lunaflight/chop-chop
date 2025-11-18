import re

from src.linter import entry, rule_result


def description() -> str:
    return "Definitions should not be repeated in the same part of speech."


OKAY_IF_AFTER_CHARACTERS = [" ", "@", "^"]
escaped_chars = "".join(re.escape(char) for char in OKAY_IF_AFTER_CHARACTERS)
MALFORMED_QUOTATION_BRACE_REGEX = rf"(?<![{escaped_chars}])\{{(\d+)\}}"


def lint(entry_: entry.T) -> rule_result.T:
    sentences = entry.self_written_sentences(entry_)

    for sentence in sentences:
        match = re.search(MALFORMED_QUOTATION_BRACE_REGEX, sentence)
        if match:
            malformed_quotation_brace = match.group(0)
            return rule_result.warning(
                f'Found "{malformed_quotation_brace}", '
                'did you forget a "^" for a citation?'
            )

    return rule_result.ok()
