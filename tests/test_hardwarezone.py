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


def test_replace_ellipses_with_ascii() -> None:
    test_suffix_for_caching = "ellipses"
    url = "https://forums.hardwarezone.com.sg/threads/sg-soon-no-need-water-from-malaysia-liao.7105036/post-155324874"
    expected_post = "If we have sufficient solar electricity or nuclear power generator... we can have endless supply of water...<br>We are limited by energy..."  # noqa: E501
    expected_credit = (
        "2025 Feb 15, "
        "Can Or Not. "
        "HardwareZone, "
        '"SG soon no need water from malaysia liao". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_charmap_codec_handled() -> None:
    test_suffix_for_caching = "charmap_codec"
    url = "https://forums.hardwarezone.com.sg/threads/my-iphone-1-month-changes-3-screen-protector.6757633/post-141915882"
    expected_post = "$3 is cheap liao<br>Bought one recently at one of the shop at Nex due to finger print and dirt<br>Stall owner quote me $19, though i know is chop carrot head but since he serve me and see him hit flies at his stall, then chin chai and bought from him"  # noqa: E501
    expected_credit = (
        "2022 May 31, "
        "106gunner. "
        "HardwareZone, "
        '"真气死人！my iPhone 1 month changes 3 screen protector!". '  # noqa: RUF001
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
