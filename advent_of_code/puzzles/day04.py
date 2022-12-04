"""Advent of Code 2022 – Day 4. Camp Cleanup."""

from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 4
TITLE: Final[str] = "Camp Cleanup"

example_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


class CleaningRange:
    """Elf cleaning range."""

    def __init__(self, cleaning_range: str) -> None:
        split = cleaning_range.split("-")
        assert len(split) == 2
        self.start = int(split[0])
        self.end = int(split[1])

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def __repr__(self) -> str:
        return str(self)


CleaningRangePairs = list[tuple[CleaningRange, CleaningRange]]


def _convert_input_to_cleaning_range_pairs(input_data: str) -> CleaningRangePairs:
    ranges: CleaningRangePairs = []
    for line in input_data.strip().splitlines():
        split_line = line.strip().split(",")
        assert len(split_line) == 2
        ranges.append((CleaningRange(split_line[0]), CleaningRange(split_line[1])))
    return ranges


def _a_is_within_b(a: CleaningRange, b: CleaningRange) -> bool:
    return (b.start <= a.start) and (a.end <= b.end)


def one_pair_is_within_another(a: CleaningRange, b: CleaningRange) -> int:
    """One pair of a cleaning range is within another."""
    return int(_a_is_within_b(a, b) or _a_is_within_b(b, a))


def puzzle_1(range_pairs: CleaningRangePairs) -> int:
    """Puzzle 1."""
    total = 0
    for a, b in range_pairs:
        total += one_pair_is_within_another(a, b)
    return total


def _a_overlaps_b(a: CleaningRange, b: CleaningRange) -> bool:
    if _a_is_within_b(a, b):
        return True
    return (a.start <= b.start) and (a.end >= b.start)


def pairs_overlap(a: CleaningRange, b: CleaningRange) -> int:
    """Cleaning ranges overlap."""
    return int(_a_overlaps_b(a, b) or _a_overlaps_b(b, a))


def puzzle_2(range_pairs: CleaningRangePairs) -> int:
    """Puzzle 2."""
    total = 0
    for a, b in range_pairs:
        total += pairs_overlap(a, b)
    return total


def main() -> None:
    """Execute puzzles."""
    example_ranges = _convert_input_to_cleaning_range_pairs(example_input)
    cleaning_ranges = _convert_input_to_cleaning_range_pairs(read_input_to_string(DAY))

    # Puzzle 1.
    ex_res = puzzle_1(example_ranges)
    check_result(2, ex_res)
    res1 = puzzle_1(cleaning_ranges)
    check_result(507, res1)

    # Puzzle 2.
    ex_res = puzzle_2(example_ranges)
    check_result(4, ex_res)
    res2 = puzzle_2(cleaning_ranges)
    check_result(897, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
