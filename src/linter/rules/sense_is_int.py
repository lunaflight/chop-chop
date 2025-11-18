from src.linter import entry, rule_result


def description() -> str:
    return "Senses should be a non-negative integer."


def lint(entry_: entry.T) -> rule_result.T:
    sense = entry_["sense"]

    def error_expecting(expectation: str) -> rule_result.T:
        return rule_result.error(f'Found "{sense}", expecting {expectation}')

    try:
        if int(sense) >= 0:
            return rule_result.ok()
        return error_expecting("non-negative integer")
    except ValueError:
        return error_expecting("number")
