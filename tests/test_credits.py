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


def _test_assertation(
    url: str, test_name: str, expected_post: str, expected_credit: str
) -> None:
    platform_ = platform.of_url(url)
    soup = get_soup(platform_=platform_, test_name=test_name)
    assertation_ = platform.get_assertation_for_testing(platform_, soup)
    post = assertation_.post
    credit = assertation_.credit

    assert post == expected_post
    assert credit == expected_credit


def test_reddit_reply() -> None:
    test_name = "reply"
    url = "https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9fl4g/"
    expected_post = 'Better to end the operation then to let the public find out how much it cost. <br>Some friends of PAP sure benefit from this "free" shuttle bus service.<br>They could be charging 10k per trip.<br>Even better, like LBW. Oweself award ownself the tender.'  # noqa: E501
    expected_credit = (
        "2025 Oct 13, "
        "u/ValentinoCappuccino. "
        "r/singapore, "
        '"Contract for Marine Parade free shuttle bus service set to end". '
        f"{url}"
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_reddit_main_post() -> None:
    test_name = "main_post"
    url = "https://www.reddit.com/r/singapore/comments/1oixj70/hsa_blood_stocklevels_for_a_is_critical_low_29_oct/"
    expected_post = "HSA Blood StockLevels for A- is Critical Low (29 Oct)<br>According to Red Cross Singapore website. The blood stock levels for A- is at critical low. Screenshot from Red Cross SG website. <br>As a regular blood donor, I hope people who are young and healthy and able to give. Please do so, and especially you are A negative.<br>Blood is needed to save lives in times of emergencies and to sustain the lives of those with medical conditions, like leukemia, thalassaemia and bleeding disorders, as well as patients who are undergoing major surgeries.<br>For many patients, blood donors are their lifeline. One unit of blood can save three lives!<br>Blood Stock level: https://redcross.sg/#bloodstock"  # noqa: E501
    expected_credit = (
        "2025 Oct 29, "
        "u/Bitter-Rattata. "
        "r/singapore, "
        '"HSA Blood StockLevels for A- is Critical Low (29 Oct)". '
        f"{url}"
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_backslash_n_replaced_with_br() -> None:
    test_name = "blackslash_n_replaced_with_br"
    url = "https://www.reddit.com/r/singapore/comments/1o8rpju/grandpas_struggle_to_secure_a_better_hdb_flat/"
    expected_post = "Grandpa's struggle to secure a better HDB flat, 1970s<br>These are all the letters and forms kept by my maternal grandparents to get a HDB flat in the 70s.<br>My maternal grandfather or gua gong, was a coconut hawker with his wife in the old Tekka Market. Everyday, they opened early in the morning to serve the early morning customers, like cooked food hawkers who served breakfast and housewives. They would cut coconuts, grind coconuts and deliver coconuts to the old shophouses along the Rochor Canal. <br>They closed late at night around 10pm, after disposing of the coconut shells and other trash. It was very tiring work that made them desire to live near the market. <br>Originally, my gua gong, gua ma, my mother and her 4 siblings all lived at 12 Race Course Rd, which is now Exit E of the MRT here. My gua gong, who was born in poverty in China, was adopted by his Chia relatives here, who were abusive to him and his family. My own mother recounts being sent to become essentially their maid as a little girl. He wanted to get away from them, and got a 1 rm flat in Kim Keat. It was quickly realised to be too small for a family of 7  so he kept writing to the gov for a larger flat, or one closer to Tekka.<br>He secured Blk 422 AMK in 78 or 79, after years of trying, before selling that flat to finance his final home in Tekka, where I found his documents in our old furniture. "  # noqa: E501
    expected_credit = (
        "2025 Oct 17, "
        "u/mt-tekka. "
        "r/singapore, "
        '"Grandpa\'s struggle to secure a better HDB flat, 1970s". '
        f"{url}"
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_hardwarezone_reply() -> None:
    test_name = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/post-157701902"
    expected_post = "Also, we'll have our highlight stories from the show floor. Easier to see and get ideas"  # noqa: E501
    expected_credit = (
        "2025 Oct 30, "
        "Dr.Vijay. "
        "HardwareZone, "
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_hardwarezone_main_post() -> None:
    test_name = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/"
    expected_post = "The Tech Show 2025: any good lobang<br>Any interesting products to shop?<br>Have gotten desk from ulti and chair from ergotune<br>got any smart sofa that can recline and dyson promos for their hair curler"  # noqa: E501
    expected_credit = (
        "2025 Oct 30, "
        "katty91. "
        "HardwareZone, "
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_soft_reply() -> None:
    test_name = "reply"
    url = "https://soft.com.sg/threads/childhood-jeers.6640/#post-108928"
    expected_post = 'haha...suddenly remembered more...<br>Copy cat, kiss the rat, go home let your mother slap, father say, "nevermind". Mother say, "Go and die!"<br>i learnt that in kindergarten, then when i recited it at home, my mum was appalled, and told me not to chant it anymore...lol!'  # noqa: E501
    expected_credit = (
        f'2005 Oct 30, MichaelAngelo. S.O.F.T., "Childhood jeers". {url}'
    )

    _test_assertation(
        url=url,
        test_name=test_name,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
