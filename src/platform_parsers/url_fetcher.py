import logging
import time

import requests
from bs4 import BeautifulSoup
from real_headers import real_headers

LOGGER = logging.getLogger(__name__)

OK_RESPONSE = 200
TOO_MANY_REQUESTS = 429

DEFAULT_RETRY_AFTER_DELAY_SEC = 5


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=real_headers(), timeout=10)

    if response.status_code != OK_RESPONSE:
        retry_after_delay = int(response.headers.get("Retry-After"))\
            if response.status_code == TOO_MANY_REQUESTS\
            else DEFAULT_RETRY_AFTER_DELAY_SEC
        LOGGER.debug("Received bad status code. Trying after delay.",
                      extra={response.status_code, retry_after_delay})
        time.sleep(retry_after_delay)
        return get_soup(url)

    return BeautifulSoup(response.text, "html.parser")
