from src.linter import rule_result
from src.linter.json import entry
from src.linter.json.specs import CATEGORIES


def description() -> str:
    return "The categories should be spelled correctly."


def lint(entry_: entry.T) -> rule_result.T:
    categories = entry_.category

    if categories is None:
        return rule_result.ok()

    for category in categories:
        if category not in CATEGORIES:
            return rule_result.error(
                f'Found "{category}", known categories are '
                f"[{', '.join(CATEGORIES)}]"
            )

    return rule_result.ok()
