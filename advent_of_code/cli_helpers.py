"""Command line interface helpers."""

from textwrap import dedent
from typing import Any


def print_results(
    day: int, title: str, result1: Any | None, result2: Any | None
) -> None:
    if result1 is None:
        result1 = "(none)"
    if result2 is None:
        result2 = "(none)"
    msg = f"Day {day}. '{title}'\n  puzzle 1: {result1}\n  puzzle 2: {result2}\n"
    msg = dedent(msg.strip())
    print(msg)
    return None
