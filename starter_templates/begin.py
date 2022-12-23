#!/usr/bin/env python3

import logging
import os
import sys

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
# noinspection PyPep8
from downloader import Downloader


@click.command()
@click.option('--session', type=str, required=True, help="Session cookie required to downloader the input from AOC.")
def main(session):
    """General entry point for solutions."""
    logging.basicConfig(level=logging.NOTSET, format="%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S%z")

    # Fill in specifics for the year and the day that you are working on.
    aoc_downloader = Downloader(year=0, day=0, cookie_list=[('session', session), ])
    aoc_downloader.download_input(destination=os.path.dirname(__file__))

    # logger = logging.getLogger()

    # If you want to log the output:
    # logger.debug(aoc_downloader.input_data)

    # Place the code to run the solution with the downloaded input after this line:
    # solution = Solution(aoc_downloader.input_data)


if __name__ == '__main__':
    main()
