"""Advent of Code 2022"""

from typing import Callable, Final

from typer import Typer

from advent_of_code.puzzles import day01, day02, day03

app = Typer()

__version__ = "1.0.0"

PUZZLES: Final[dict[int, Callable[[], None]]] = {
    1: day01.main,
    2: day02.main,
    3: day03.main,
}


def _run_all_puzzles() -> None:
    for fxn in PUZZLES.values():
        fxn()


def _run_puzzle(day: int) -> None:
    PUZZLES[day]()


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
