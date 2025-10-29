from __future__ import annotations

import logging
from pathlib import Path

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

PATH_TO_HTML_CACHE = Path("src/platform_parsers/htmls_for_testing")


def path_of_platform(platform: str) -> Path:
    return PATH_TO_HTML_CACHE / f"{platform}.html"


def cache(platform: str, soup: BeautifulSoup) -> None:
    file_path = path_of_platform(platform)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(str(soup), encoding="utf-8")
    LOGGER.debug("Cached file successfully",
                  extra={platform, file_path})


def read(platform: str) -> BeautifulSoup | None:
    file_path = path_of_platform(platform)
    if not file_path.is_file():
        LOGGER.debug("Cache file not found",
                      extra={platform, file_path})
        return None

    content = file_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    LOGGER.debug("Cache retrieved successfully",
                  extra={platform})
    return soup
