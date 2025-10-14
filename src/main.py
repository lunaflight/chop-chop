#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
import platform_parsers.reddit


def mock(platform):
    platform = platform.lower()
    if platform == 'reddit':
        credit = platform_parsers.reddit.mock().credit()
        print(credit)
    else:
        raise ValueError("Unknown platform: " + platform)


def read_url_from_stdin():
    url = input()
    if 'reddit' in url:
        credit = platform_parsers.reddit.of_url(url).credit()
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
