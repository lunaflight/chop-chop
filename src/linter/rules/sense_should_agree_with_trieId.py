import re

from src.linter import entry, rule_result


def description() -> str:
    return "Sense and trieId should match."


POST_HASH_REGEX = r"#(.*)"


def lint(entry_: entry.T) -> rule_result.T:
    sense = entry_.sense
    trieId = entry_.trieId

    if sense == "0":
        return rule_result.ok()

    match = re.search(POST_HASH_REGEX, trieId)

    if not match:
        return rule_result.error(
            "Expected '#' in trieId because sense is not 0."
        )

    post_hash_string = match.group(1)

    if post_hash_string == sense:
        return rule_result.ok()
    return rule_result.error(
        f"Expected sense '{sense}' and trieId '{trieId}' to match"
        "because sense is not 0."
    )
