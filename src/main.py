#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from src.platform_parsers import platform


def escape_double_apostrophe(string: str) -> str:
    return string.replace('"', '\\"')


# TODO: This tuple should be labeled, a dictionary should be returned instead.
def read_url_from_stdin() -> tuple[str, str]:
    url = input()
    platform_ = platform.of_url(url)
    post = platform.post(platform_)
    credit = platform.credit(platform_)

    return (post, credit)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--enable-logging",
        action="store_true",
        help="Enable logging for debugging")
    args = parser.parse_args()

    if args.enable_logging:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)

    post, credit = read_url_from_stdin()

    print(f'{{ "eg": "{escape_double_apostrophe(post)}", '  # noqa: T201
          f'"src": "{escape_double_apostrophe(credit)}" }}')


if __name__ == "__main__":
    main()
