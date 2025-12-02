from collections.abc import Callable

from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return (
        "Words that are linked via @{} or are listed must link to known "
        "entries."
    )


def lint(
    entry_: entry.T, is_known_word: Callable[[str], bool]
) -> rule_result.T:
    linked_words = entry.get_linked_words(entry_)
    for word in linked_words:
        if not is_known_word(word):
            return rule_result.error(
                f'Found "{word}", which does not link to a valid word.'
            )

    return rule_result.ok()
