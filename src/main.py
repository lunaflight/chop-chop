#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from src import sanitizer, windows_hacks
from src.platform_parsers import assertation, platform

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
    post = assertation_.post
    credit = assertation_.credit

    # Rudimentary formatting is done by printing twice, to separate the
    # [eg] string onto a single line for easier string manipulation in VIM.
    print(  # noqa: T201
        f'{{ "eg": "{sanitizer.escape_double_apostrophe(post)}",'
    )
    print(  # noqa: T201
        f'"src": "{sanitizer.escape_double_apostrophe(credit)}" }}'
    )


if __name__ == "__main__":
    main()
