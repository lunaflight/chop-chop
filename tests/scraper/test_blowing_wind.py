from tests.scraper import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/"
    expected_post = "What Was The Last Song You Were Listening To?<br>So what was the last song you listened to?<br>If you have the youtube link,just copy the URL and paste it in your comment.If you're using the quick reply,paste the link inside the quick reply box and click 'More Reply Options',and the youtube link would automatically be embedded.<br>Like this :<br>http://www.youtube.com/watch?v=07MiAg2vZt0<br>If not,just state the song name and artist,like this :<br>Artist - Song Name<br>Start sharing!"  # noqa: E501
    expected_credit = (
        "2011 Nov 10, "
        "DriveMe. "
        "Blowing Wind, "
        '"What Was The Last Song You Were Listening To?". '
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
    url = "https://www.blowingwind.io/forum/topic/27903-what-was-the-last-song-you-were-listening-to/?do=findComment&comment=338321"
    expected_post = "Perfect to get drunk to."
    expected_credit = (
        "2011 Nov 11, "
        "jeeves. "
        "Blowing Wind, "
        '"What Was The Last Song You Were Listening To?". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
