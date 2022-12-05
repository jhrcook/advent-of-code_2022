"""Advent of Code 2022 – Day 5. Supply Stacks."""

from dataclasses import dataclass
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 5
TITLE: Final[str] = "Supply Stacks"

example_input = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


@dataclass
class MoveInstruction:
    """A single crate movement instruction."""

    move: int
    from_col: int
    to_col: int

    def __str__(self) -> str:
        return f"move {self.move} from {self.from_col} to {self.to_col}"


class MoveInstructions:
    """Create movement instructions."""

    def __init__(self, instruct_str: str) -> None:
        self._instruct_str = instruct_str
        instructions: list[MoveInstruction] = []
        for line in instruct_str.strip().splitlines():
            split_line = line.strip().split(" ")
            instructions.append(
                MoveInstruction(
                    move=int(split_line[1]),
                    from_col=int(split_line[3]),
                    to_col=int(split_line[5]),
                )
            )
        self.instructions = instructions

    def __str__(self) -> str:
        msg = "\n".join([str(i) for i in self.instructions])
        msg = "Move Instructions\n" + ("-" * 25) + "\n" + msg + "\n" + ("-" * 25) + "\n"
        return msg

    def __repr__(self) -> str:
        return str(self)


def _split_row_of_crates(row_str: str) -> list[str]:
    return [row_str[i : i + 3].strip() for i in range(0, len(row_str), 4)]


class CrateConfiguration:
    """Crate configuration."""

    def __init__(self, config_str: str) -> None:
        self._config_str = config_str

        # 1. Get data in rows.
        rows: list[list[str]] = []
        n_cols = -1
        for line in config_str.splitlines():
            if line.strip() == "":
                continue
            if "1" in line:
                n_cols = max([int(x.strip()) for x in _split_row_of_crates(line)])
                break
            crates = _split_row_of_crates(line)
            crates = [x.replace("[", "").replace("]", "") for x in crates]
            rows.append(crates)
        rows.reverse()
        assert n_cols > 0

        # 2. Re-arrange the data into columns.
        columns: list[list[str]] = [[] for _ in range(n_cols)]
        for row in rows:
            for c, x in enumerate(row):
                if x != "":
                    columns[c].append(x)
        self.columns = columns

    def __str__(self) -> str:
        msg = "Crate Configuration\n" + ("-" * 25) + "\n"
        for i, col in enumerate(self.columns):
            msg += f"{i:2d}  {' '.join(col)}\n"
        msg += "-" * 25
        return msg

    def __repr__(self) -> str:
        return str(self)


def parse_input_to_crates(
    input_str: str,
) -> tuple[CrateConfiguration, MoveInstructions]:
    """Parse puzzle input.

    Args:
        input_str (str): Puzzle input string.

    Returns:
        tuple[CrateConfiguration, MoveInstructions]: Crate configuration and move
        instructions.
    """
    split_input_str = input_str.splitlines()
    split_i = 0
    for i, line in enumerate(split_input_str):
        if i > 0 and line.strip() == "":
            split_i = i
            break
    config_str = "\n".join(split_input_str[:split_i])
    instruct_str = "\n".join(split_input_str[(split_i + 1) :])
    config = CrateConfiguration(config_str)
    instruct = MoveInstructions(instruct_str)
    return config, instruct


def crane_9000_move(config: CrateConfiguration, instruction: MoveInstruction) -> None:
    """Move the crates given a single instruction for crane 9000."""
    n, f, t = instruction.move, instruction.from_col - 1, instruction.to_col - 1
    for _ in range(n):
        config.columns[t].append(config.columns[f].pop())


def puzzle_1(configuration: CrateConfiguration, instructions: MoveInstructions) -> str:
    """Puzzle 1."""
    for instruction in instructions.instructions:
        crane_9000_move(configuration, instruction)
    msg = "".join([col[-1] for col in configuration.columns])
    return msg


def crane_9001_move(config: CrateConfiguration, instruction: MoveInstruction) -> None:
    """Move the crates given a single instruction for crane 9001."""
    n, f, t = instruction.move, instruction.from_col - 1, instruction.to_col - 1
    if n == 1:
        crane_9000_move(config, instruction)
    else:
        col = config.columns[f]
        new_col = col[:-n]
        config.columns[t] += col[-n:]
        config.columns[f] = new_col


def puzzle_2(configuration: CrateConfiguration, instructions: MoveInstructions) -> str:
    """Puzzle 2."""
    for instruction in instructions.instructions:
        crane_9001_move(configuration, instruction)

    msg = "".join([col[-1] for col in configuration.columns])
    return msg


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    example_config, example_instruct = parse_input_to_crates(example_input)
    config, instructions = parse_input_to_crates(read_input_to_string(DAY))
    exp_res = puzzle_1(example_config, example_instruct)
    check_result("CMZ", exp_res)
    res1 = puzzle_1(config, instructions)
    check_result("RFFFWBPNS", res1)

    # Puzzle 2.
    example_config, example_instruct = parse_input_to_crates(example_input)
    config, instructions = parse_input_to_crates(read_input_to_string(DAY))
    exp_res = puzzle_2(example_config, example_instruct)
    check_result("MCD", exp_res)
    res2 = puzzle_2(config, instructions)
    check_result("CQQBBJFCS", res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
