from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "No TODOs should be found."


def lint(entry_: entry.T) -> rule_result.T:
    all_strings = entry.all_strings(entry_)
    todo_strings = [s for s in all_strings if "TODO" in s]

    if todo_strings:
        return rule_result.warning(
            f'found TODO in "{todo_strings[0]}" -- this entry is unfinished.'
        )

    return rule_result.ok()
