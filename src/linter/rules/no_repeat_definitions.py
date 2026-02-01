from src.linter import rule_result
from src.linter.json import entry
from src.python_lib_functions import find_duplicate


def description() -> str:
    return "Definitions should not be repeated in the same part of speech."


def lint(entry_: entry.T) -> rule_result.T:
    for part_of_speech in entry_.meanings.values():
        definitions = [
            definition_entry.definition for definition_entry in part_of_speech
        ]

        duplicate_definition = find_duplicate(definitions)
        if duplicate_definition:
            return rule_result.error(
                f"Found repeat definition: {duplicate_definition}"
            )

    return rule_result.ok()
