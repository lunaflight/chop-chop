#!/usr/bin/env python3

from bs4 import BeautifulSoup

from src.platform_parsers import platform
from tests import soup_cacher


def get_soup(platform_: platform.T, test_name: str) -> BeautifulSoup:
    platform_str = platform.to_plain_string(platform_)
    filename = f"{platform_str}_{test_name}"

    cached_soup = soup_cacher.read(filename=filename)
    if not cached_soup:
        cached_soup = platform.get_soup_for_testing(platform_)
        soup_cacher.cache(filename=filename, soup=cached_soup)

    return cached_soup


def assert_credit(url: str, test_name: str, expected_credit: str) -> None:
    platform_ = platform.of_url(url)
    soup = get_soup(platform_=platform_, test_name=test_name)
    credit = platform.credit_with_soup_for_testing(platform_, soup)

    assert credit == expected_credit


# TODO: This needs to test the post as well. This means that an attestation.py
# and functions that return attestation.Ts might be sane.
def test_reddit_reply() -> None:
    test_name = "reply"
    url = "https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9fl4g/"
    expected_credit = (
        '2025 Oct 13, '
        'u/ValentinoCappuccino. '
        'r/singapore, '
        '"Contract for Marine Parade free shuttle bus service set to end". '
        f"{url}"
    )

    assert_credit(url=url,
                  test_name=test_name,
                  expected_credit=expected_credit)


def test_reddit_main_post() -> None:
    test_name = "main_post"
    url = "https://www.reddit.com/r/singapore/comments/1oixj70/hsa_blood_stocklevels_for_a_is_critical_low_29_oct/"
    expected_credit = (
        '2025 Oct 29, '
        'u/Bitter-Rattata. '
        'r/singapore, '
        '"HSA Blood StockLevels for A- is Critical Low (29 Oct)". '
        f"{url}"
    )

    assert_credit(url=url,
                  test_name=test_name,
                  expected_credit=expected_credit)


def test_hardwarezone_reply() -> None:
    test_name = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/post-157701902"
    expected_credit = (
        '2025 Oct 30, '
        'Dr.Vijay. '
        'HardwareZone, '
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    assert_credit(url=url,
                  test_name=test_name,
                  expected_credit=expected_credit)


def test_hardwarezone_main_post() -> None:
    test_name = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/"
    expected_credit = (
        '2025 Oct 30, '
        'katty91. '
        'HardwareZone, '
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    assert_credit(url=url,
                  test_name=test_name,
                  expected_credit=expected_credit)
