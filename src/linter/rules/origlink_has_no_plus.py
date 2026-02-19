from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return (
        "The origlink field should not have a + as it will be rendered with"
        "an underline. Instead, an empty string should be provided."
    )


def lint(entry_: entry.T) -> rule_result.T:
    if "+" in (entry_.origlink or []):
        return rule_result.warning(
            "Found + in [origlink], consider using an empty string so it is "
            "rendered without an underline."
        )

    return rule_result.ok()
