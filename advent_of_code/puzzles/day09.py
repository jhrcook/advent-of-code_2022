"""Advent of Code 2022 – Day 9. Rope Bridge."""

from itertools import product
from math import sqrt
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 9
TITLE: Final[str] = "Rope Bridge"

example_input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

example_input2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


class MoveInstruction:
    """Movement instruction."""

    def __init__(self, instruct_str: str) -> None:
        self._instruction_str = instruct_str
        split = instruct_str.split(" ")
        assert len(split) == 2
        self.direction, self.steps = split[0], int(split[1])

    def __str__(self) -> str:
        return f"{self.direction} {self.steps}"

    def __repr__(self) -> str:
        return str(self)


Position = tuple[int, int]


class Rope:
    """Model of this short rope."""

    def __init__(self, length: int) -> None:
        self.length: int = length
        self.knots: list[Position] = [(0, 0) for _ in range(length)]

    def __str__(self) -> str:
        return " - ".join([str(x) for x in self.knots])

    def __repr__(self) -> str:
        return str(self)

    def move(self, instruction: MoveInstruction) -> list[list[Position]]:
        """Move the rope following some instruction."""
        positions: list[list[Position]] = []
        for _ in range(instruction.steps):
            new_knots: list[Position] = []
            for i, knot in enumerate(self.knots):
                if i == 0:
                    knot = self._move_head(knot, instruction=instruction)
                else:
                    knot = self._move_trailing_knot(a=new_knots[-1], b=knot)
                new_knots.append(knot)
            self.knots = new_knots
            positions.append(new_knots)
        return positions

    def _move_head(self, head: Position, instruction: MoveInstruction) -> Position:
        m = -1 if instruction.direction in ("D", "L") else 1
        if instruction.direction in ("U", "D"):
            return (head[0] + m, head[1])
        else:
            return (head[0], head[1] + m)

    def _move_trailing_knot(self, a: Position, b: Position) -> Position:
        if abs(b[0] - a[0]) < 2 and abs(b[1] - a[1]) < 2:
            return b  # No movement.
        return find_closest_position_for_b(a, b)


def distance(a: Position, b: Position) -> float:
    """Calculate the distance between two points."""
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def find_closest_position_for_b(target: Position, b: Position) -> Position:
    """Find the closest position for point `b` to `target`."""
    new_pos: Position = b
    min_dist: float = 5.0
    for r, c in product(range(-1, 2), range(-1, 2)):
        pos = (b[0] + r, b[1] + c)
        d = distance(target, pos)
        if d < min_dist:
            new_pos = pos
            min_dist = d
    return new_pos


def parse_move_instructions(instruct_str: str) -> list[MoveInstruction]:
    """Parse movement instructions."""
    return [MoveInstruction(x) for x in instruct_str.strip().splitlines()]


def puzzle_1(instructions: list[MoveInstruction]) -> int:
    """Puzzle 1."""
    rope = Rope(2)
    tail_positions: set[Position] = set()
    for instruction in instructions:
        positions = rope.move(instruction)
        tail_positions = tail_positions.union([p[-1] for p in positions])
    return len(tail_positions)


def puzzle_2(instructions: list[MoveInstruction]) -> int:
    """Puzzle 2."""
    rope = Rope(10)
    tail_positions: set[Position] = set()
    for instruction in instructions:
        positions = rope.move(instruction)
        tail_positions = tail_positions.union([p[-1] for p in positions])
    return len(tail_positions)


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_res = puzzle_1(parse_move_instructions(example_input))
    check_result(13, ex_res)
    res1 = puzzle_1(parse_move_instructions(read_input_to_string(DAY)))
    check_result(6332, res1)

    # Puzzle 2.
    ex_res = puzzle_2(parse_move_instructions(example_input))
    check_result(1, ex_res)
    ex_res = puzzle_2(parse_move_instructions(example_input2))
    check_result(36, ex_res)
    res2 = puzzle_2(parse_move_instructions(read_input_to_string(DAY)))
    check_result(2511, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
