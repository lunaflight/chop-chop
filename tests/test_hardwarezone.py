from tests import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/post-138981367"
    expected_post = "Normal lah, jin happy collect money then throw tile liao ... then forget pu one tile xiao xiang gong"  # noqa: E501
    expected_credit = (
        "2022 Jan 4, "
        "Bunknifer. "
        "HardwareZone, "
        '"Noob mahjong question - experts please help". '
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
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/"
    expected_post = "Noob mahjong question - experts please help<br>Let’s say I 听 六万 九万。Someone throws 九万 I didn’t see or missed. Then in the same round the next player throws 六万，can I game?"  # noqa: E501, RUF001
    expected_credit = (
        "2022 Jan 3, "
        "gytaci. "
        "HardwareZone, "
        '"Noob mahjong question - experts please help". '
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
