from dataclasses import dataclass
from enum import Enum, auto

from bs4 import BeautifulSoup

from src.scraper import assertation
from src.scraper.platforms import invision, reddit, xenforo


class SiteName(Enum):
    BLOWINGWIND = auto()
    HARDWAREZONE = auto()
    MYCARFORUM = auto()
    REDDIT = auto()
    SINGAPOREBRIDES = auto()
    SINGAPOREMOTHERHOOD = auto()
    SOFT = auto()


@dataclass
class T:
    site_name: SiteName
    url: str


def to_stylised_string(t: T) -> str:  # noqa: PLR0911
    match t.site_name:
        case SiteName.BLOWINGWIND:
            return "Blowing Wind"
        case SiteName.HARDWAREZONE:
            return "HardwareZone"
        case SiteName.MYCARFORUM:
            return "Mycarforum"
        case SiteName.REDDIT:
            return "Reddit"
        case SiteName.SINGAPOREBRIDES:
            return "SingaporeBrides"
        case SiteName.SINGAPOREMOTHERHOOD:
            return "SingaporeMotherhood"
        case SiteName.SOFT:
            return "S.O.F.T."

    raise ValueError("Unknown site_name.")


def to_plain_string(t: T) -> str:
    return to_stylised_string(t).lower().replace(" ", "_")


def identifying_url_substring(site_name: SiteName) -> str:  # noqa: PLR0911
    match site_name:
        case SiteName.BLOWINGWIND:
            return "blowingwind.io"
        case SiteName.HARDWAREZONE:
            return "hardwarezone.com.sg"
        case SiteName.MYCARFORUM:
            return "mycarforum.com"
        case SiteName.REDDIT:
            return "reddit.com"
        case SiteName.SINGAPOREBRIDES:
            return "singaporebrides.com"
        case SiteName.SINGAPOREMOTHERHOOD:
            return "singaporemotherhood.com"
        case SiteName.SOFT:
            return "soft.com.sg"

    raise ValueError("Unknown site_name.")


def of_url(url: str) -> T:
    for site_name_ in SiteName:
        if identifying_url_substring(site_name_) in url:
            return T(site_name=site_name_, url=url)
    raise ValueError("The URL does not match any known site_name.")


def get_assertation(t: T) -> assertation.T:
    match t.site_name:
        case SiteName.BLOWINGWIND | SiteName.MYCARFORUM:
            return invision.of_url(t.url).assertation()
        case SiteName.REDDIT:
            return reddit.of_url(t.url).assertation()
        case (
            SiteName.HARDWAREZONE
            | SiteName.SINGAPOREBRIDES
            | SiteName.SINGAPOREMOTHERHOOD
            | SiteName.SOFT
        ):
            return xenforo.of_url(t.url).assertation()


def get_soup_for_testing(t: T) -> BeautifulSoup:
    match t.site_name:
        case SiteName.BLOWINGWIND | SiteName.MYCARFORUM:
            return invision.of_url(t.url).soup
        case SiteName.REDDIT:
            return reddit.of_url(t.url).soup_from_old
        case (
            SiteName.HARDWAREZONE
            | SiteName.SINGAPOREBRIDES
            | SiteName.SINGAPOREMOTHERHOOD
            | SiteName.SOFT
        ):
            return xenforo.of_url(t.url).soup


def get_assertation_for_testing(t: T, soup: BeautifulSoup) -> assertation.T:
    match t.site_name:
        case SiteName.BLOWINGWIND | SiteName.MYCARFORUM:
            return invision.of_url_with_soup(url=t.url, soup=soup).assertation()
        case SiteName.REDDIT:
            return reddit.of_url_with_soup(
                url=t.url, soup_from_old=soup
            ).assertation()
        case (
            SiteName.HARDWAREZONE
            | SiteName.SINGAPOREBRIDES
            | SiteName.SINGAPOREMOTHERHOOD
            | SiteName.SOFT
        ):
            return xenforo.of_url_with_soup(url=t.url, soup=soup).assertation()
