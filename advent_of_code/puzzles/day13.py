"""Advent of Code 2022 – Day 13. Distress Signal."""

from typing import Final

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 13
TITLE: Final[str] = "Distress Signal"

example_input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

Packet = list[int | "Packet"]
PacketPair = tuple[Packet, Packet]


def _parse_packet(line: str) -> Packet:
    return eval(line.strip())


def parse_distress_signal_code(input_str: str) -> list[PacketPair]:
    """Parse a distress signal input code."""
    distress_code: list[PacketPair] = []
    input_lines = [x.strip() for x in input_str.strip().splitlines()]
    input_lines = [x for x in input_lines if x != ""]
    for i in range(len(input_lines) // 2):
        pair = (
            _parse_packet(input_lines[i * 2]),
            _parse_packet(input_lines[(i * 2) + 1]),
        )
        distress_code.append(pair)
    return distress_code


def packet_pair_in_correct_order(
    left: int | Packet, right: int | Packet
) -> bool | None:
    """Check that a packet pair is in the correct order."""
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in zip(left, right):
            res = packet_pair_in_correct_order(a, b)
            if res is not None:
                return res
        if len(left) == len(right):
            return None
        else:
            return len(left) < len(right)
    elif isinstance(left, int):
        return packet_pair_in_correct_order([left], right)
    elif isinstance(right, int):
        return packet_pair_in_correct_order(left, [right])
    else:
        raise BaseException("Unexpected flow in packet comparison.")


def puzzle_1(distress_code: list[PacketPair]) -> int:
    """Puzzle 1."""
    correct_order: list[int] = []
    for i, pair in enumerate(distress_code):
        if packet_pair_in_correct_order(*pair):
            correct_order.append(i + 1)
    return sum(correct_order)


def puzzle_2() -> None:
    """Puzzle 2."""
    ...


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_code = parse_distress_signal_code(example_input)
    ex_res = puzzle_1(ex_code)
    check_result(13, ex_res)
    res1 = puzzle_1(parse_distress_signal_code(read_input_to_string(DAY)))
    check_result(6101, res1)

    # Puzzle 2.
    ...

    print_results(DAY, TITLE, result1=res1, result2=None)


if __name__ == "__main__":
    main()
