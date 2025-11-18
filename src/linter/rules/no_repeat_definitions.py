from src.linter import entry, rule_result


def lint(entry_: entry.T) -> rule_result.T:
    for part_of_speech in entry_["meanings"].values():
        seen_definitions: set[str] = set()

        for definition_entry in part_of_speech:
            definition = definition_entry["definition"]

            if definition in seen_definitions:
                return rule_result.error(
                    f"Found repeat definition: {definition}"
                )

            seen_definitions.add(definition)

    return rule_result.ok()
