from __future__ import annotations

import logging
from pathlib import Path

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

PATH_TO_HTML_CACHE = Path("tests/cached_htmls")


def path(filename: str) -> Path:
    return PATH_TO_HTML_CACHE / f"{filename}.html"


def cache(filename: str, soup: BeautifulSoup) -> None:
    file_path = path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(str(soup), encoding="utf-8")
    LOGGER.debug(
        "Cached file successfully",
        extra={"filename_": filename, "file_path": file_path},
    )


def read(filename: str) -> BeautifulSoup | None:
    file_path = path(filename)
    if not file_path.is_file():
        LOGGER.debug(
            "Cache file not found",
            extra={"filename_": filename, "file_path": file_path},
        )
        return None

    content = file_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    LOGGER.debug("Cache retrieved successfully", extra={"filename_": filename})
    return soup
