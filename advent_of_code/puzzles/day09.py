"""Advent of Code 2022 – Day 9. Rope Bridge."""

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

    def __init__(self) -> None:
        self.head = (0, 0)
        self.tail = (0, 0)

    def __str__(self) -> str:
        return f"H: {self.head}  T: {self.tail}"

    def __repr__(self) -> str:
        return str(self)

    def move(self, instruction: MoveInstruction) -> list[tuple[Position, Position]]:
        """Move the rope following some instruction."""
        positions: list[tuple[Position, Position]] = []
        m = -1 if instruction.direction in ("D", "L") else 1
        for _ in range(instruction.steps):
            if instruction.direction in ("U", "D"):
                self.head = self.head[0] + m, self.head[1]
                if (
                    abs(self.tail[0] - self.head[0]) < 2
                    and abs(self.tail[1] - self.head[1]) < 2
                ):
                    ...  # do nothing
                elif self.head[1] == self.tail[1]:
                    self.tail = self.tail[0] + m, self.tail[1]
                else:
                    self.tail = self.tail[0] + m, self.head[1]
            else:
                self.head = self.head[0], self.head[1] + m
                if (
                    abs(self.tail[0] - self.head[0]) < 2
                    and abs(self.tail[1] - self.head[1]) < 2
                ):
                    ...
                elif self.head[0] == self.tail[0]:
                    self.tail = self.tail[0], self.tail[1] + m
                else:
                    self.tail = self.head[0], self.tail[1] + m
            positions.append((self.head, self.tail))
        return positions


def parse_move_instructions(instruct_str: str) -> list[MoveInstruction]:
    """Parse movement instructions."""
    return [MoveInstruction(x) for x in instruct_str.strip().splitlines()]


def puzzle_1(instructions: list[MoveInstruction]) -> int:
    """Puzzle 1."""
    rope = Rope()
    tail_positions: set[Position] = set()
    for instruction in instructions:
        positions = rope.move(instruction)
        tail_positions = tail_positions.union([p[1] for p in positions])
    return len(tail_positions)


def puzzle_2() -> None:
    """Puzzle 2."""
    ...


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_res = puzzle_1(parse_move_instructions(example_input))
    check_result(13, ex_res)
    res1 = puzzle_1(parse_move_instructions(read_input_to_string(DAY)))
    check_result(6332, res1)

    # Puzzle 2.
    ...

    print_results(DAY, TITLE, result1=res1, result2=None)


if __name__ == "__main__":
    main()
