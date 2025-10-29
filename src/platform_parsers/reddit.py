import logging
from datetime import datetime
from typing import cast
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup, Tag

from platform_parsers import (
    bbcode_format,
    citation_format,
    platform,
    soup_cacher,
    url_fetcher,
)

LOGGER = logging.getLogger(__name__)


def narrow_soup_if_reply(soup: BeautifulSoup, *, is_reply: bool) -> Tag | None:
    if is_reply:
        return soup.find("div", {"data-type": "comment"})

    return soup.find("div", class_="content")


class T:
    # The old URL is used for more stable parsing.
    def __init__(self,
                 modern_url: str,
                 soup_from_old: BeautifulSoup,
                 *,
                 is_reply: bool,
                 ) -> None:
        self.soup_from_old = soup_from_old
        self.modern_url = modern_url
        self.is_reply = is_reply

    def post(self) -> str:
        paragraphs = [self.title()]

        body_paragraphs = (
            narrow_soup_if_reply(  # type: ignore[union-attr]
                self.soup_from_old, is_reply=self.is_reply)
            .find("div", class_="usertext-body")
            .find_all("p"))
        body_paragraphs = cast("list[str]", [p.text for p in body_paragraphs])

        paragraphs.extend(body_paragraphs)

        return bbcode_format.join_with_br(paragraphs)

    def subreddit(self) -> str:
        path = urlparse(self.modern_url).path.split("/")
        return path[path.index("r") + 1]

    def timestamp(self) -> datetime:
        datetime_str = (
            narrow_soup_if_reply(  # type: ignore[union-attr]
                self.soup_from_old, is_reply=self.is_reply)
            .find("p", class_="tagline")
            .find("time")
            .get("datetime"))
        assert isinstance(datetime_str, str)

        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        return (self.soup_from_old  # type: ignore[union-attr]
                .find("a", {"data-event-action": "title"})
                .text)

    def username(self) -> str:
        return (
            narrow_soup_if_reply(  # type: ignore[union-attr]
                self.soup_from_old, is_reply=self.is_reply)
            .find("p", class_="tagline")
            .find("a", class_="author")
            .text)

    def credit(self) -> str:
        return citation_format.online_with_title(
            timestamp=self.timestamp(),
            name=f"u/{self.username()}",
            platform_name=f"r/{self.subreddit()}",
            title=self.title(),
            url=self.modern_url)


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


def of_url(url: str) -> T:
    old_url = old_url_of_url(url)
    modern_url = modern_url_of_url(url)
    soup_from_old = url_fetcher.get_soup(old_url)
    is_reply = is_reply_if_permalink(url)
    return T(modern_url=modern_url,
             soup_from_old=soup_from_old,
             is_reply=is_reply)


def mock() -> T:
    url = ("https://www.reddit.com/r/singapore/comments/1o5i3fl/"
           "contract_for_marine_parade_free_shuttle_bus/nj9fl4g/")
    platform_str = platform.to_plain_string(platform.T.REDDIT)

    cached_soup = soup_cacher.read(platform_str)
    if not cached_soup:
        cached_soup = of_url(url).soup_from_old
        soup_cacher.cache(platform_str, cached_soup)

    return T(modern_url=url,
             soup_from_old=cached_soup,
             is_reply=is_reply_if_permalink(url))
