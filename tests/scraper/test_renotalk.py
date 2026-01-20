from expecttest import assert_expected_inline

from tests.scraper import src_interfacer


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://www.renotalk.com/forum/topic/11895-housewarming-invite/page/588/?tab=comments#comment-304037"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Actually my shoes too...i tend to wear until spoil until cannot spoil, mend until cannot mend anymore then i will she de throw away....cos not easy for me to like a pair of shoes and i dun really buy shoes that often...in short, too lazy....",
    "src": "2008 Jun 6, Air. RenoTalk, \\"Housewarming Invite\\". https://www.renotalk.com/forum/topic/11895-housewarming-invite/page/588/?tab=comments#comment-304037"
}""",
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://www.renotalk.com/forum/topic/11895-housewarming-invite/"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Housewarming Invite<br>Dear Friends!<br>Finally after putting up the pictures of my done-up place, I can call a chapter to this fabulous time spent in researching and chit-chatting with my RT friends. As i mentioned before in my RT blog... I won't be coming in much or even at all in the future, I've arranged a gathering over at my place during CNY.<br>I hope you guys and gals who have been tagged were able to receive the PM.<br>I didn't extend the invite to everyone my apologies because some ppl rather not attend. Do let me know if you can or cannot make it! or drop me a PM if you wanna come by but somehow you were not informed and i'll send you the details.<br>Cheers!",
    "src": "2008 Jan 6, Phantom. RenoTalk, \\"Housewarming Invite\\". https://www.renotalk.com/forum/topic/11895-housewarming-invite/"
}""",
    )
