"""Command line interface helpers."""

from textwrap import dedent
from typing import Any


def print_results(day: int, result1: Any | None, result2: Any | None) -> None:
    if result1 is None:
        result1 = "(none)"
    if result2 is None:
        result2 = "(none)"
    msg = f"Results for Day {day}\n  puzzle 1: {result1}\n  puzzle 2: {result2}"
    msg = dedent(msg.strip())
    print(msg)
    return None
