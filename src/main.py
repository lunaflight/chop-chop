#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from src import sanitizer, windows_hacks
from src.scraper import assertation, platform

windows_hacks.set_stdin_stdout_encoding_if_windows()


def read_url_from_stdin() -> assertation.T:
    url = sanitizer.clean_input_for_utf8_compatibility(input())

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

    print(assertation.to_json(assertation_))  # noqa: T201


if __name__ == "__main__":
    main()
