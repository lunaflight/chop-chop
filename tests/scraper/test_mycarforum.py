from typing import TypedDict

from tests.scraper import url_checker


class ExpectedData(TypedDict):
    expected_post: str
    expected_credit: str
    test_suffix_for_caching: str


def get_expected_data_of_reply_2115341(url: str) -> ExpectedData:
    return {
        "expected_post": "yeah lor.. really hope so...<br>but mebbe not doing sea sports..<br>more likely spa etc..<br>hahaa<br>Wah, good way to relax!<br>C u there!!<br>Aiya!! I guess MCF should start selling member's T-shirt to support the forum, then all those going Bintan can hi to each other.",  # noqa: E501
        "expected_credit": (
            "2007 Nov 5, Davidcks. Mycarforum, "
            f'"Bring/Buy beer from SG to Bintan resorts?". {url}'
        ),
        "test_suffix_for_caching": "reply",
    }


def test_reply_directly_from_share() -> None:
    url = "https://www.mycarforum.com/forums/topic/2111034-bringbuy-beer-from-sg-to-bintan-resorts/?do=findComment&comment=2115341"
    expected_data = get_expected_data_of_reply_2115341(url)
    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=expected_data["test_suffix_for_caching"],
        expected_post=expected_data["expected_post"],
        expected_credit=expected_data["expected_credit"],
    )


def test_reply_directly_from_url_bar() -> None:
    url = "https://www.mycarforum.com/forums/topic/2111034-bringbuy-beer-from-sg-to-bintan-resorts/page/4/#comment-2115341"
    expected_data = get_expected_data_of_reply_2115341(url)
    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=expected_data["test_suffix_for_caching"],
        expected_post=expected_data["expected_post"],
        expected_credit=expected_data["expected_credit"],
    )


def test_main_post() -> None:
    test_suffix_for_caching = "topic"
    url = "https://www.mycarforum.com/forums/topic/2111034-bringbuy-beer-from-sg-to-bintan-resorts/"
    expected_post = (
        "Bring/Buy beer from SG to Bintan resorts?<br>Hi, I need advise "
        "from the experts who visit bintan resorts often. Me with some "
        "family and  friends are going over to bintan lagoon next long "
        "weekend.<br>And was told that beer are expensive there, so was "
        "wondering if it is a good idea to buy in SG and bring it across, "
        "or is there any duly free shops at TM ferry terminal to purchase "
        "from?? Someone told me that it is ok to bring a six pack each "
        "person into bintan, is this true?<br>Does anyone has any "
        "suggestion or advise?? 10q 10q."
    )
    expected_credit = (
        '2007 Nov 1, Davidcks. Mycarforum, "Bring/Buy beer from SG to '
        f'Bintan resorts?". {url}'
    )
    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
