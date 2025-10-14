from bs4 import BeautifulSoup, NavigableString
from platform_parsers import (format,
                              platform,
                              soup_cacher,
                              url_fetcher)
from datetime import datetime
from urllib.parse import urlparse
import logging
from typing import Optional


# Returns the post_id in the format [post-NNNNN]
def post_id(url: str) -> Optional[str]:
    # Sometimes, it is located as a fragment at the end of the URL,
    post_id = urlparse(url).fragment

    # Other times, it is just the final segment in the path.
    if not post_id:
        post_id = urlparse(url).path.split('/')[-1]

    if not post_id.startswith("post-"):
        return None

    return post_id


class T:
    def __init__(self,
                 stylised_platform: str,
                 url: str,
                 soup: BeautifulSoup) -> None:
        self.stylised_platform = stylised_platform
        self.post_id = post_id(url)
        self.soup = soup
        self.url = url

    def post(self) -> str:
        contents = self.soup\
            .find('article', {'data-content': f"{self.post_id}"})\
            .find('article', class_="message-body")\
            .find('div', class_="bbWrapper")\
            .contents

        paragraphs = []
        for content in contents:
            if isinstance(content, NavigableString) and str(content).strip():
                paragraphs.append(str(content.strip()))

        return "<br>".join(paragraphs)

    def timestamp(self) -> datetime:
        datetime_str = self.soup\
            .find('article', {'data-content': f"{self.post_id}"})\
            .find('time')['datetime']
        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        return self.soup\
            .find('h1', class_="p-title-value")\
            .text

    def username(self) -> str:
        return self.soup\
            .find('article', {'data-content': f"{self.post_id}"})\
            .find('section', class_="message-user")\
            .find('a', class_="username")\
            .text

    def credit(self) -> str:
        return format.online_with_title(
            timestamp=self.timestamp(),
            name=self.username(),
            platform_name=self.stylised_platform,
            title=self.title(),
            url=self.url)


def of_url(url: str) -> T:
    if not post_id(url):
        logging.error("Expected a permalink to the comment.")
        raise ValueError("Invalid URL: Expected a permalink to the comment.")

    soup = url_fetcher.get_soup(url)
    stylised_platform = platform.to_stylised_string(platform.of_url(url))
    return T(stylised_platform=stylised_platform, url=url, soup=soup)


def mock(mock_url: str, platform: str, stylised_platform: str) -> T:
    cached_soup = soup_cacher.read(platform)

    if not cached_soup:
        cached_soup = of_url(mock_url).soup
        soup_cacher.cache(platform, cached_soup)

    return T(stylised_platform=stylised_platform,
             url=mock_url,
             soup=cached_soup)


def mock_hardwarezone() -> T:
    mock_url = ("https://forums.hardwarezone.com.sg/threads/"
                "any-good-use-for-myactivesg-credits.7163585/#post-157582701")
    platform_str = platform.to_plain_string(platform.T.HARDWAREZONE)
    stylised_platform = platform.to_stylised_string(platform.T.HARDWAREZONE)

    return mock(mock_url=mock_url,
                platform=platform_str,
                stylised_platform=stylised_platform)


def mock_singaporebrides() -> T:
    mock_url = ("https://singaporebrides.com/weddingforum/threads/"
                "any-clubbers-out-there.1305/page-396#post-730029")
    platform_str = platform.to_plain_string(platform.T.SINGAPOREBRIDES)
    stylised_platform = platform.to_stylised_string(platform.T.SINGAPOREBRIDES)

    return mock(mock_url=mock_url,
                platform=platform_str,
                stylised_platform=stylised_platform)
