"""Advent of Code 2022 – Day 1. Calorie Counting"""

from pathlib import Path
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import puzzle_input_file

DAY: Final[int] = 1
TITLE: Final[str] = "Calorie Counting"

ex_input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


class ElfCalorie:
    """Elf calories data."""

    def __init__(self, values: list[int]) -> None:
        self.values = values
        self.total = sum(values)
        return None

    def __str__(self) -> str:
        return f"Elf Calories: {self.total}"

    def __repr__(self) -> str:
        return str(self)


def _read_file(fpath: Path) -> str:
    with open(fpath) as f:
        return "".join(list(f))


def parse_elf_calorie_input(data: str) -> list[ElfCalorie]:
    """Parse elf calories input data.

    Args:
        data (str): Raw input string.

    Returns:
        list[ElfCalorie]: List of elf calorie data.
    """
    _current_values: list[int] = []
    elves: list[ElfCalorie] = []
    for x in data.splitlines():
        x = x.strip()
        if x == "":
            if len(_current_values) > 0:
                elves.append(ElfCalorie(_current_values))
                _current_values = []
        else:
            _current_values.append(int(x))

    if len(_current_values) > 0:
        elves.append(ElfCalorie(_current_values))
        _current_values = []

    return elves


def puzzle_1(elf_cals: list[ElfCalorie]) -> int:
    """Puzzle 1.

    Args:
        elf_cals (list[ElfCalorie]): Elf calories.

    Returns:
        int: The top total calorie value.
    """
    cals = [elf.total for elf in elf_cals]
    return max(cals)


def puzzle_2(elf_cals: list[ElfCalorie]) -> int:
    """Puzzle 2.

    Args:
        elf_cals (list[ElfCalorie]): Elf calories.

    Returns:
        int: Sum of the top three total calorie values.
    """
    cals = sorted([elf.total for elf in elf_cals])
    return sum(cals[-3:])


def main() -> None:
    """Execute puzzles."""
    ex_elfs = parse_elf_calorie_input(ex_input)
    elf_calories = parse_elf_calorie_input(_read_file(puzzle_input_file(day=DAY)))

    # Puzzle 1.
    ex_res = puzzle_1(ex_elfs)
    check_result(24000, ex_res)
    res1 = puzzle_1(elf_cals=elf_calories)
    check_result(68787, res1)

    # Puzzle 2.
    ex_res = puzzle_2(ex_elfs)
    check_result(45000, ex_res)
    res2 = puzzle_2(elf_cals=elf_calories)
    check_result(198041, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
