#!/usr/bin/env python3

import logging
import os
import sys
from typing import List

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
# noinspection PyPep8
from downloader import Downloader


class RuckSackOrganizer(object):
    LOWERCASE_DELIMITER: int = 96
    UPPERCASE_DELIMITER: int = 64

    LOWERCASE_PRIORITY_DIFF: int = 96
    UPPERCASE_PRIORITY_DIFF: int = 38

    LETTERS_IN_ALPHABET: int = 26

    ELVES_PER_GROUP: int = 3

    def __init__(self):
        self._logger = logging.getLogger(RuckSackOrganizer.__name__)
        self._rucksacks: list[RuckSackOrganizer.RuckSack] = []

        self._groups: list[
            tuple[RuckSackOrganizer.RuckSack, ...]
        ] = []

        self._group_intersections: list[list[str]] = []

    class RuckSack(object):
        def __init__(self, *, rucksack_line: str):
            self._item_intersection: list[str] = []

            self._rucksack_line = rucksack_line

            self._left_compartment = list(rucksack_line[:int(len(rucksack_line) / 2)])
            self._right_compartment = list(rucksack_line[int(len(rucksack_line) / 2):])

        def find_items_types_found_across_compartments(self) -> None:
            # Grab the intersection between the compartments:
            for item in list(set(self._left_compartment) & set(self._right_compartment)):
                self._item_intersection.append(item)

        @property
        def item_intersections(self) -> list[str]:
            return self._item_intersection

        @property
        def rucksack_line(self) -> str:
            return self._rucksack_line

        @property
        def left_compartment(self) -> list[str]:
            return self._left_compartment

        @property
        def right_compartment(self) -> list[str]:
            return self._right_compartment

    def process_input_data(self, input_data: List[str]) -> None:
        self._logger.info(f"Processing {len(input_data)} line(s).")
        for line in input_data:
            rucksack_line: str = line.strip()

            rucksack = RuckSackOrganizer.RuckSack(rucksack_line=rucksack_line)
            rucksack.find_items_types_found_across_compartments()

            self._rucksacks.append(rucksack)

    def divide_rucksacks(self) -> None:
        current_group: list[RuckSackOrganizer.RuckSack] = []
        for rucksack in self._rucksacks:
            current_group.append(rucksack)
            if len(current_group) == RuckSackOrganizer.ELVES_PER_GROUP:
                self._groups.append(tuple(current_group))
                current_group = []

    def find_intersections_across_groups(self) -> None:
        for first, second, third in self._groups:
            self._group_intersections.append(
                list(set(first.rucksack_line) & set(second.rucksack_line) & set(third.rucksack_line))
            )

    @staticmethod
    def get_item_priority(item: str) -> int:
        # Lowercase item types a through z have priorities 1 through 26.
        # Uppercase item types A through Z have priorities 27 through 52.
        utf_code = ord(item)
        if RuckSackOrganizer.LOWERCASE_DELIMITER < utf_code <= RuckSackOrganizer.LOWERCASE_DELIMITER + \
                RuckSackOrganizer.LETTERS_IN_ALPHABET:
            # Lower case letter, subtract 96 to get priority:
            return utf_code - RuckSackOrganizer.LOWERCASE_PRIORITY_DIFF
        elif RuckSackOrganizer.UPPERCASE_DELIMITER < utf_code <= RuckSackOrganizer.UPPERCASE_DELIMITER + \
                RuckSackOrganizer.LETTERS_IN_ALPHABET:
            # Upper case letter, subtract 38 to get the priority:
            return utf_code - RuckSackOrganizer.UPPERCASE_PRIORITY_DIFF
        else:
            raise RuntimeError(f"Unrecognized item {item}, {ord(item)}!")

    @property
    def rucksacks(self):
        return self._rucksacks

    @property
    def group_intersections(self):
        return self._group_intersections


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

    sum_of_compartment_priorities = 0
    for rucksack in solution.rucksacks:
        for item in rucksack.item_intersections:
            sum_of_compartment_priorities += solution.get_item_priority(item)
    logger.info(f"Sum of priorities for compartments: {sum_of_compartment_priorities}.")

    solution.divide_rucksacks()
    solution.find_intersections_across_groups()

    sum_of_group_priorities = 0
    for group_intersection in solution.group_intersections:
        for item in group_intersection:
            sum_of_group_priorities += solution.get_item_priority(item)
    logger.info(f"Sum of priorities for groups: {sum_of_group_priorities}.")


if __name__ == '__main__':
    main()
