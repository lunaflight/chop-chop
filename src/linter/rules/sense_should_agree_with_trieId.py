import re

from src.linter import entry, rule_result


def description() -> str:
    return "Sense and trieId should match."


POST_HASH_REGEX = r"#(.*)"


def lint(entry_: entry.T) -> rule_result.T:
    sense = entry_.sense
    trieId = entry_.trieId

    try:
        trieId_sense = re.search(POST_HASH_REGEX, trieId).group(1)  # type: ignore[union-attr]
    except AttributeError:
        trieId_sense = None

    if trieId_sense is None:
        if sense == "0":
            return rule_result.ok()
        return rule_result.error(
            "Expected '#' in trieId because sense is not 0."
        )

    if trieId_sense is not sense:
        return rule_result.error(
            f"Expected sense '{sense}' and trieId '{trieId}' to match "
            "because sense is not 0."
        )

    return rule_result.ok()
