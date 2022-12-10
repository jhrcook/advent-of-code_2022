"""Advent of Code 2022 data."""

import os
from pathlib import Path


def _data_dir() -> Path:
    return Path(os.getcwd()) / "data"


def puzzle_input_file(day: int, filename: str | None = None) -> Path:
    """Get path to day's input file."""
    if filename is None:
        filename = "input.txt"
    return _data_dir() / f"day{day:02d}" / filename


def read_input_to_string(day: int, filename: str | None = None) -> str:
    """Read input data file as a string."""
    return puzzle_input_file(day=day, filename=filename).read_text()
