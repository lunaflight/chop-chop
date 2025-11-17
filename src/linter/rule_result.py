from dataclasses import dataclass
from enum import Enum, auto


class Level(Enum):
    OK = auto()
    SUGGESTION = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass
class T:
    level: Level
    info: str | None


def ok() -> T:
    return T(level=Level.OK, info=None)


def suggestion(info: str) -> T:
    return T(level=Level.SUGGESTION, info=info)


def warning(info: str) -> T:
    return T(level=Level.WARNING, info=info)


def error(info: str) -> T:
    return T(level=Level.ERROR, info=info)


def to_string(t: T) -> str:
    colon_info = "" if t.info is None else f": {t.info}"
    return f"{t.level.name}{colon_info}"
