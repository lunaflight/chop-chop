import logging
from datetime import datetime
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup, Tag

from src.scraper import (
    assertation,
    body_format,
    citation_format,
    url_fetcher,
)

LOGGER = logging.getLogger(__name__)

COOKIES = {
    # Required to bypass an over 18 confirmation screen
    "over18": "1"
}


def narrow_soup(soup: BeautifulSoup, *, is_reply: bool) -> Tag | None:
    if is_reply:
        return soup.find("div", {"data-type": "comment"})

    return soup.find("div", class_="sitetable")


class T:
    # The old URL is used for more stable parsing.
    def __init__(
        self,
        modern_url: str,
        soup_from_old: BeautifulSoup,
        *,
        is_reply: bool,
    ) -> None:
        self.soup_from_old = soup_from_old
        self.modern_url = modern_url
        self.is_reply = is_reply

    def post(self) -> str:
        try:
            body_with_children = (
                narrow_soup(  # type: ignore[union-attr]
                    self.soup_from_old, is_reply=self.is_reply
                )
                .find("div", class_="usertext-body")
                .find("div")
            )
        except AttributeError:
            body_with_children = None
        assert isinstance(body_with_children, Tag | None)

        return body_format.create(
            title=self.title(),
            body_with_children=body_with_children,
            is_reply=self.is_reply,
            only_use_br_as_line_break=False,
        )

    def subreddit(self) -> str:
        path = urlparse(self.modern_url).path.split("/")
        return path[path.index("r") + 1]

    def timestamp(self) -> datetime:
        datetime_str = (
            narrow_soup(  # type: ignore[union-attr]
                self.soup_from_old, is_reply=self.is_reply
            )
            .find("p", class_="tagline")
            .find("time")
            .get("datetime")
        )
        assert isinstance(datetime_str, str)

        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        return self.soup_from_old.find("a", {"data-event-action": "title"}).text  # type: ignore[union-attr]

    def username(self) -> str:
        try:
            username = (
                narrow_soup(  # type: ignore[union-attr]
                    self.soup_from_old, is_reply=self.is_reply
                )
                .find("p", class_="tagline")
                .find("a", class_="author")
                .text
            )
            username = f"u/{username}"
        except AttributeError:
            username = "Deleted User"

        return username

    def credit(self) -> str:
        return citation_format.online_with_title(
            timestamp=self.timestamp(),
            name=self.username(),
            platform_name=f"r/{self.subreddit()}",
            title=self.title(),
            url=self.modern_url,
        )

    def assertation(self) -> assertation.T:
        return assertation.create(post=self.post(), credit=self.credit())


def replace_netloc_of_url(url: str, netloc: str) -> str:
    if not urlparse(url).scheme:
        url = "https://" + url

    parsed_url = urlparse(url)._replace(netloc=netloc)
    return urlunparse(parsed_url)


def old_url_of_url(url: str) -> str:
    return replace_netloc_of_url(url, netloc="old.reddit.com")


def modern_url_of_url(url: str) -> str:
    return replace_netloc_of_url(url, netloc="www.reddit.com")


def is_reply_if_permalink(url: str) -> bool:
    path_with_empty_strs = urlparse(url).path.split("/")
    path = [segment for segment in path_with_empty_strs if segment]
    # Permalink paths are of the form:
    # [r, subreddit, comments, id, title, comment_id] noqa: ERA001
    return path.index("comments") + 4 == len(path)


def of_url_with_soup(url: str, soup_from_old: BeautifulSoup) -> T:
    modern_url = modern_url_of_url(url)
    is_reply = is_reply_if_permalink(url)
    return T(
        modern_url=modern_url, soup_from_old=soup_from_old, is_reply=is_reply
    )


def of_url(url: str) -> T:
    old_url = old_url_of_url(url)
    soup_from_old = url_fetcher.get_soup(old_url, cookies=COOKIES)
    return of_url_with_soup(url=url, soup_from_old=soup_from_old)
