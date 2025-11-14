import logging

from bs4 import BeautifulSoup

from src.scraper import assertation, platform
from tests.scraper import soup_cacher

LOGGER = logging.getLogger(__name__)


def get_soup(
    platform_: platform.T, test_suffix_for_caching: str
) -> BeautifulSoup:
    platform_str = platform.to_plain_string(platform_)
    filename = f"{platform_str}_{test_suffix_for_caching}"

    cached_soup = soup_cacher.read(filename=filename)
    if not cached_soup:
        cached_soup = platform.get_soup_for_testing(platform_)
        soup_cacher.cache(filename=filename, soup=cached_soup)

    return cached_soup


def get_assertation_as_json(
    url: str,
    test_suffix_for_caching: str,
) -> str:
    platform_ = platform.of_url(url)
    soup = get_soup(
        platform_=platform_, test_suffix_for_caching=test_suffix_for_caching
    )
    assertation_ = platform.get_assertation_for_testing(platform_, soup)
    return assertation.to_json(assertation_)
