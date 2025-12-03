from src.linter import rule_result
from src.linter.json import entry


def description() -> str:
    return "Example sentences must contain the head word."


def lint(entry_: entry.T) -> rule_result.T:
    head_word_forms = entry.head_word_forms(entry_)
    attestations = entry.get_attestations(entry_)

    for attestation_entry_ in attestations:
        sentence = attestation_entry_.eg

        found = False
        for word_form in head_word_forms:
            if word_form.lower() in sentence.lower():
                found = True

        if not found:
            # Suggestion is used since this can get noisy and is not foolproof
            # in detection.
            return rule_result.suggestion(
                f'Found "{sentence}", which does not contain "{entry_.word}". '
                "Did you forget to add it?"
            )

    return rule_result.ok()
