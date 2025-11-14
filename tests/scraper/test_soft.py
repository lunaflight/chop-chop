from expecttest import assert_expected_inline

from tests.scraper import src_interfacer


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://soft.com.sg/threads/childhood-jeers.6640/#post-108928"
    json = src_interfacer.get_assertation_as_json(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
    )

    assert_expected_inline(
        json,
        """\
{
    "post": "haha...suddenly remembered more...<br>Copy cat, kiss the rat, go home let your mother slap, father say, \\"nevermind\\". Mother say, \\"Go and die!\\"<br>i learnt that in kindergarten, then when i recited it at home, my mum was appalled, and told me not to chant it anymore...lol!",
    "credit": "2005 Oct 30, MichaelAngelo. S.O.F.T., \\"Childhood jeers\\". https://soft.com.sg/threads/childhood-jeers.6640/#post-108928"
}""",
    )
