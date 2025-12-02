from pydantic import BaseModel


class T(BaseModel):
    etyPath: list[str]
    etyScheme: list[str] | None = None
    etyType: list[str] | None = None
    special: list[str] | None = None
    etyScript: list[str] | None = None
    etyTrad: list[str] | None = None
    etyRoman: list[str]
    etyLit: list[str]


def get_linked_words(_t: T) -> list[str]:
    # Assuming that no linked words are in etymology entries.
    # This can very well contain linked words especially in etyRoman,
    # and should be updated if required.
    return []


def self_written_sentences(_t: T) -> list[str]:
    return []


def all_strings(t: T) -> list[str]:
    return [
        *t.etyPath,
        *(t.etyScheme or []),
        *(t.etyType or []),
        *(t.special or []),
        *(t.etyScript or []),
        *(t.etyTrad or []),
        *t.etyRoman,
        *t.etyLit,
    ]
