import re

CATEGORIES = [
    "abbreviations",
    "brands & companies",
    "childish",
    "conserved english",
    "cuisine",
    "cultural",
    "drinks",
    "education",
    "games",
    "insults",
    "kueh",
    "locations",
    "meme-derived",
    "nature",
    "ns",
    "online slang",
    "onomatopoeia",
    "particles",
    "rhyming slang",
    "sayings",
    "snowclones",
    "terms of address",
    "units of measure",
    "vulgar",
]
CERTAINTY_LEVELS = ["likely", "poss", "dubious", "warn"]


def get_linked_words(s: str) -> list[str]:
    at_word_capture_regex = r"@\{(?:[^|}]+\|)?([^}]+)\}"

    return re.findall(at_word_capture_regex, s)
