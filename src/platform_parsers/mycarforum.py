from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, cast
from urllib.parse import parse_qs, urlparse

from src.platform_parsers import (
    assertation,
    bbcode_format,
    citation_format,
    platform,
    url_fetcher,
)

if TYPE_CHECKING:
    from bs4 import BeautifulSoup, Tag


def comment_id(url: str) -> int | None:
    try:
        query = urlparse(url).query
        post_id = parse_qs(query).get("comment", [])[0]
    except (AttributeError, IndexError):
        return None

    return int(post_id)


def narrow_soup_to_comment_id(
    soup: BeautifulSoup, comment_id: int | None
) -> Tag | None:
    if comment_id is None:
        return soup

    return soup.find("article", {"id": f"elComment_{comment_id}"})


class T:
    def __init__(
        self, stylised_platform: str, url: str, soup: BeautifulSoup
    ) -> None:
        self.stylised_platform = stylised_platform
        self.comment_id = comment_id(url)
        self.soup = soup
        self.url = url

    def post(self) -> str:
        contents = (
            narrow_soup_to_comment_id(
                # type: ignore[union-attr]
                soup=self.soup,
                comment_id=self.comment_id,
            )
            .find("div", class_="cPost_contentWrap")
            .find("div", {"data-role": "commentContent"})
            .find_all("p", recursive=False)
        )

        paragraphs = []

        if self.comment_id is None:
            paragraphs.append(self.title())

        body_paragraphs = cast("list[str]", [p.text for p in contents])

        paragraphs.extend(body_paragraphs)

        return bbcode_format.join_with_br(paragraphs)

    def timestamp(self) -> datetime:
        datetime_str = (
            narrow_soup_to_comment_id(
                # type: ignore[union-attr]
                soup=self.soup,
                comment_id=self.comment_id,
            )
            .find("time")
            .get("datetime")
        )
        assert isinstance(datetime_str, str)

        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        return (
            self.soup.find("h1", class_="ipsType_pageTitle")  # type: ignore[union-attr]
            .find("span")
            .find("span")
            .text
        )

    def username(self) -> str:
        return (
            narrow_soup_to_comment_id(
                # type: ignore[union-attr]
                soup=self.soup,
                comment_id=self.comment_id,
            )
            .find("h3", class_="cAuthorPane_author")
            .find("a")
            .text
        )

    def credit(self) -> str:
        return citation_format.online_with_title(
            timestamp=self.timestamp(),
            name=self.username(),
            platform_name=self.stylised_platform,
            title=self.title(),
            url=self.url,
        )

    def assertation(self) -> assertation.T:
        return assertation.T(post=self.post(), credit=self.credit())


def of_url_with_soup(url: str, soup: BeautifulSoup) -> T:
    stylised_platform = platform.to_stylised_string(platform.of_url(url))
    return T(stylised_platform=stylised_platform, url=url, soup=soup)


def of_url(url: str) -> T:
    soup = url_fetcher.get_soup(url)
    return of_url_with_soup(url=url, soup=soup)
