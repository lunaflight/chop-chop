from expecttest import assert_expected_inline

from tests.scraper import src_interfacer


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://www.bmw-sg.com/forums/threads/satay-outing-charity-drive-club-sandy-12-june-2008.18962/page-11#post-279351"
    json = src_interfacer.get_assertation_as_json(
        url=url, test_suffix_for_caching=test_suffix_for_caching
    )

    assert_expected_inline(
        json,
        """\
{
    "eg": "Re: Satay outing - Charity Drive - Club Sandy - 12 June 2008<br>I dunno if bobby's joke good anot, my china not powerful, he too chim for me.<br>but all i need to do is look at his shoes, for sure make me laugh",
    "src": "2008 Jun 12, phil. BMW.SG, \\"Satay outing - Charity Drive - Club Sandy - 12 June 2008\\". https://www.bmw-sg.com/forums/threads/satay-outing-charity-drive-club-sandy-12-june-2008.18962/page-11#post-279351"
}""",
    )
