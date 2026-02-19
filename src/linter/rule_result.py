from dataclasses import dataclass

from src.linter import rule_level


@dataclass
class T:
    level: rule_level.T
    info: str | None


def get_level(t: T) -> rule_level.T:
    return t.level


def ok() -> T:
    return T(level=rule_level.T.OK, info=None)


def suggestion(info: str) -> T:
    return T(level=rule_level.T.SUGGESTION, info=info)


def warning(info: str) -> T:
    return T(level=rule_level.T.WARNING, info=info)


def error(info: str) -> T:
    return T(level=rule_level.T.ERROR, info=info)


def to_string(t: T) -> str:
    colon_info = "" if t.info is None else f": {t.info}"
    rule_level_str = rule_level.to_string(t.level)
    return f"{rule_level_str}{colon_info}"
