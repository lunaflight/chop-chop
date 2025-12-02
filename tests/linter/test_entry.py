from expecttest import assert_expected_inline

from src.linter.json import entry

PURPOSELY_EMPTY = "empty for testing"


def test_linked_words() -> None:
    entry_ = entry.create_for_testing(
        etyNotes="@{etyNotes}",
        meanings={
            "noun": [
                {
                    "definition": "@{definition}",
                    "example": [{"eg": "@{eg}"}],
                    "synonyms": ["synonym"],
                    "antonyms": ["antonym"],
                }
            ]
        },
        particles=[
            {
                "particle": PURPOSELY_EMPTY,
                "effect": PURPOSELY_EMPTY,
                "meaning": "@{particles meaning}",
                "example": "@{particles example}",
            }
        ],
        usage="@{usage}",
        related=["related"],
    )

    linked_words = entry.get_linked_words(entry_)
    assert_expected_inline(
        ", ".join(linked_words),
        """etyNotes, usage, definition, eg, synonym, antonym, particles meaning, particles example, related""",
    )
