#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from platform_parsers import xenforo, reddit


def mock(platform):
    platform = platform.lower()
    if platform == 'reddit':
        post = reddit.mock().post()
        credit = reddit.mock().credit()
    elif platform == 'hwz':
        post = xenforo.mock_hardwarezone().post()
        credit = xenforo.mock_hardwarezone().credit()
    elif platform == 'sgb':
        post = xenforo.mock_singaporebrides().post()
        credit = xenforo.mock_singaporebrides().credit()
    else:
        raise ValueError("Unknown platform: " + platform)

    print(post)
    print(credit)


def read_url_from_stdin():
    url = input()
    if 'reddit.com' in url:
        post = reddit.of_url(url).post()
        credit = reddit.of_url(url).credit()
    elif 'hardwarezone.com.sg' in url or 'singaporebrides.com' in url:
        post = xenforo.of_url(url).post()
        credit = xenforo.of_url(url).credit()

    print(post)
    print(credit)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--test-with-mock',
        type=str,
        metavar='PLATFORM',
        help='Use saved HTMLs instead of stdin, for testing purposes')
    parser.add_argument(
        '--enable-logging',
        action='store_true',
        help='Enable logging for debugging')
    args = parser.parse_args()

    if args.enable_logging:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING)

    if args.test_with_mock:
        mock(platform=args.test_with_mock)
    else:
        read_url_from_stdin()


if __name__ == "__main__":
    main()
