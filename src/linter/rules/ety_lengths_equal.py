from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "The number of entries in the etymology should match across fields."


def lint(entry_: entry.T) -> rule_result.T:
    for etymology_entry in entry_.origin:
        components = [
            ("etyPath", len(etymology_entry.etyPath)),
            ("etyRoman", len(etymology_entry.etyRoman)),
            ("etyLit", len(etymology_entry.etyLit)),
        ]

        lengths = [length for _, length in components]

        if len(set(lengths)) > 1:
            error_details = ", ".join(
                f"{name} (length: {length})" for name, length in components
            )

            first_word = (
                etymology_entry.etyRoman[0]
                if etymology_entry.etyRoman
                else "unknown word"
            )

            return rule_result.error(
                "Found mismatched lengths in the etymology of "
                f"{first_word}: {error_details}"
            )

    return rule_result.ok()
