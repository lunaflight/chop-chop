from tests import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/post-157701902"
    expected_post = "Also, we'll have our highlight stories from the show floor. Easier to see and get ideas"  # noqa: E501
    expected_credit = (
        "2025 Oct 30, "
        "Dr.Vijay. "
        "HardwareZone, "
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/the-tech-show-2025-any-good-lobang.7166719/"
    expected_post = "The Tech Show 2025: any good lobang<br>Any interesting products to shop?<br>Have gotten desk from ulti and chair from ergotune<br>got any smart sofa that can recline and dyson promos for their hair curler"  # noqa: E501
    expected_credit = (
        "2025 Oct 30, "
        "katty91. "
        "HardwareZone, "
        '"The Tech Show 2025: any good lobang". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
