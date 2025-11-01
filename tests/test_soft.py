from tests import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://soft.com.sg/threads/childhood-jeers.6640/#post-108928"
    expected_post = 'haha...suddenly remembered more...<br>Copy cat, kiss the rat, go home let your mother slap, father say, "nevermind". Mother say, "Go and die!"<br>i learnt that in kindergarten, then when i recited it at home, my mum was appalled, and told me not to chant it anymore...lol!'  # noqa: E501
    expected_credit = (
        f'2005 Oct 30, MichaelAngelo. S.O.F.T., "Childhood jeers". {url}'
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
