#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from platform_parsers import platform, xenforo, reddit


def mock(platform_str):
    platform_str = platform_str.lower()
    if platform_str == platform.to_plain_string(platform.T.REDDIT):
        post = reddit.mock().post()
        credit = reddit.mock().credit()
    elif platform_str == platform.to_plain_string(platform.T.HARDWAREZONE):
        post = xenforo.mock_hardwarezone().post()
        credit = xenforo.mock_hardwarezone().credit()
    elif platform_str == platform.to_plain_string(platform.T.SINGAPOREBRIDES):
        post = xenforo.mock_singaporebrides().post()
        credit = xenforo.mock_singaporebrides().credit()
    elif platform_str == platform.to_plain_string(
            platform.T.SINGAPOREMOTHERHOOD):
        post = xenforo.mock_singaporemotherhood().post()
        credit = xenforo.mock_singaporemotherhood().credit()
    else:
        raise ValueError("Unknown platform: " + platform_str)

    print(post)
    print(credit)


def read_url_from_stdin():
    url = input()
    platform_type = platform.of_url(url)

    if platform.is_xenforo(platform_type):
        post = xenforo.of_url(url).post()
        credit = xenforo.of_url(url).credit()
    elif platform_type == platform.T.REDDIT:
        post = reddit.of_url(url).post()
        credit = reddit.of_url(url).credit()
    else:
        raise ValueError("Unknown platform")

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
        mock(platform_str=args.test_with_mock)
    else:
        read_url_from_stdin()


if __name__ == "__main__":
    main()
