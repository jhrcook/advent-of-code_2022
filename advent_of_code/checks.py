"""Checking the results of puzzles."""

from textwrap import dedent
from typing import TypeVar

T = TypeVar("T")


class FailedPuzzle(BaseException):
    """Puzzle failed on example data."""

    def __init__(self, expected: T, actual: T) -> None:
        self.expected = expected
        self.actual = actual
        msg = f"""
        Failed puzzle
          expected: {self.expected}
            actual: {self.actual}
        """
        msg = dedent(msg)
        super().__init__(msg)
        return None


def check_result(expected: T, actual: T) -> bool:
    if expected != actual:
        raise FailedPuzzle(expected, actual)
    return True
