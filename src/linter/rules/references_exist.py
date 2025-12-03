import re

from src.linter import rule_result
from src.linter.json import entry
from src.linter.json.specs import REFERENCE_CAPTURE_REGEX


def description() -> str:
    return "Every reference should link to something that exists."


def lint(entry_: entry.T) -> rule_result.T:
    strings = entry.all_strings(entry_)
    number_of_references = (
        len(entry_.references) if entry_.references is not None else 0
    )

    reference_numbers: list[int] = []
    for string in strings:
        matches = re.findall(REFERENCE_CAPTURE_REGEX, string)
        reference_numbers.extend(int(match) for match in matches)

    if reference_numbers == []:
        return rule_result.ok()

    maximum_ref_num = max(reference_numbers)
    if maximum_ref_num > number_of_references:
        return rule_result.error(
            f"The largest reference number found is {maximum_ref_num} "
            f"but insufficient references ({number_of_references}) exist."
        )

    return rule_result.ok()
