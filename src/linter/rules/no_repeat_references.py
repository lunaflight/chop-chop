from src.linter import rule_result
from src.linter.json import entry
from src.python_lib_functions import find_duplicate


def description() -> str:
    return "References should not be repeated."


def lint(entry_: entry.T) -> rule_result.T:
    if entry_.references is None:
        return rule_result.ok()

    names: list[str] = [reference.name for reference in entry_.references]
    links: list[str] = [
        reference.link
        for reference in entry_.references
        if reference.link is not None
    ]

    duplicate_name: str | None = find_duplicate(names)
    if duplicate_name:
        return rule_result.error(
            f"Found repeat reference name: {duplicate_name}"
        )

    duplicate_link: str | None = find_duplicate(links)
    if duplicate_link:
        return rule_result.error(
            f"Found repeat reference link: {duplicate_link}"
        )

    return rule_result.ok()
