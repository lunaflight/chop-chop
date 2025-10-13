from bs4 import BeautifulSoup
from typing import Optional
from platform_parsers import format, url_fetcher
from datetime import datetime
from urllib.parse import urlparse, urlunparse


class T:
    # The old URL is used for more stable parsing.
    def __init__(self, modern_url: str, soup_from_old: BeautifulSoup) -> None:
        self.soup_from_old = soup_from_old
        self.modern_url = modern_url

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


def of_url(url: str, save_to_file: Optional[str] = None) -> T:
    old_url = old_url_of_url(url)
    modern_url = modern_url_of_url(url)
    soup_from_old = url_fetcher.get_soup(old_url, save_to_file=save_to_file)
    return T(modern_url=modern_url, soup_from_old=soup_from_old)


def mock() -> T:
    # TODO: Remove [--save-to-file] in [main.py] and have this populate the
    # mock if it is empty.
    url = ("https://www.reddit.com/r/singapore/comments/1o58jy5/"
           "growing_old_alone_in_singapore_why_these_single/nj81rwn/")
    with open("src/platform_parsers/htmls_for_testing/reddit.html",
              'r',
              encoding='utf-8') as file:
        soup_from_old = BeautifulSoup(file.read(), 'html.parser')
        return T(modern_url=url, soup_from_old=soup_from_old)
