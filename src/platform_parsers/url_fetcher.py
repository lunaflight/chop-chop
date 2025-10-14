import logging
import time
import requests
from bs4 import BeautifulSoup
from real_headers import real_headers


OK_RESPONSE = 200
TOO_MANY_REQUESTS = 429

DEFAULT_RETRY_AFTER_DELAY_SEC = 5


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=real_headers())

    if response.status_code != OK_RESPONSE:
        retry_after_delay = int(response.headers.get('Retry-After'))\
            if response.status_code == TOO_MANY_REQUESTS\
            else DEFAULT_RETRY_AFTER_DELAY_SEC
        logging.debug(f"Received {response.status_code} status code. "
                      f"Trying again in {retry_after_delay}s.")
        time.sleep(retry_after_delay)
        return get_soup(url)

    return BeautifulSoup(response.text, 'html.parser')
