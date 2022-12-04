"""Advent of Code 2022 – Day 3. Rucksack Reorganization."""

from string import ascii_lowercase, ascii_uppercase
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 3
TITLE: Final[str] = "Rucksack Reorganization"

example_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


class Rucksack:
    """Rucksack data."""

    def __init__(self, objects: str) -> None:
        objects = objects.strip()
        self._objects = objects
        split = len(objects) // 2
        self.compartments = [objects[:split], objects[split:]]

    def __str__(self) -> str:
        return " ".join(self.compartments)

    def __repr__(self) -> str:
        return str(self)


def convert_input_into_rucksacks(input_data: str) -> list[Rucksack]:
    """Convert input data into rucksack data."""
    rucksacks: list[Rucksack] = []
    for line in input_data.strip().splitlines():
        rucksacks.append(Rucksack(line))
    return rucksacks


def find_object_in_both_compartments(rucksack: Rucksack) -> str:
    """Find the object in both compartments of a rucksack."""
    in_both = set(rucksack.compartments[0]).intersection(rucksack.compartments[1])
    assert len(in_both) == 1
    return list(in_both)[0]


def make_object_priority_table() -> dict[str, int]:
    """Create an object:priority table."""
    return {k: i + 1 for i, k in enumerate(list(ascii_lowercase + ascii_uppercase))}


def puzzle_1(rucksacks: list[Rucksack]) -> int:
    """Puzzle 1."""
    total = 0
    object_priority_table = make_object_priority_table()
    for rucksack in rucksacks:
        in_both = find_object_in_both_compartments(rucksack)
        total += object_priority_table[in_both]
    return total


def find_group_badge(group: list[Rucksack]) -> str:
    """Find the badge for a group of elves."""
    badge = set(group[0]._objects)
    for r in group[1:]:
        badge = badge.intersection(r._objects)
    assert len(badge) == 1
    return list(badge)[0]


def puzzle_2(rucksacks: list[Rucksack]) -> int:
    """Puzzle 2."""
    total = 0
    object_priority_table = make_object_priority_table()
    for i in range(len(rucksacks) // 3):
        j = i * 3
        group = rucksacks[j : j + 3]
        badge = find_group_badge(group)
        total += object_priority_table[badge]
    return total


def main() -> None:
    """Execute puzzles."""
    ex_rucksacks = convert_input_into_rucksacks(example_input)
    rucksacks = convert_input_into_rucksacks(read_input_to_string(DAY))

    # Puzzle 1.
    ex_res = puzzle_1(ex_rucksacks)
    check_result(157, ex_res)
    res1 = puzzle_1(rucksacks)
    check_result(7446, res1)

    # Puzzle 2.
    ex_res = puzzle_2(ex_rucksacks)
    check_result(70, ex_res)
    res2 = puzzle_2(rucksacks)
    check_result(2646, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
