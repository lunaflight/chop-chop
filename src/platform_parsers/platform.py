from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup

from src.platform_parsers import reddit, xenforo


class Platform(Enum):
    HARDWAREZONE = "HardwareZone"
    REDDIT = "Reddit"
    SINGAPOREBRIDES = "SingaporeBrides"
    SINGAPOREMOTHERHOOD = "SingaporeMotherhood"


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
        case Platform.REDDIT:
            return "Reddit"
        case Platform.SINGAPOREBRIDES:
            return "SingaporeBrides"
        case Platform.SINGAPOREMOTHERHOOD:
            return "SingaporeMotherhood"

    raise ValueError("Unknown platform.")


def to_plain_string(t: T) -> str:
    return to_stylised_string(t).lower()


def identifying_url_substring(platform: Platform) -> str:
    match platform:
        case Platform.HARDWAREZONE:
            return "hardwarezone.com.sg"
        case Platform.REDDIT:
            return "reddit.com"
        case Platform.SINGAPOREBRIDES:
            return "singaporebrides.com"
        case Platform.SINGAPOREMOTHERHOOD:
            return "singaporemotherhood.com"

    raise ValueError("Unknown platform.")


def of_url(url: str) -> T:
    for platform in Platform:
        if identifying_url_substring(platform) in url:
            return T(platform=platform, url=url)
    raise ValueError("The URL does not match any known platform.")


def post(t: T) -> str:
    match t.platform:
        case Platform.REDDIT:
            return reddit.of_url(t.url).post()
        case (Platform.HARDWAREZONE
              | Platform.SINGAPOREBRIDES
              | Platform.SINGAPOREMOTHERHOOD):
            return xenforo.of_url(t.url).post()


def credit(t: T) -> str:
    match t.platform:
        case Platform.REDDIT:
            return reddit.of_url(t.url).credit()
        case (Platform.HARDWAREZONE
              | Platform.SINGAPOREBRIDES
              | Platform.SINGAPOREMOTHERHOOD):
            return xenforo.of_url(t.url).credit()


def get_soup_for_testing(t: T) -> BeautifulSoup:
    match t.platform:
        case Platform.REDDIT:
            return reddit.of_url(t.url).soup_from_old
        case (Platform.HARDWAREZONE
              | Platform.SINGAPOREBRIDES
              | Platform.SINGAPOREMOTHERHOOD):
            return xenforo.of_url(t.url).soup


def credit_with_soup_for_testing(t: T, soup: BeautifulSoup) -> str:
    match t.platform:
        case Platform.REDDIT:
            return (reddit.of_url_with_soup(url=t.url, soup_from_old=soup)
                    .credit())
        case (Platform.HARDWAREZONE
              | Platform.SINGAPOREBRIDES
              | Platform.SINGAPOREMOTHERHOOD):
            return xenforo.of_url_with_soup(url=t.url, soup=soup).credit()
