def escape_double_apostrophe(string: str) -> str:
    return string.replace('"', '\\"')


# https://tutorialreference.com/python/examples/faq/python-how-to-remove-ufeff-from-string
def clean_input_for_utf8_compatibility(string: str) -> str:
    # Clean up \ufeff (Byte Order Mark) chars to ensure good behaviour from
    # stdin especially on Windows
    return string.strip().replace("\ufeff", "")


def clean_unicode_for_output(string: str) -> str:
    replacements = {
        "\xa0": "",  # non-breaking space
        "…": "...",
    }

    for key, val in replacements.items():
        string = string.replace(key, val)

    return string
