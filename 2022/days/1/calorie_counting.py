#!/usr/bin/env python3
import os.path
import sys
import logging
from typing import Tuple

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from downloader import Downloader


class CalorieCounting(object):
    def __init__(self):
        self.logger = logging.getLogger(CalorieCounting.__name__)

        self.elves = []

    def calculate_elf_capacity(self, input_data) -> None:
        total = 0
        for entry in input_data:
            if entry.strip().isnumeric():
                total += int(entry)
            else:
                self.elves.append(total)
                total = 0

    @property
    def max_capacity(self) -> int:
        return max(self.elves)

    @property
    def max_capacity_tuple(self) -> Tuple[int, int, int]:
        sorted_capacities = sorted(self.elves)
        return sorted_capacities[-1], sorted_capacities[-2], sorted_capacities[-3]


@click.command()
@click.option('--session', type=str, required=True, help="Session cookie required to downloader the input from AOC.")
def main(session):
    """General entry point for solutions."""
    logging.basicConfig(level=logging.NOTSET, format="%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S%z")

    # Fill in specifics for the year and the day that you are working on.
    aoc_downloader = Downloader(year=2022, day=1, cookie_list=[('session', session), ])
    aoc_downloader.download_input(destination=os.path.dirname(__file__))

    logger = logging.getLogger()
    # Place the code to run the solution with the downloaded input after this line:

    calorie_counting = CalorieCounting()
    calorie_counting.calculate_elf_capacity(aoc_downloader.input_data)

    logger.info(calorie_counting.max_capacity)
    logger.info(calorie_counting.max_capacity_tuple)


if __name__ == '__main__':
    main()
