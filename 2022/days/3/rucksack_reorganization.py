#!/usr/bin/env python3

import logging
import os
import sys
from typing import List

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
# noinspection PyPep8
from downloader import Downloader


class RuckSackOrganizer(object):

    LOWERCASE_DELIMITER: int = 96
    UPPERCASE_DELIMITER: int = 64

    LOWERCASE_PRIORITY_DIFF: int = 96
    UPPERCASE_PRIORITY_DIFF: int = 38

    LETTERS_IN_ALPHABET: int = 26

    def __init__(self):
        self._logger = logging.getLogger(RuckSackOrganizer.__name__)
        self._rucksacks: list[RuckSackOrganizer.RuckSack] = []

    class Compartment(object):
        pass

    class RuckSack(object):
        def __init__(self, *, left_compartment: list[str], right_compartment: list[str]):
            self._item_counts: dict[str, int] = {}

            self._left_compartment = left_compartment
            self._right_compartment = right_compartment

        def find_items_types_found_across_compartments(self) -> None:
            for item in self._left_compartment:
                if item not in self._item_counts:
                    self._item_counts[item] = 1
                else:
                    self._item_counts[item] += 1
            for item in self._right_compartment:
                if item not in self._item_counts:
                    self._item_counts[item] = 1
                else:
                    self._item_counts[item] += 1

        @property
        def item_counts(self):
            return self._item_counts

        @property
        def left_compartment(self):
            return self._left_compartment

        @property
        def right_compartment(self):
            return self._right_compartment


    def process_input_data(self, input_data: List[str]) -> None:
        self._logger.info(f"Processing {len(input_data)} line(s).")
        for line in input_data:
            rucksack_line: str = line.strip()
            left_compartment = list(rucksack_line[:int(len(rucksack_line) / 2)])
            right_compartment = list(rucksack_line[int(len(rucksack_line) / 2):])

            rucksack = RuckSackOrganizer.RuckSack(left_compartment=left_compartment,
                                                  right_compartment=right_compartment)
            rucksack.find_items_types_found_across_compartments()

            self._rucksacks.append(rucksack)

    @staticmethod
    def get_item_priority(item: str) -> int:
        # Lowercase item types a through z have priorities 1 through 26.
        # Uppercase item types A through Z have priorities 27 through 52.
        utf_code = ord(item)
        if RuckSackOrganizer.LOWERCASE_DELIMITER < utf_code < RuckSackOrganizer.LOWERCASE_DELIMITER + \
                RuckSackOrganizer.LETTERS_IN_ALPHABET:
            # Lower case letter, subtract 96 to get priority.:
            return utf_code - RuckSackOrganizer.LOWERCASE_PRIORITY_DIFF
        elif RuckSackOrganizer.UPPERCASE_DELIMITER < utf_code < RuckSackOrganizer.UPPERCASE_PRIORITY_DIFF + \
                RuckSackOrganizer.LETTERS_IN_ALPHABET:
            # Upper case letter, subtract 38 to get the priority:
            return utf_code - RuckSackOrganizer.UPPERCASE_PRIORITY_DIFF
        else:
            raise RuntimeError(f"Unrecognized item {item}!")

    @property
    def rucksacks(self):
        return self._rucksacks


@click.command()
@click.option('--session', type=str, required=True, help="Session cookie required to downloader the input from AOC.")
def main(session):
    """General entry point for solutions."""
    logging.basicConfig(level=logging.NOTSET, format="%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S%z")

    # Fill in specifics for the year and the day that you are working on.
    aoc_downloader = Downloader(year=2022, day=3, cookie_list=[('session', session), ])
    aoc_downloader.download_input(destination=os.path.dirname(__file__))

    logger = logging.getLogger()

    # If you want to log the output:
    # logger.debug(aoc_downloader.input_data)

    # Place the code to run the solution with the downloaded input after this line:
    solution = RuckSackOrganizer()
    solution.process_input_data(aoc_downloader.input_data)

    for rucksack in solution.rucksacks:
        logger.info((rucksack.left_compartment, str.join(rucksack.right_compartment)))
        for item_stat in rucksack.item_counts.items():
            logger.info(item_stat)


if __name__ == '__main__':
    main()
