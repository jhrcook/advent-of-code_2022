"""Advent of Code 2022 data."""

import os
from pathlib import Path


def _data_dir() -> Path:
    return Path(os.getcwd()) / "data"


def puzzle_input_file(day: int) -> Path:
    """Get path to day's input file."""
    return _data_dir() / f"day{day:02d}" / "input.txt"


def read_input_to_string(day: int) -> str:
    """Read input data file as a string."""
    return puzzle_input_file(day=day).read_text()
