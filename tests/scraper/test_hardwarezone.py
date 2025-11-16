from expecttest import assert_expected_inline

from tests.scraper import src_interfacer


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/post-138981367"
    json = src_interfacer.get_assertation_as_json(
        url=url, test_suffix_for_caching=test_suffix_for_caching
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Normal lah, jin happy collect money then throw tile liao ... then forget pu one tile xiao xiang gong",
    "src": "2022 Jan 4, Bunknifer. HardwareZone, \\"Noob mahjong question - experts please help\\". https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/post-138981367"
}""",
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Noob mahjong question - experts please help<br>Let's say I \\u542c \\u516d\\u4e07 \\u4e5d\\u4e07\\u3002Someone throws \\u4e5d\\u4e07 I didn't see or missed. Then in the same round the next player throws \\u516d\\u4e07\\uff0ccan I game?",
    "src": "2022 Jan 3, gytaci. HardwareZone, \\"Noob mahjong question - experts please help\\". https://forums.hardwarezone.com.sg/threads/noob-mahjong-question-experts-please-help.6672504/"
}""",
    )


def test_replace_ellipses_with_ascii() -> None:
    test_suffix_for_caching = "ellipses"
    url = "https://forums.hardwarezone.com.sg/threads/sg-soon-no-need-water-from-malaysia-liao.7105036/post-155324874"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "If we have sufficient solar electricity or nuclear power generator... we can have endless supply of water...<br>We are limited by energy...",
    "src": "2025 Feb 15, Can Or Not. HardwareZone, \\"SG soon no need water from malaysia liao\\". https://forums.hardwarezone.com.sg/threads/sg-soon-no-need-water-from-malaysia-liao.7105036/post-155324874"
}""",
    )


def test_italicised_text_is_captured() -> None:
    test_suffix_for_caching = "italics"
    url = "https://forums.hardwarezone.com.sg/threads/value-dollar-store-made-me-realised-how-overcharged-other-shops-are-no-referral-links.6020067/page-2755#post-155126288"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Which ish ok rah<br>Rike my fren also<br>Seasons $4.8 that time he loaded 1 carton. I also go load wif him.<br>Then yeos promo he loaded 1 carton again<br>Then milo $7.95 he loaded 2 cartons cos very chip<br>Then ytd he went all out. Ribena & 100+ he loaded 3 cartons!<br>Like wtf. Cos he complained to me he always feel itchy. Went health checkup the report number shows his sugar level on the high side. Like... yall know what I mean? This ish self-pwnz at its best riao",
    "src": "2025 Jan 26, addict951. HardwareZone, \\"Value dollar store made me realised how overcharged other shops are [NO referral links]\\". https://forums.hardwarezone.com.sg/threads/value-dollar-store-made-me-realised-how-overcharged-other-shops-are-no-referral-links.6020067/page-2755#post-155126288"
}""",
    )


def test_emoji_image_not_captured() -> None:
    test_suffix_for_caching = "emoji"
    url = "https://forums.hardwarezone.com.sg/threads/value-dollar-store-made-me-realised-how-overcharged-other-shops-are-no-referral-links.6020067/post-155126104"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "assuming we didn't buy any other drinks",
    "src": "2025 Jan 26, ezowulf. HardwareZone, \\"Value dollar store made me realised how overcharged other shops are [NO referral links]\\". https://forums.hardwarezone.com.sg/threads/value-dollar-store-made-me-realised-how-overcharged-other-shops-are-no-referral-links.6020067/post-155126104"
}""",
    )
