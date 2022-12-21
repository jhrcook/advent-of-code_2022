"""Advent of Code 2022 – Day 15. Beacon Exclusion Zone."""

import re
from enum import Enum
from typing import Final, TypeAlias

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 15
TITLE: Final[str] = "Beacon Exclusion Zone"

example_input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

Coord: TypeAlias = tuple[int, int]


class Thing(str, Enum):
    """Thing in a cave."""

    SENSOR = "S"
    BEACON = "B"
    HASHTAG = "#"
    EMPTY = "."


def manhattan_distance(c1: Coord, c2: Coord) -> int:
    """Calculate the Manhattan distance between two points."""
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


class Measurement:
    """Sensor and beacon measurement."""

    def __init__(self, sensor: Coord, beacon: Coord) -> None:
        self.sensor = sensor
        self.beacon = beacon
        self.distance = manhattan_distance(sensor, beacon)

    def __str__(self) -> str:
        return f"sensor: {self.sensor}  beacon: {self.beacon}  (dist: {self.distance})"

    def __repr__(self) -> str:
        return str(self)


def parse_coordinate_input(input_str: str) -> list[Measurement]:
    """Parse input data into sensor-beacon measurements."""
    measurements: list[Measurement] = []
    for line in input_str.strip().splitlines():
        split = [x.strip() for x in re.split(r":|,", line)]
        assert len(split) == 4
        s_x = int(split[0].split("x=")[1])
        s_y = int(split[1].split("y=")[1])
        b_x = int(split[2].split("x=")[1])
        b_y = int(split[3].split("y=")[1])
        measurements.append(Measurement(sensor=(s_x, s_y), beacon=(b_x, b_y)))
    return measurements


def _count_senors_and_beacons_on_row(ms: list[Measurement], y: int) -> int:
    hits: set[Coord] = set()
    for m in ms:
        if m.sensor[1] == y:
            hits.add(m.sensor)
        if m.beacon[1] == y:
            hits.add(m.beacon)
    return len(hits)


def puzzle_1(measurements: list[Measurement], y_check: int) -> int:
    """Puzzle 1."""
    measurements.sort(key=lambda m: m.sensor[0])
    x_marked: set[int] = set()
    for m in measurements:
        dy = abs(m.sensor[1] - y_check)  # Difference in sensor y and row being checked.
        if m.distance <= dy:
            continue
        dist = m.distance - dy  # Adjust range of sensor based on the difference.
        x_min, x_max = m.sensor[0] - dist, m.sensor[0] + dist
        x_marked.update(range(x_min, x_max + 1))
    return len(x_marked) - _count_senors_and_beacons_on_row(measurements, y=y_check)


def puzzle_2() -> None:
    """Puzzle 2."""
    ...


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_data = parse_coordinate_input(example_input)
    ex_res = puzzle_1(ex_data, 10)
    check_result(26, ex_res)
    measurements = parse_coordinate_input(read_input_to_string(DAY))
    res1 = puzzle_1(measurements, 2000000)
    check_result(5688618, res1)

    # Puzzle 2.
    ...

    print_results(DAY, TITLE, result1=res1, result2=None)


if __name__ == "__main__":
    main()
