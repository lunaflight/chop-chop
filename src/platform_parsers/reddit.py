from bs4 import BeautifulSoup
from platform_parsers import format, soup_cacher, url_fetcher
from datetime import datetime
from urllib.parse import urlparse, urlunparse
import logging


class T:
    # The old URL is used for more stable parsing.
    def __init__(self, modern_url: str, soup_from_old: BeautifulSoup) -> None:
        self.soup_from_old = soup_from_old
        self.modern_url = modern_url

    # TODO: The following does not work well on multi-line comments.
    # [https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9fl4g/]
    def post(self) -> str:
        return self.soup_from_old\
            .find('div', {'data-type': 'comment'})\
            .find('div', class_='usertext-body')\
            .find_all('p')[0]\
            .get_text()

    def subreddit(self) -> str:
        path = urlparse(self.modern_url).path.split('/')
        return path[path.index('r') + 1]

    def timestamp(self) -> datetime:
        datetime_str = self.soup_from_old\
            .find('div', {'data-type': 'comment'})\
            .find('p', class_='tagline')\
            .find('time')['datetime']
        return datetime.fromisoformat(datetime_str)

    def title(self) -> str:
        title_tag = self.soup_from_old\
            .find('a', {'data-event-action': 'title'})
        return title_tag.text

    def username(self) -> str:
        return self.soup_from_old\
            .find('div', {'data-type': 'comment'})\
            .find('p', class_='tagline')\
            .find('a', class_='author')\
            .text

    def credit(self) -> str:
        return format.online_with_title(
            timestamp=self.timestamp(),
            name=f'u/{self.username()}',
            platform_name=f'r/{self.subreddit()}',
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


def is_permalink(url: str) -> bool:
    path_with_empty_strs = urlparse(url).path.split("/")
    path = [segment for segment in path_with_empty_strs if segment]
    # Permalink paths are of the form:
    # [r, subreddit, comments, id, title, comment_id]
    return path.index("comments") + 4 == len(path)


def of_url(url: str) -> T:
    if not is_permalink(url):
        logging.error("Expected a permalink to the comment.")
        raise ValueError("Invalid URL: Expected a permalink to the comment.")

    old_url = old_url_of_url(url)
    modern_url = modern_url_of_url(url)
    soup_from_old = url_fetcher.get_soup(old_url)
    return T(modern_url=modern_url, soup_from_old=soup_from_old)


def mock() -> T:
    url = ("https://www.reddit.com/r/singapore/comments/1o58jy5/"
           "growing_old_alone_in_singapore_why_these_single/nj81rwn/")
    platform = "reddit"

    cached_soup = soup_cacher.read(platform)
    if not cached_soup:
        cached_soup = of_url(url).soup_from_old
        soup_cacher.cache(platform, cached_soup)

    return T(modern_url=url, soup_from_old=cached_soup)
