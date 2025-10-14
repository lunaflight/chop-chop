from enum import Enum


class T(Enum):
    REDDIT = "Reddit"
    HARDWAREZONE = "HardwareZone"
    SINGAPOREBRIDES = "SingaporeBrides"


def to_stylised_string(platform: T):
    if platform == T.REDDIT:
        return "Reddit"
    elif platform == T.HARDWAREZONE:
        return "HardwareZone"
    elif platform == T.SINGAPOREBRIDES:
        return "SingaporeBrides"
    else:
        raise ValueError("Unknown platform.")


def to_plain_string(platform: T):
    if platform == T.REDDIT:
        return "reddit"
    elif platform == T.HARDWAREZONE:
        return "hardwarezone"
    elif platform == T.SINGAPOREBRIDES:
        return "singaporebrides"
    else:
        raise ValueError("Unknown platform.")


def identifying_url_substring(platform: T):
    if platform == T.REDDIT:
        return "reddit.com"
    elif platform == T.HARDWAREZONE:
        return "hardwarezone.com.sg"
    elif platform == T.SINGAPOREBRIDES:
        return "singaporebrides.com"
    else:
        raise ValueError("Unknown platform.")


def of_url(url: str):
    for platform in T:
        if identifying_url_substring(platform) in url:
            return platform
    raise ValueError("The URL does not match any known platform.")


def is_xenforo(platform: T):
    return platform == T.HARDWAREZONE or platform == T.SINGAPOREBRIDES
