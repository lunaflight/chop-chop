from typing import TypeAlias

from src.linter.json import definition_entry

T: TypeAlias = list[definition_entry.T]


def get_linked_words(t: T) -> list[str]:
    linked_words = []
    for definition_entry_ in t:
        linked_words.extend(
            definition_entry.get_linked_words(definition_entry_)
        )
    return linked_words
