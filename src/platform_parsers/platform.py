from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup

from src.platform_parsers import assertation, mycarforum, reddit, xenforo


class Platform(Enum):
    HARDWAREZONE = "HardwareZone"
    MYCARFORUM = "Mycarforum"
    REDDIT = "Reddit"
    SINGAPOREBRIDES = "SingaporeBrides"
    SINGAPOREMOTHERHOOD = "SingaporeMotherhood"
    SOFT = "S.O.F.T."


# TODO: This file could use a better name, since platform is already one
# of its fields.
@dataclass
class T:
    platform: Platform
    url: str


def to_stylised_string(t: T) -> str:
    match t.platform:
        case Platform.HARDWAREZONE:
            return "HardwareZone"
        case Platform.MYCARFORUM:
            return "Mycarforum"
        case Platform.REDDIT:
            return "Reddit"
        case Platform.SINGAPOREBRIDES:
            return "SingaporeBrides"
        case Platform.SINGAPOREMOTHERHOOD:
            return "SingaporeMotherhood"
        case Platform.SOFT:
            return "S.O.F.T."

    raise ValueError("Unknown platform.")


def to_plain_string(t: T) -> str:
    return to_stylised_string(t).lower()


def identifying_url_substring(platform: Platform) -> str:
    match platform:
        case Platform.HARDWAREZONE:
            return "hardwarezone.com.sg"
        case Platform.MYCARFORUM:
            return "mycarforum.com"
        case Platform.REDDIT:
            return "reddit.com"
        case Platform.SINGAPOREBRIDES:
            return "singaporebrides.com"
        case Platform.SINGAPOREMOTHERHOOD:
            return "singaporemotherhood.com"
        case Platform.SOFT:
            return "soft.com.sg"

    raise ValueError("Unknown platform.")


def of_url(url: str) -> T:
    for platform_ in Platform:
        if identifying_url_substring(platform_) in url:
            return T(platform=platform_, url=url)
    raise ValueError("The URL does not match any known platform.")


def get_assertation(t: T) -> assertation.T:
    match t.platform:
        case Platform.MYCARFORUM:
            return mycarforum.of_url(t.url).assertation()
        case Platform.REDDIT:
            return reddit.of_url(t.url).assertation()
        case (
            Platform.HARDWAREZONE
            | Platform.SINGAPOREBRIDES
            | Platform.SINGAPOREMOTHERHOOD
            | Platform.SOFT
        ):
            return xenforo.of_url(t.url).assertation()


def get_soup_for_testing(t: T) -> BeautifulSoup:
    match t.platform:
        case Platform.MYCARFORUM:
            return mycarforum.of_url(t.url).soup
        case Platform.REDDIT:
            return reddit.of_url(t.url).soup_from_old
        case (
            Platform.HARDWAREZONE
            | Platform.SINGAPOREBRIDES
            | Platform.SINGAPOREMOTHERHOOD
            | Platform.SOFT
        ):
            return xenforo.of_url(t.url).soup


def get_assertation_for_testing(t: T, soup: BeautifulSoup) -> assertation.T:
    match t.platform:
        case Platform.MYCARFORUM:
            return mycarforum.of_url_with_soup(
                url=t.url, soup=soup
            ).assertation()
        case Platform.REDDIT:
            return reddit.of_url_with_soup(
                url=t.url, soup_from_old=soup
            ).assertation()
        case (
            Platform.HARDWAREZONE
            | Platform.SINGAPOREBRIDES
            | Platform.SINGAPOREMOTHERHOOD
            | Platform.SOFT
        ):
            return xenforo.of_url_with_soup(url=t.url, soup=soup).assertation()
