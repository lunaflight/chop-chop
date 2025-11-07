def escape_double_apostrophe(string: str) -> str:
    return string.replace('"', '\\"')


# https://tutorialreference.com/python/examples/faq/python-how-to-remove-ufeff-from-string
def clean_for_utf8_compatibility(string: str) -> str:
    # Clean up \ufeff (Byte Order Mark) chars to ensure good behaivour
    # especially on Windows
    return string.strip().replace("\ufeff", "")
