from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "(), [] and {} brackets must be closed properly."


def brackets_are_balanced(s: str) -> bool:
    bracket_map = {")": "(", "}": "{", "]": "["}
    stack: list[str] = []

    for char in s:
        if char in bracket_map:
            top_element = stack.pop() if stack else None
            if bracket_map[char] != top_element:
                return False
        elif char in bracket_map.values():
            stack.append(char)

    return len(stack) == 0


def lint(entry_: entry.T) -> rule_result.T:
    strings = entry.all_strings(entry_)

    for s in strings:
        if not brackets_are_balanced(s):
            return rule_result.warning(
                f'The string "{s}" does not have a balanced bracket sequence.'
            )

    return rule_result.ok()
