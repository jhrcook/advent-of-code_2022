"""Advent of Code 2022 – Day 2. Rock Paper Scissors"""

from enum import Enum
from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import puzzle_input_file, read_file_to_string

DAY: Final[int] = 2
TITLE: Final[str] = "Rock Paper Scissors"

example_strategy_guide = """
A Y
B X
C Z
"""

GameStrategy = list[tuple[str, str]]


def parse_game_strategy(strat_str: str) -> GameStrategy:
    """Parse the game strategy from a string."""
    strategy: GameStrategy = []
    strat_str = strat_str.strip()
    for line in strat_str.splitlines():
        if line == "":
            continue
        choices = [x.strip() for x in line.split(" ")]
        assert len(choices) == 2
        strategy.append((choices[0], choices[1]))
    return strategy


class RPSResult(str, Enum):
    """Rock-Paper-Scissors result."""

    LOSS = "LOSS"
    DRAW = "DRAW"
    WIN = "WIN"


rps_choice_conversion_table: Final[dict[str, str]] = {"X": "A", "Y": "B", "Z": "C"}


def play_round_of_rps(a: str, b: str) -> RPSResult:
    """Result of a round of Rock-Paper-Scissors.

    Args:
        a (str): Opponents choice.
        b (str): My choice.

    Raises:
        BaseException: Raised if no result found.

    Returns:
        RPSResult: Result of the round of the game.
    """
    b = rps_choice_conversion_table[b]
    if a == b:
        return RPSResult.DRAW
    if a == "A":
        if b == "B":
            return RPSResult.WIN
        else:
            return RPSResult.LOSS
    elif a == "B":
        if b == "C":
            return RPSResult.WIN
        else:
            return RPSResult.LOSS
    elif a == "C":
        if b == "A":
            return RPSResult.WIN
        else:
            return RPSResult.LOSS
    else:
        raise BaseException("Should not reach this point.")


game_result_points: Final[dict[RPSResult, int]] = {
    RPSResult.LOSS: 0,
    RPSResult.DRAW: 3,
    RPSResult.WIN: 6,
}

choice_played_points_xyz: Final[dict[str, int]] = {"X": 1, "Y": 2, "Z": 3}

choice_played_points_abc: Final[dict[str, int]] = {"A": 1, "B": 2, "C": 3}


def puzzle_1(strategy: GameStrategy) -> int:
    """Puzzle 1."""
    total_points: int = 0
    for a, b in strategy:
        result = play_round_of_rps(a, b)
        points = game_result_points[result] + choice_played_points_xyz[b]
        total_points += points
    return total_points


desired_outcome_table: Final[dict[str, RPSResult]] = {
    "X": RPSResult.LOSS,
    "Y": RPSResult.DRAW,
    "Z": RPSResult.WIN,
}


def get_choice_to_win(a: str, outcome: RPSResult) -> str:
    """Get the choice required for the desired result.

    Args:
        a (str): Choice of opponent.
        outcome (RPSResult): Desired result of the round.

    Raises:
        BaseException: Raised if no solution found.

    Returns:
        str: Choice I should make.
    """
    if outcome is RPSResult.DRAW:
        return a

    if a == "A":
        if outcome is RPSResult.WIN:
            return "B"
        else:
            return "C"
    elif a == "B":
        if outcome is RPSResult.WIN:
            return "C"
        else:
            return "A"
    elif a == "C":
        if outcome is RPSResult.WIN:
            return "A"
        else:
            return "B"
    else:
        raise BaseException("Should not reach this point.")


def puzzle_2(strategy: GameStrategy) -> int:
    """Puzzle 2."""
    total_points: int = 0
    for a, b in strategy:
        result = desired_outcome_table[b]
        choice = get_choice_to_win(a, result)
        points = game_result_points[result] + choice_played_points_abc[choice]
        total_points += points
    return total_points


def main() -> None:
    """Execute puzzles."""
    input_file = puzzle_input_file(DAY)
    input_strategy = parse_game_strategy(read_file_to_string(input_file))

    # Puzzle 1.
    ex_strat = parse_game_strategy(example_strategy_guide)
    ex_res = puzzle_1(ex_strat)
    check_result(15, ex_res)
    res1 = puzzle_1(input_strategy)
    check_result(11873, res1)

    # Puzzle 2.
    ex_strat = parse_game_strategy(example_strategy_guide)
    ex_res = puzzle_2(ex_strat)
    check_result(12, ex_res)
    res2 = puzzle_2(input_strategy)
    check_result(12014, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
