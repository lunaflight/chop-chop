from bs4 import BeautifulSoup

from src.platform_parsers import platform
from tests import soup_cacher


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


def assert_produces_post_and_credit(
    url: str,
    test_suffix_for_caching: str,
    expected_post: str,
    expected_credit: str,
) -> None:
    platform_ = platform.of_url(url)
    soup = get_soup(
        platform_=platform_, test_suffix_for_caching=test_suffix_for_caching
    )
    assertation_ = platform.get_assertation_for_testing(platform_, soup)
    post = assertation_.post
    credit = assertation_.credit

    assert post == expected_post
    assert credit == expected_credit
