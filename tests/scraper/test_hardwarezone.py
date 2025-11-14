from expecttest import assert_expected_inline

from tests.scraper import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/post-138981367"
    json = url_checker.get_assertation_as_json(
        url=url, test_suffix_for_caching=test_suffix_for_caching
    )

    assert_expected_inline(
        json,
        """\
{
    "post": "Normal lah, jin happy collect money then throw tile liao ... then forget pu one tile xiao xiang gong",
    "credit": "2022 Jan 4, Bunknifer. HardwareZone, \\"Noob mahjong question - experts please help\\". https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/post-138981367"
}""",
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/"
    json = url_checker.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "post": "Noob mahjong question - experts please help<br>Let\\u2019s say I \\u542c \\u516d\\u4e07 \\u4e5d\\u4e07\\u3002Someone throws \\u4e5d\\u4e07 I didn\\u2019t see or missed. Then in the same round the next player throws \\u516d\\u4e07\\uff0ccan I game?",
    "credit": "2022 Jan 3, gytaci. HardwareZone, \\"Noob mahjong question - experts please help\\". https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/"
}""",
    )


def test_replace_ellipses_with_ascii() -> None:
    test_suffix_for_caching = "ellipses"
    url = "https://forums.hardwarezone.com.sg/threads/sg-soon-no-need-water-from-malaysia-liao.7105036/post-155324874"
    json = url_checker.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "post": "If we have sufficient solar electricity or nuclear power generator... we can have endless supply of water...<br>We are limited by energy...",
    "credit": "2025 Feb 15, Can Or Not. HardwareZone, \\"SG soon no need water from malaysia liao\\". https://forums.hardwarezone.com.sg/threads/sg-soon-no-need-water-from-malaysia-liao.7105036/post-155324874"
}""",
    )
