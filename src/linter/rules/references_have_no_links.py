import re

from src.linter import rule_result
from src.linter.json import entry

HTTP_REGEX = r"https?://"


def description() -> str:
    return "References should not contains HTTPS links."


def lint(entry_: entry.T) -> rule_result.T:
    for reference in entry_.references or []:
        if re.search(HTTP_REGEX, reference.name):
            return rule_result.warning(
                f'Found "{reference.name}" in references, '
                f"the [link] field should be used to provide a HTTPS link"
            )
    return rule_result.ok()
