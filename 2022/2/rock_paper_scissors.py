#!/usr/bin/env python3

import logging
import os
import sys
from enum import IntEnum
from typing import List

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
# noinspection PyPep8
from downloader import Downloader


class RockPaperScissors(object):
    class Choice(IntEnum):
        """
        Represents the score for each shape choice.
        """
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    class Decision(IntEnum):
        """
        Represents the score for each decision.
        """
        WIN = 6
        DRAW = 3
        LOSE = 0

    CHOICE_MAPPING: dict[str, Choice] = {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS
    }

    DECISION_MAPPING: dict[str, Decision] = {
        "X": Decision.LOSE,
        "Y": Decision.DRAW,
        "Z": Decision.WIN
    }

    WINNING_CONDITION_MAP: dict = {
        Choice.ROCK: Choice.PAPER,
        Choice.PAPER: Choice.SCISSORS,
        Choice.SCISSORS: Choice.ROCK
    }

    LOSE_CONDITION_MAP: dict = {
        Choice.ROCK: Choice.SCISSORS,
        Choice.PAPER: Choice.ROCK,
        Choice.SCISSORS: Choice.PAPER
    }

    def __init__(self):
        self._logger = logging.getLogger(RockPaperScissors.__name__)

        self._mapped_choices: List[tuple[RockPaperScissors.Choice, RockPaperScissors.Decision]] = []
        self._player_score: int = 0

    def process_input_data(self, input_data: List[str]) -> None:
        self._logger.info(f"Processing {len(input_data)} line(s).")
        for line in input_data:
            left, right = line.strip().split(" ")
            self._mapped_choices.append((
                RockPaperScissors.CHOICE_MAPPING.get(left),
                RockPaperScissors.DECISION_MAPPING.get(right)
            ))

    def calculate_scores(self) -> None:
        win_rate, draw_rate, lose_rate = 0, 0, 0
        for choices in self._mapped_choices:
            opponent_choice, player_choice = choices
            if player_choice == RockPaperScissors.Decision.WIN:
                win_rate += 1
                # We chose to win, so we must add the win value plus whatever score is assigned to the shape that is
                # required to beat the opponent.
                self._player_score += RockPaperScissors.Decision.WIN.value \
                    + RockPaperScissors.WINNING_CONDITION_MAP.get(opponent_choice).value
            elif player_choice == RockPaperScissors.Decision.DRAW:
                draw_rate += 1
                # We chose to draw, so we add the draw score plus whatever score is assigned to the shape the opponent
                # selected, since we too select that same shape.
                self._player_score += RockPaperScissors.Decision.DRAW.value + opponent_choice.value
            elif player_choice == RockPaperScissors.Decision.LOSE:
                lose_rate += 1
                # We chose to lose, so we only get the score assigned to the shape that loses to the opponent.
                self._player_score += RockPaperScissors.LOSE_CONDITION_MAP.get(opponent_choice).value
            else:
                # Sanity check the input.
                raise RuntimeError("Unrecognized input.")
        self._logger.info(f"Stats: win rate = {win_rate}, lose rate = {lose_rate}, draw rate = {draw_rate}.")

    @property
    def total_player_score(self):
        return self._player_score


@click.command()
@click.option('--session', type=str, required=True, help="Session cookie required to downloader the input from AOC.")
def main(session) -> None:
    """General entry point for solutions."""
    logging.basicConfig(level=logging.NOTSET, format="%(asctime)s: %(levelname)s: %(name)s: %(lineno)d: %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S%z")

    # Fill in specifics for the year and the day that you are working on.
    aoc_downloader = Downloader(year=2022, day=2, cookie_list=[('session', session), ])
    aoc_downloader.download_input(destination=os.path.dirname(__file__))

    logger = logging.getLogger()

    # If you want to log the output:
    # logger.debug(aoc_downloader.input_data)

    # Place the code to run the solution with the downloaded input after this line:
    solution = RockPaperScissors()
    solution.process_input_data(aoc_downloader.input_data)
    solution.calculate_scores()

    logger.info(f"Player score: {solution.total_player_score}.")


if __name__ == '__main__':
    main()
