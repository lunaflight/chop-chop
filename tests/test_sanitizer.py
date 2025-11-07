from src import sanitizer


def test_ufeff_stripped() -> None:
    string = " \ufeffhttps://en.wiktionary.org/wiki/%E9%8D%8B "
    expected_string = "https://en.wiktionary.org/wiki/%E9%8D%8B"

    assert sanitizer.clean_for_utf8_compatibility(string) == expected_string
