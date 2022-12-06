"""Advent of Code 2022 – Day 6. Tuning Trouble."""

from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 6
TITLE: Final[str] = "Tuning Trouble"

example_inputs_1 = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
    "nppdvjthqldpwncqszvftbrmjlhg": 6,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
}


example_inputs_2 = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
    "nppdvjthqldpwncqszvftbrmjlhg": 23,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
}


def find_position_of_marker(data: str, n_chars: int) -> int | None:
    """Finf the position of a marker.

    Args:
        data (str): Datastream buffer.
        n_chars (int): Number of characters for the marker.

    Returns:
        int | None: The last index of the marker or `None` if the marker is not found.
    """
    for i in range(len(data)):
        if len(set(data[i : (i + n_chars)])) == n_chars:
            return i + n_chars
    return None


def puzzle_1(datastream_buffer: str) -> int:
    """Puzzle 1."""
    datastream_buffer = datastream_buffer.strip()
    if (res := find_position_of_marker(datastream_buffer, n_chars=4)) is not None:
        return res
    raise BaseException("No 'start-of-packet marker' found.")


def puzzle_2(datastream_buffer: str) -> int:
    """Puzzle 2."""
    datastream_buffer = datastream_buffer.strip()
    if (res := find_position_of_marker(datastream_buffer, n_chars=14)) is not None:
        return res
    raise BaseException("No 'start-of-packet marker' found.")


def main() -> None:
    """Execute puzzles."""
    datastream_buffer = read_input_to_string(DAY)

    # Puzzle 1.
    for example_input, expected_value in example_inputs_1.items():
        ex_res = puzzle_1(example_input)
        check_result(expected_value, ex_res)
    first_datastream = datastream_buffer.splitlines()[0]
    res1 = puzzle_1(first_datastream)
    check_result(1210, res1)

    # Puzzle 2.
    for example_input, expected_value in example_inputs_2.items():
        ex_res = puzzle_2(example_input)
        check_result(expected_value, ex_res)
    first_datastream = datastream_buffer.splitlines()[0]
    res2 = puzzle_2(first_datastream)
    check_result(3476, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
