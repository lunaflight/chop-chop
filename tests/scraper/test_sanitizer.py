from src import sanitizer


def test_ufeff_stripped() -> None:
    string = " \ufeffhttps://en.wiktionary.org/wiki/%E9%8D%8B "
    expected_string = "https://en.wiktionary.org/wiki/%E9%8D%8B"

    assert (
        sanitizer.clean_input_for_utf8_compatibility(string) == expected_string
    )


def test_clean_unicode_for_output() -> None:
    string = "bad\xa0 characters…"
    expected_string = "bad characters..."

    assert sanitizer.clean_unicode_for_output(string) == expected_string
