from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional
import logging

PATH_TO_HTML_CACHE = Path("src/platform_parsers/htmls_for_testing")


def path_of_platform(platform: str):
    return PATH_TO_HTML_CACHE / f"{platform}.html"


def cache(platform: str, soup: BeautifulSoup):
    file_path = path_of_platform(platform)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(str(soup), encoding='utf-8')
    logging.debug(f"Cached '{platform}' at: {file_path}")


def read(platform: str) -> Optional[BeautifulSoup]:
    file_path = path_of_platform(platform)
    if not file_path.is_file():
        logging.debug(f"Cache file not found for '{platform}' at: {file_path}")
        return None

    content = file_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    logging.debug(f"Cache retrieved successfully for '{platform}'.")
    return soup
