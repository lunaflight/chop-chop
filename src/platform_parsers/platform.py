from enum import Enum


class T(Enum):
    HARDWAREZONE = "HardwareZone"
    REDDIT = "Reddit"
    SINGAPOREBRIDES = "SingaporeBrides"
    SINGAPOREMOTHERHOOD = "SingaporeMotherhood"


def to_stylised_string(platform: T) -> str:
    if platform == T.HARDWAREZONE:
        return "HardwareZone"
    if platform == T.REDDIT:
        return "Reddit"
    if platform == T.SINGAPOREBRIDES:
        return "SingaporeBrides"
    if platform == T.SINGAPOREMOTHERHOOD:
        return "SingaporeMotherhood"

    raise ValueError("Unknown platform.")


def to_plain_string(platform: T) -> str:
    return to_stylised_string(platform).lower()


def identifying_url_substring(platform: T) -> str:
    if platform == T.HARDWAREZONE:
        return "hardwarezone.com.sg"
    if platform == T.REDDIT:
        return "reddit.com"
    if platform == T.SINGAPOREBRIDES:
        return "singaporebrides.com"
    if platform == T.SINGAPOREMOTHERHOOD:
        return "singaporemotherhood.com"

    raise ValueError("Unknown platform.")


def of_url(url: str) -> T:
    for platform in T:
        if identifying_url_substring(platform) in url:
            return platform
    raise ValueError("The URL does not match any known platform.")


def is_xenforo(platform: T) -> bool:
    return platform in {T.HARDWAREZONE,
                        T.SINGAPOREBRIDES,
                        T.SINGAPOREMOTHERHOOD}
