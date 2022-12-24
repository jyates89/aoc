#!/usr/bin/env python3

import logging
import os
import sys
from enum import Enum
from typing import List

import click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
# noinspection PyPep8
from downloader import Downloader


class RockPaperScissors(object):
    class Choice(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    class ScoreType(Enum):
        WIN = 6
        TIE = 3

    CHOICE_SCORE_MAPPING: dict = {
        "A": Choice.ROCK.value,
        "B": Choice.PAPER.value,
        "C": Choice.SCISSORS.value,
        "X": Choice.ROCK.value,
        "Y": Choice.PAPER.value,
        "Z": Choice.SCISSORS.value
    }

    def __init__(self):
        self._logger = logging.getLogger(RockPaperScissors.__name__)

        self._mapped_choices: List[tuple[int, int]] = []
        self._player_score: int = 0

    def process_input_data(self, input_data: List[str]) -> None:
        self._logger.info(f"Processing {len(input_data)} line(s).")
        for line in input_data:
            left, right = line.strip().split(" ")
            self._mapped_choices.append((
                RockPaperScissors.CHOICE_SCORE_MAPPING.get(left),
                RockPaperScissors.CHOICE_SCORE_MAPPING.get(right)
            ))

    def calculate_scores(self) -> None:
        for choices in self._mapped_choices:
            opponent_choice, player_choice = choices
            if opponent_choice == player_choice:
                # There was a tie, so player gets the amount assigned to their shape, plus the value for a tie.
                self._player_score += player_choice + RockPaperScissors.ScoreType.TIE.value
            elif RockPaperScissors.Choice(opponent_choice) == RockPaperScissors.Choice.ROCK and \
                    RockPaperScissors.Choice(player_choice) == RockPaperScissors.Choice.SCISSORS:
                # Player loses, only getting the amount for the choice.
                self._player_score += player_choice
            elif RockPaperScissors.Choice(opponent_choice) == RockPaperScissors.Choice.SCISSORS and \
                    RockPaperScissors.Choice(player_choice) == RockPaperScissors.Choice.ROCK:
                # Player wins, getting the amount for the choice AND the win value.
                self._player_score += player_choice + RockPaperScissors.ScoreType.WIN.value
            else:
                # The rest of it can be simple to check, the player wins if they have the highest scoring shape.
                if opponent_choice > player_choice:
                    self._player_score += player_choice
                else:
                    self._player_score += player_choice + RockPaperScissors.ScoreType.WIN.value

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
