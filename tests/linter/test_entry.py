from itertools import count

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


def test_all_strings() -> None:
    ints = (str(i) for i in count())
    entry_ = entry.create(
        {
            "word": next(ints),
            "trieId": next(ints),
            "sense": next(ints),
            "etyNotes": next(ints),
            "origin": [
                {
                    "etyPath": [next(ints)],
                    "etyScheme": [next(ints)],
                    "etyType": [next(ints)],
                    "special": [next(ints)],
                    "etyScript": [next(ints)],
                    "etyTrad": [next(ints)],
                    "etyRoman": [next(ints)],
                    "etyLit": [next(ints)],
                }
            ],
            "origLink": [next(ints)],
            "meanings": {
                "noun": [
                    {
                        "definition": next(ints),
                        "example": [{"eg": next(ints), "src": next(ints)}],
                        "synonyms": [next(ints)],
                        "antonyms": [next(ints)],
                    }
                ]
            },
            "usage": next(ints),
            "particles": [
                {
                    "particle": next(ints),
                    "effect": next(ints),
                    "meaning": next(ints),
                    "example": next(ints),
                    "exampleSource": next(ints),
                }
            ],
            "related": [next(ints)],
            "category": [next(ints)],
            "references": [
                {
                    "name": next(ints),
                    "link": next(ints),
                }
            ],
            "credits": [next(ints)],
        }
    )
    assert isinstance(entry_, entry.T)

    all_strings = entry.all_strings(entry_)
    assert_expected_inline(
        ", ".join(all_strings),
        """0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28""",
    )
