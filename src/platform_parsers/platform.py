from enum import Enum


class T(Enum):
    HARDWAREZONE = "HardwareZone"
    REDDIT = "Reddit"
    SINGAPOREBRIDES = "SingaporeBrides"
    SINGAPOREMOTHERHOOD = "SingaporeMotherhood"


def to_stylised_string(platform: T):
    if platform == T.HARDWAREZONE:
        return "HardwareZone"
    elif platform == T.REDDIT:
        return "Reddit"
    elif platform == T.SINGAPOREBRIDES:
        return "SingaporeBrides"
    elif platform == T.SINGAPOREMOTHERHOOD:
        return "SingaporeMotherhood"
    else:
        raise ValueError("Unknown platform.")


def to_plain_string(platform: T):
    return to_stylised_string(platform).lower()


def identifying_url_substring(platform: T):
    if platform == T.HARDWAREZONE:
        return "hardwarezone.com.sg"
    elif platform == T.REDDIT:
        return "reddit.com"
    elif platform == T.SINGAPOREBRIDES:
        return "singaporebrides.com"
    elif platform == T.SINGAPOREMOTHERHOOD:
        return "singaporemotherhood.com"
    else:
        raise ValueError("Unknown platform.")


def of_url(url: str):
    for platform in T:
        if identifying_url_substring(platform) in url:
            return platform
    raise ValueError("The URL does not match any known platform.")


def is_xenforo(platform: T):
    return (platform == T.HARDWAREZONE or
            platform == T.SINGAPOREBRIDES or
            platform == T.SINGAPOREMOTHERHOOD)
