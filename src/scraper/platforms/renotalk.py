import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, Tag

from src.scraper import (
    assertation,
    body_format,
    citation_format,
    platform,
    url_fetcher,
)


def post_id(url: str) -> str | None:
    parsed_url = urlparse(url)

    # .../?tab=comments#comment-NNNNN
    if parsed_url.fragment:
        fragment_match = re.search(r"comment-(\d+)", parsed_url.fragment)
        if fragment_match:
            return fragment_match.group(1)

    # .../?do=findComment&comment=NNNNN
    query_params = parse_qs(parsed_url.query)

    if "comment" in query_params:
        # Take the first comment parameter value
        return str(query_params["comment"][0])

    return None


def narrow_soup_to_post_id(
    soup: BeautifulSoup, post_id: str | None
) -> Tag | None:
    if post_id is None:
        return soup

    return soup.find("article", {"id": f"elComment_{post_id}"})


class T:
    def __init__(
        self, stylised_platform: str, url: str, soup: BeautifulSoup
    ) -> None:
        self.stylised_platform = stylised_platform
        self.post_id = post_id(url)
        self.soup = soup
        self.url = url

    def post(self) -> str:
        body_with_children = narrow_soup_to_post_id(
            # type: ignore[union-attr]
            soup=self.soup,
            post_id=self.post_id,
        ).find("div", {"data-role": "commentContent"})
        assert isinstance(body_with_children, Tag)

        return body_format.create(
            title=self.title(),
            body_with_children=body_with_children,
            is_reply=self.post_id is not None,
            only_use_br_as_line_break=False,
        )

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
        return self.soup.find("h1", class_="ipsType_pageTitle").get_text(  # type: ignore[union-attr]
            strip=True
        )

    def username(self) -> str:
        return (
            narrow_soup_to_post_id(
                # type: ignore[union-attr]
                soup=self.soup,
                post_id=self.post_id,
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
        return assertation.create(post=self.post(), credit=self.credit())


def of_url_with_soup(url: str, soup: BeautifulSoup) -> T:
    stylised_platform = platform.to_stylised_string(platform.of_url(url))
    return T(stylised_platform=stylised_platform, url=url, soup=soup)


def of_url(url: str) -> T:
    soup = url_fetcher.get_soup(url)
    return of_url_with_soup(url=url, soup=soup)
