from src.linter import entry, rule_result


def lint(entry: entry.T) -> rule_result.T:
    sense = entry["sense"]

    def error_expecting(expectation: str) -> str:
        return f'Found "{sense}", expecting {expectation}'

    try:
        if int(sense) >= 0:
            return rule_result.ok()
        return rule_result.error(error_expecting("non-negative integer"))
    except ValueError:
        return rule_result.error(error_expecting("number"))
