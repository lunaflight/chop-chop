from itertools import chain
from typing import TypeAlias

from src.linter.json import attestation_entry, definition_entry

T: TypeAlias = list[definition_entry.T]


def get_linked_words(t: T) -> list[str]:
    linked_words = []
    for definition_entry_ in t:
        linked_words.extend(
            definition_entry.get_linked_words(definition_entry_)
        )
    return linked_words


def self_written_sentences(t: T) -> list[str]:
    return [
        *chain.from_iterable(
            definition_entry.self_written_sentences(e) for e in t
        ),
    ]


def all_strings(t: T) -> list[str]:
    return [
        *chain.from_iterable(definition_entry.all_strings(e) for e in t),
    ]


def get_attestations(t: T) -> list[attestation_entry.T]:
    return [
        *chain.from_iterable(definition_entry.get_attestations(e) for e in t)
    ]
