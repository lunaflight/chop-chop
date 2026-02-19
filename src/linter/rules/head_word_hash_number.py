import re

from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "The head word should not have a #."


REGEX = r".*(#[0-9]*)"


def lint(entry_: entry.T) -> rule_result.T:
    word = entry_.word

    match = re.search(REGEX, word)
    if match:
        return rule_result.error(
            'You likely mistook "word" for the "trieId" since it ends in '
            f'"{match.group(1)}"'
        )

    return rule_result.ok()
