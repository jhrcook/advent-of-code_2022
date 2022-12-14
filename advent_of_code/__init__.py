"""Advent of Code 2022."""

from typing import Final, Protocol

from typer import Typer

from advent_of_code.puzzles import (
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
    day10,
    day11,
    day12,
    day13,
)

app = Typer()

__version__ = "1.0.0"


class AdventOfCodeDayModule(Protocol):
    """Advent of Code puzzle protocol."""

    DAY: int
    TITLE: str

    def main(self) -> None:
        """Main function to run the puzzles for a day of Advent of Code."""
        ...


PUZZLES: Final[list[AdventOfCodeDayModule]] = [
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
    day10,
    day11,
    day12,
    day13,
]

PUZZLES.sort(key=lambda m: m.DAY)


def _get_puzzle(day: int) -> AdventOfCodeDayModule:
    if day > len(PUZZLES):
        raise ModuleNotFoundError(f"No puzzle for day {day}.")
    return PUZZLES[day - 1]


def _run_all_puzzles() -> None:
    for puzzle in PUZZLES:
        puzzle.main()


def _run_puzzle(day: int) -> None:
    _get_puzzle(day).main()


@app.command()
def run_puzzles(day: int | None = None) -> None:
    """Run puzzles.

    Args:
        day (int | None, optional): Specific day to run the puzzles for. Defaults to
        `None` to run all puzzles.
    """
    print("--- Advent of Code 2022 ---")
    if day is None:
        _run_all_puzzles()
    else:
        _run_puzzle(day=day)
