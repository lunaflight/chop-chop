import re

from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "(), [] and {} brackets must be closed properly."


def remove_emoticons(s: str) -> str:
    emoticons = {
        ":)", ":]", ";)", ";]",
        "(:", "[:", "(;", "[;",
        ":(", ":[", ";(", ";[",
        "):", "]:", ");", "];",

        ":^)", ":^]", ";^)", ";^]",
        "(^:", "[^:", "(^;", "[^;",
        ":^(", ":^[", ";^(", ";^[",
        ")^:", "]^:", ")^;", "]^;",

        ":-)", ":-]", ";-)", ";-]",
        "(-:", "[-:", "(-;", "[-;",
        ":-(", ":-[", ";-(", ";-[",
        ")-:", "]-:", ")-;", "]-;",

        "=)", "=]", "(=", "[=",
        "=(", "=[", ")=", "]=",
    }  # fmt: skip
    escaped = [re.escape(e) for e in emoticons]

    # delete emoticon surrounded by a non-letter on both sides
    pattern = r"(?<![a-zA-Z])(" + "|".join(escaped) + r")(?![a-zA-Z])"
    return re.sub(pattern, "", s)


def brackets_are_balanced(string: str) -> bool:
    emoteless_string = remove_emoticons(string)
    bracket_map = {")": "(", "}": "{", "]": "["}
    stack: list[str] = []

    for char in emoteless_string:
        if char in bracket_map:
            top_element = stack.pop() if stack else None
            if bracket_map[char] != top_element:
                return False
        elif char in bracket_map.values():
            stack.append(char)

    return len(stack) == 0


def lint(entry_: entry.T) -> rule_result.T:
    sentences = entry.all_strings(entry_)

    for sentence in sentences:
        if not brackets_are_balanced(sentence):
            return rule_result.warning(
                f'The string "{
                    sentence
                }" does not have a balanced bracket sequence.'
            )

    return rule_result.ok()
