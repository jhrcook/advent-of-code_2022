"""Advent of Code 2022 – Day 14. Regolith Reservoir."""

from typing import Final, TypeAlias

import numpy as np
import numpy.typing as npt

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 14
TITLE: Final[str] = "Regolith Reservoir"

example_input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

Coord = tuple[int, int]
CavePath = list[Coord]
Cave: TypeAlias = npt.NDArray[np.int_]

# Cave key:
#   0: empty
#  -1: sand
#   1: rock


def parse_input_into_paths(input_str: str) -> list[CavePath]:
    """Parse input string into paths.

    Args:
        input_str (str): Input data as a string.

    Returns:
        list[CavePath]: List of paths of rock in the cave.
    """
    paths: list[CavePath] = []
    for line in input_str.strip().splitlines():
        line = line.strip()
        path: CavePath = []
        paths.append(path)
        for coord_str in line.split(" -> "):
            coord = [int(x) for x in coord_str.split(",")]
            assert len(coord) == 2
            path.append((coord[0], coord[1]))
    return paths


def _get_max_val_from_coords(cave_paths: list[CavePath], idx: int) -> int:
    all_vals = []
    for path in cave_paths:
        all_vals += [coord[idx] for coord in path]
    return max(all_vals)


def _add_rocks_between(a: Coord, b: Coord, cave: Cave) -> None:
    if a[0] != b[0]:
        low, high = min([a[0], b[0]]), max([a[0], b[0]])
        cave[a[1], low : (high + 1)] = 1
    elif a[1] != b[1]:
        low, high = min([a[1], b[1]]), max([a[1], b[1]])
        cave[low : (high + 1), a[0]] = 1
    else:
        raise BaseException("No straight line between coords.")


def parse_cave_paths_to_array(cave_paths: list[CavePath]) -> Cave:
    """Convert the paths of rocks in a cave into an array for the cave.

    Cave key:
      0: empty
     -1: sand
      1: rock

    Args:
        cave_paths (list[CavePath]): Path of rocks in the cave.

    Returns:
        Cave: The cave represnetated as a matrix.
    """
    max_x = _get_max_val_from_coords(cave_paths, 0)
    max_y = _get_max_val_from_coords(cave_paths, 1)
    cave = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for path in cave_paths:
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            _add_rocks_between(a, b, cave=cave)
    return cave


def parse_input_to_cave(input_str: str) -> Cave:
    """Parse input string into a matrix representation of the cave."""
    return parse_cave_paths_to_array(parse_input_into_paths(input_str))


def add_sand_particle(cave: Cave, start: Coord = (0, 500)) -> None:
    """Add a particle of sand to the cave.

    Args:
        cave (Cave): Cave.
        start (tuple, optional): Where to begin adding sand. Defaults to (0, 500).
    """
    sand: Coord = start
    while True:
        if sand[0] + 1 >= cave.shape[0]:
            return
        elif cave[sand[0] + 1, sand[1]] == 0:
            sand = sand[0] + 1, sand[1]
        elif sand[1] - 1 < 0:
            return
        elif cave[sand[0] + 1, sand[1] - 1] == 0:
            sand = sand[0] + 1, sand[1] - 1
        elif sand[1] + 1 >= cave.shape[1]:
            return
        elif cave[sand[0] + 1, sand[1] + 1] == 0:
            sand = sand[0] + 1, sand[1] + 1
        else:
            break
    cave[sand[0], sand[1]] = -1


def fill_cave_with_sand(cave: Cave, start: Coord) -> Cave:
    """Fill a cave with sand."""
    n_sand = -1
    while n_sand != np.sum(cave == -1):
        n_sand = np.sum(cave == -1)
        add_sand_particle(cave, start=start)
    return cave


def puzzle_1(cave: Cave) -> int:
    """Puzzle 1."""
    cave = fill_cave_with_sand(cave, (0, 500))
    return np.sum(cave == -1)


def _buffer_cave_infinite_floor(cave: Cave, ext: int) -> Cave:
    size_buffer = np.zeros((cave.shape[0], ext), dtype=int)
    cave = np.hstack([size_buffer.copy(), cave, size_buffer.copy()])
    bottom_buffer = np.zeros((2, cave.shape[1]), dtype=int)
    bottom_buffer[-1, :] = 1
    cave = np.vstack([cave, bottom_buffer])
    return cave


def puzzle_2(cave: Cave) -> int:
    """Puzzle 2."""
    ext = 1_000
    cave = _buffer_cave_infinite_floor(cave, ext)
    cave = fill_cave_with_sand(cave, start=(0, 500 + ext))
    return np.sum(cave == -1)


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_cave = parse_input_to_cave(example_input)
    ex_res = puzzle_1(ex_cave)
    check_result(24, ex_res)
    cave = parse_input_to_cave(read_input_to_string(DAY))
    res1 = puzzle_1(cave)
    check_result(885, res1)

    # Puzzle 2.
    ex_cave = parse_input_to_cave(example_input)
    ex_res = puzzle_2(ex_cave)
    check_result(93, ex_res)
    cave = parse_input_to_cave(read_input_to_string(DAY))
    res2 = puzzle_2(cave)
    check_result(28691, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
