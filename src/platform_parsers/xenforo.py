from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

from src.platform_parsers import (
    assertation,
    bbcode_format,
    citation_format,
    platform,
    url_fetcher,
)


# Returns the post_id in the format [post-NNNNN]
def post_id(url: str) -> str | None:
    # Sometimes, it is located as a fragment at the end of the URL,
    post_id = urlparse(url).fragment

    # Other times, it is just the final segment in the path.
    if not post_id:
        post_id = urlparse(url).path.split("/")[-1]

    if not post_id.startswith("post-"):
        return None

    return post_id


def narrow_soup_to_post_id(
    soup: BeautifulSoup, post_id: str | None
) -> Tag | None:
    if post_id is None:
        return soup

    return soup.find("article", {"data-content": f"{post_id}"})


class T:
    def __init__(
        self, stylised_platform: str, url: str, soup: BeautifulSoup
    ) -> None:
        self.stylised_platform = stylised_platform
        self.post_id = post_id(url)
        self.soup = soup
        self.url = url

    def post(self) -> str:
        contents = (
            narrow_soup_to_post_id(
                # type: ignore[union-attr]
                soup=self.soup,
                post_id=self.post_id,
            )
            .find("article", class_="message-body")
            .find("div", class_="bbWrapper")
            .contents
        )

        paragraphs = []

        if self.post_id is None:
            paragraphs.append(self.title())

        # Emojis, which are embed as images in the HTML, may be present.
        paragraphs += [
            str(content.strip())
            for content in contents
            if isinstance(content, NavigableString) and str(content).strip()
        ]

        return bbcode_format.join_with_br(paragraphs)

    def timestamp(self) -> datetime:
        datetime_str = (
            narrow_soup_to_post_id(
                # type: ignore[union-attr]
                soup=self.soup,
                post_id=self.post_id,
            )
            .find("time")
            .get("datetime")
        )
        assert isinstance(datetime_str, str)

        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        return self.soup.find("h1", class_="p-title-value").text  # type: ignore[union-attr]

    def username(self) -> str:
        return (
            narrow_soup_to_post_id(
                # type: ignore[union-attr]
                soup=self.soup,
                post_id=self.post_id,
            )
            .find("section", class_="message-user")
            .find("a", class_="username")
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
