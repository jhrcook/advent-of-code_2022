"""Advent of Code 2022 – Day N. Title"""

from pathlib import Path
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import puzzle_input_file

DAY: Final[int] = 1
TITLE: Final[str] = ""


def puzzle_1() -> None:
    """Puzzle 1."""
    ...


def puzzle_2() -> None:
    """Puzzle 2."""
    ...


def main() -> None:
    """Execute puzzles."""
    input_file = puzzle_input_file(DAY)
    print_results(DAY, TITLE, result1=None, result2=None)


if __name__ == "__main__":
    main()
