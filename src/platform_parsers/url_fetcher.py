import logging
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

LOGGER = logging.getLogger(__name__)

OK_RESPONSE = 200
TOO_MANY_REQUESTS = 429

DEFAULT_RETRY_AFTER_DELAY_SEC = 5

USER_AGENT = UserAgent()

HEADERS = {"User-Agent": USER_AGENT.random}


def get_soup(url: str, cookies: dict | None = None) -> BeautifulSoup:
    response = requests.get(
        url,
        headers=HEADERS,
        cookies=cookies,
        timeout=DEFAULT_RETRY_AFTER_DELAY_SEC,
    )

    if response.status_code != OK_RESPONSE:
        retry_after_header = response.headers.get("Retry-After")
        retry_after_delay = (
            int(retry_after_header)
            if (
                response.status_code == TOO_MANY_REQUESTS
                and retry_after_header is not None
            )
            else DEFAULT_RETRY_AFTER_DELAY_SEC
        )
        LOGGER.debug(
            "Received bad status code. Trying after delay.",
            extra={
                "response": response.status_code,
                "retry_after_delay": retry_after_delay,
            },
        )
        time.sleep(retry_after_delay)
        return get_soup(url)

    return BeautifulSoup(response.text, "html.parser")
