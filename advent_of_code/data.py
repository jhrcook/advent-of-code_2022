"""Advent of Code 2022 data."""

import os
from pathlib import Path


def _data_dir() -> Path:

    return Path(os.getcwd()) / "data"


def puzzle_input_file(day: int) -> Path:
    return _data_dir() / f"day{day:02d}" / "input.txt"
