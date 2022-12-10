"""Advent of Code 2022 – Day 10. Cathode-Ray Tube."""

from typing import Final, Protocol

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 10
TITLE: Final[str] = "Cathode-Ray Tube"

example_input = """
noop
addx 3
addx -5
"""

example_input_2 = read_input_to_string(DAY, filename="example-input.txt")


class CpuOperation(Protocol):
    """CPU operation protocol."""

    def __call__(self, X: int) -> list[int]:
        """Call a CPU operation.

        Args:
            X (int): Current X register value.

        Returns:
            list[int]: Values of X after the completion of eac cycle.
        """
        ...


class Noop:
    """A `noop` operation."""

    def __call__(self, X: int) -> list[int]:
        """Execute a `noop` instruction (1 cycle)."""
        return [X]

    def __str__(self) -> str:
        return "noop"

    def __repr__(self) -> str:
        return str(self)


class Addx:
    """An `addx V` operation."""

    def __init__(self, V: int) -> None:
        self.V = V

    def __call__(self, X: int) -> list[int]:
        """Execute an `addx` instruction (2 cycles)."""
        return [X, X + self.V]

    def __str__(self) -> str:
        return f"addx {self.V}"

    def __repr__(self) -> str:
        return str(self)


def parse_cpu_instructions(input_str: str) -> list[CpuOperation]:
    """Parse CPU instructions from string."""
    instructs: list[CpuOperation] = []
    for line in input_str.strip().splitlines():
        line = line.strip()
        if line.startswith("addx"):
            instructs.append(Addx(int(line.split(" ")[1])))
        elif line.startswith("noop"):
            instructs.append(Noop())
    return instructs


def execute_cpu_instructions(cpu_instructions: list[CpuOperation]) -> list[int]:
    """Execute CPU instructions.

    Args:
        cpu_instructions (list[CpuOperation]): CPU instructions.

    Returns:
        list[int]: Values of the X register for each cycle.
    """
    x_values: list[int] = [1]
    for cpu in cpu_instructions:
        x_values += cpu(x_values[-1])
    return x_values


def puzzle_1(cpu_instructions: list[CpuOperation]) -> int:
    """Puzzle 1."""
    x_values = execute_cpu_instructions(cpu_instructions)
    strengths = []
    for i in (20, 60, 100, 140, 180, 220):
        strengths.append(x_values[i - 1] * i)
    return sum(strengths)


def puzzle_2(cpu_instructions: list[CpuOperation]) -> str:
    """Puzzle 2."""
    x_values = execute_cpu_instructions(cpu_instructions)
    message = ""
    for i, x in enumerate(x_values[:-1]):
        if i % 40 == 0:
            message += "\n"
        if i % 40 in (x - 1, x, x + 1):
            message += "#"
        else:
            message += "."
    return message


def main(silent: bool = True) -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_cpu = parse_cpu_instructions(example_input_2)
    ex_res = puzzle_1(ex_cpu)
    check_result(13140, ex_res)
    res1 = puzzle_1(parse_cpu_instructions(read_input_to_string(DAY)))
    check_result(15220, res1)

    # Puzzle 2.
    ex_res2 = puzzle_2(parse_cpu_instructions(example_input_2))
    if not silent:
        print(ex_res2)
    res2 = puzzle_2(parse_cpu_instructions(read_input_to_string(DAY)))
    if not silent:
        print(res2)

    print_results(DAY, TITLE, result1=res1, result2="RFZEKBFA")


if __name__ == "__main__":
    main()
