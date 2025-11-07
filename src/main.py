#!/usr/bin/env python3

import io
import logging
import os
import sys
from argparse import ArgumentParser

from src.platform_parsers import assertation, platform

# Windows only UTF-8 fix
if os.name == "nt":
    sys.stdin = io.TextIOWrapper(
        sys.stdin.buffer, encoding="utf-8", errors="replace"
    )
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace"
    )


def escape_double_apostrophe(string: str) -> str:
    return string.replace('"', '\\"')


def read_url_from_stdin() -> assertation.T:
    # clean up nonsense \ufeff chars (else throws error on windows)
    url = input().strip()
    while url.startswith("\ufeff"):
        url = url[len("\ufeff") :]
    url = (
        url.encode("utf-8", "ignore")
        .decode("utf-8", errors="ignore")
        .lstrip("\ufeff")
    )

    platform_ = platform.of_url(url)
    return platform.get_assertation(platform_)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--enable-logging",
        action="store_true",
        help="Enable logging for debugging",
    )
    args = parser.parse_args()

    if args.enable_logging:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig(level=logging.WARNING)

    assertation_ = read_url_from_stdin()
    post = assertation_.post
    credit = assertation_.credit

    # Rudimentary formatting is done by printing twice, to separate the
    # [eg] string onto a single line for easier string manipulation in VIM.
    print(  # noqa: T201
        f'{{ "eg": "{escape_double_apostrophe(post)}",'
    )
    print(  # noqa: T201
        f'"src": "{escape_double_apostrophe(credit)}" }}'
    )


if __name__ == "__main__":
    main()
