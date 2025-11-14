from expecttest import assert_expected_inline

from src import sanitizer


def test_ufeff_stripped() -> None:
    string = " \ufeffhttps://en.wiktionary.org/wiki/%E9%8D%8B "

    assert_expected_inline(
        sanitizer.clean_input_for_utf8_compatibility(string),
        """https://en.wiktionary.org/wiki/%E9%8D%8B""",
    )


def test_clean_unicode_for_output() -> None:
    string = "bad\xa0 characters…"

    assert_expected_inline(
        sanitizer.clean_unicode_for_output(string), """bad characters..."""
    )
