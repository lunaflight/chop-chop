from expecttest import assert_expected_inline

from tests.scraper import src_interfacer


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/"

    json = src_interfacer.get_assertation_as_json(
        url=url, test_suffix_for_caching=test_suffix_for_caching
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "What Was The Last Song You Were Listening To?<br>So what was the last song you listened to?<br>If you have the youtube link,just copy the URL and paste it in your comment.If you're using the quick reply,paste the link inside the quick reply box and click 'More Reply Options',and the youtube link would automatically be embedded.<br>Like this :<br>http://www.youtube.com/watch?v=07MiAg2vZt0<br>If not,just state the song name and artist,like this :<br>Artist - Song Name<br>Start sharing!",
    "src": "2011 Nov 10, DriveMe. Blowing Wind, \\"What Was The Last Song You Were Listening To?\\". https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/"
}""",
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/?do=findComment&comment=338321"

    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Perfect to get drunk to.",
    "src": "2011 Nov 11, jeeves. Blowing Wind, \\"What Was The Last Song You Were Listening To?\\". https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/?do=findComment&comment=338321"
}""",
    )


def test_guest_username() -> None:
    test_suffix_for_caching = "guest_username"
    url = "https://www.blowingwind.io/forum/topic/120631-rant-about-bw-members-too/page/2/#comment-3143725"

    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "lao lang gei, mai kee siao la, u so old donno: rant = complain = dislike u ar???<br>now u sound like tt old foreign thrash steve - thick skin like donno wat nia.. aso sound like tt <stupid..lion> who oni think thr got oni 1 guest in this whole forum whr he mean all guest is the same 1 guest.. no wonder u old like aso act like them + make so many mistake nia..<br>but u wan think like this, up to u lo, other of rant guest here abt u will laugh die me like me lo.. i no time follow u, got better nice mbr to follow den u.. lol",
    "src": "2023 May 11, Guest guest. Blowing Wind, \\"rant about bw members too\\". https://www.blowingwind.io/forum/topic/120631-rant-about-bw-members-too/page/2/#comment-3143725"
}""",
    )
