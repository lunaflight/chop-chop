from src.linter import entry, rule_result
from src.linter.json_specs import CATEGORIES


def lint(entry_: entry.T) -> rule_result.T:
    categories = entry_["category"]

    if categories is None:
        return rule_result.ok()

    for category in categories:
        if category not in CATEGORIES:
            return rule_result.error(
                f'Found "{category}", known categories are '
                f"[{', '.join(CATEGORIES)}]"
            )

    return rule_result.ok()
