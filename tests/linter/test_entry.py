from itertools import count

import pytest
from expecttest import assert_expected_inline
from pydantic import ValidationError

from src.linter.json import entry

PURPOSELY_EMPTY = "empty for testing"


def test_missing_fields_raises_error() -> None:
    entry_ = entry.create({})
    assert_expected_inline(
        str(entry_),
        """\
5 validation errors for T
word
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing
trieId
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing
sense
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing
origin
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing
meanings
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing""",
    )


def test_superfluous_field_raises_error() -> None:
    with pytest.raises(ValidationError) as exc_info:
        entry.create_for_testing(superfluous_field=PURPOSELY_EMPTY)
    assert_expected_inline(
        str(exc_info.value),
        """\
1 validation error for T
superfluous_field
  Extra inputs are not permitted [type=extra_forbidden, input_value='empty for testing', input_type=str]
    For further information visit https://errors.pydantic.dev/2.12/v/extra_forbidden""",
    )


def test_nested_superfluous_field_raises_error() -> None:
    with pytest.raises(ValidationError) as exc_info:
        entry.create_for_testing(
            meanings={
                "noun": [
                    {
                        "definition": PURPOSELY_EMPTY,
                        "superfluous_field": PURPOSELY_EMPTY,
                    }
                ]
            }
        )
    assert_expected_inline(
        str(exc_info.value),
        """\
1 validation error for T
meanings.noun.0.superfluous_field
  Extra inputs are not permitted [type=extra_forbidden, input_value='empty for testing', input_type=str]
    For further information visit https://errors.pydantic.dev/2.12/v/extra_forbidden""",
    )


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
            "origlink": [next(ints)],
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
