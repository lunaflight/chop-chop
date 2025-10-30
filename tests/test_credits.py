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


def _test_assertation(url: str,
                      test_name: str,
                      expected_post: str,
                      expected_credit: str) -> None:
    platform_ = platform.of_url(url)
    soup = get_soup(platform_=platform_, test_name=test_name)
    assertation_ = platform.get_assertation_for_testing(platform_, soup)
    post = assertation_.post
    credit = assertation_.credit

    assert post == expected_post
    assert credit == expected_credit


# TODO: This needs to test the post as well. This means that an attestation.py
# and functions that return attestation.Ts might be sane.
def test_reddit_reply() -> None:
    test_name = "reply"
    url = "https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9fl4g/"
    expected_post = 'Contract for Marine Parade free shuttle bus service set to end<br>Better to end the operation then to let the public find out how much it cost. <br>Some friends of PAP sure benefit from this "free" shuttle bus service.<br>They could be charging 10k per trip.<br>Even better, like LBW. Oweself award ownself the tender.'  # noqa: E501
    expected_credit = (
        '2025 Oct 13, '
        'u/ValentinoCappuccino. '
        'r/singapore, '
        '"Contract for Marine Parade free shuttle bus service set to end". '
        f"{url}"
    )

    _test_assertation(url=url,
                      test_name=test_name,
                      expected_post=expected_post,
                      expected_credit=expected_credit)


def test_reddit_main_post() -> None:
    test_name = "main_post"
    url = "https://www.reddit.com/r/singapore/comments/1oixj70/hsa_blood_stocklevels_for_a_is_critical_low_29_oct/"
    expected_post = "HSA Blood StockLevels for A- is Critical Low (29 Oct)<br>According to Red Cross Singapore website. The blood stock levels for A- is at critical low. Screenshot from Red Cross SG website. <br>As a regular blood donor, I hope people who are young and healthy and able to give. Please do so, and especially you are A negative.<br>Blood is needed to save lives in times of emergencies and to sustain the lives of those with medical conditions, like leukemia, thalassaemia and bleeding disorders, as well as patients who are undergoing major surgeries.<br>For many patients, blood donors are their lifeline. One unit of blood can save three lives!<br>Blood Stock level: https://redcross.sg/#bloodstock"  # noqa: E501
    expected_credit = (
        '2025 Oct 29, '
        'u/Bitter-Rattata. '
        'r/singapore, '
        '"HSA Blood StockLevels for A- is Critical Low (29 Oct)". '
        f"{url}"
    )

    _test_assertation(url=url,
                      test_name=test_name,
                      expected_post=expected_post,
                      expected_credit=expected_credit)


def test_hardwarezone_reply() -> None:
    test_name = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/post-157701902"
    expected_post = "Also, we'll have our highlight stories from the show floor. Easier to see and get ideas"  # noqa: E501
    expected_credit = (
        '2025 Oct 30, '
        'Dr.Vijay. '
        'HardwareZone, '
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    _test_assertation(url=url,
                      test_name=test_name,
                      expected_post=expected_post,
                      expected_credit=expected_credit)


def test_hardwarezone_main_post() -> None:
    test_name = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/"
    expected_post = "The Tech Show 2025: any good lobang<br>Any interesting products to shop?<br>Have gotten desk from ulti and chair from ergotune<br>got any smart sofa that can recline and dyson promos for their hair curler"  # noqa: E501
    expected_credit = (
        '2025 Oct 30, '
        'katty91. '
        'HardwareZone, '
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    _test_assertation(url=url,
                      test_name=test_name,
                      expected_post=expected_post,
                      expected_credit=expected_credit)
