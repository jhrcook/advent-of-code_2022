"""Advent of Code 2022 – Day 12. Hill Climbing Algorithm."""

from itertools import product
from string import ascii_lowercase
from typing import Final

import networkx as nx
import numpy as np

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 12
TITLE: Final[str] = "Hill Climbing Algorithm"

example_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

Coord = tuple[int, int]

character_to_number_map: dict[str, int] = {c: i for i, c in enumerate(ascii_lowercase)}


def _convert_char_to_num(c: str) -> int:
    if c == "S":
        c = "a"
    elif c == "E":
        c = "z"
    return character_to_number_map[c]


def parse_input_to_directed_graph(input_str: str) -> nx.DiGraph:
    """Parse input data into a directed graph.

    Args:
        input_str (str): Puzzle input string.

    Returns:
        nx.DiGraph: Directed graph of locations in the map.
    """
    # Parse map into a matrix of characters.
    char_ary = np.array([list(r) for r in input_str.strip().splitlines()])

    # Convert the character matrix into the node values ("heights" in the puzzle.)
    _fxn = np.vectorize(_convert_char_to_num)
    num_ary = _fxn(char_ary)

    # Initialize a graph object.
    graph = nx.DiGraph()
    start: Coord = (-1, -1)
    end: Coord = (-1, -1)

    # Add nodes.
    for r, c in product(range(char_ary.shape[0]), range(char_ary.shape[1])):
        char = char_ary[r, c]
        num = num_ary[r, c]
        graph.add_node((r, c), name=char, weight=num)
        if char == "S":
            start = (r, c)
        elif char == "E":
            end = (r, c)

    # Add edges.
    max_r, max_c = char_ary.shape
    for r, c in product(range(char_ary.shape[0]), range(char_ary.shape[1])):
        a = num_ary[r, c]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            _r, _c = r + dr, c + dc
            if _r < 0 or _c < 0 or _r >= max_r or _c >= max_c:
                continue
            b = num_ary[_r, _c]
            if (b - a) <= 1:
                graph.add_edge((r, c), (_r, _c))

    # Check some assertion about the results.
    assert nx.number_of_nodes(graph) == (num_ary.shape[0] * num_ary.shape[1])
    assert start != (-1, -1), "Start location not found."
    assert end != (-1, -1), "End location not found."

    return graph


def puzzle_1(terrain_graph: nx.DiGraph) -> int:
    """Puzzle 1."""
    start: Coord = (-1, -1)
    end: Coord = (-1, -1)
    node_names = nx.get_node_attributes(terrain_graph, "name")
    for node in terrain_graph.nodes:
        if node_names[node] == "S":
            start = node
        elif node_names[node] == "E":
            end = node

    assert start != (-1, -1)
    assert end != (-1, -1)

    shortest_path_len = nx.shortest_path_length(terrain_graph, source=start, target=end)
    assert isinstance(shortest_path_len, int)
    return shortest_path_len


def puzzle_2(terrain_graph: nx.DiGraph) -> int:
    """Puzzle 2."""
    a_nodes: list[Coord] = []
    end: Coord = (-1, -1)
    node_names = nx.get_node_attributes(terrain_graph, "name")
    for node in terrain_graph.nodes:
        if node_names[node] in ("a", "S"):
            a_nodes.append(node)
        elif node_names[node] == "E":
            end = node

    assert end != (-1, -1)
    assert len(a_nodes) > 1

    shortest_dist = nx.number_of_edges(terrain_graph)
    for start in a_nodes:
        try:
            sp = nx.shortest_path_length(terrain_graph, source=start, target=end)
            assert isinstance(sp, int)
            if sp < shortest_dist:
                shortest_dist = sp
        except nx.exception.NetworkXNoPath:
            ...

    return shortest_dist


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_terrain = parse_input_to_directed_graph(example_input)
    ex_res = puzzle_1(ex_terrain)
    check_result(31, ex_res)
    terrain = parse_input_to_directed_graph(read_input_to_string(DAY))
    res1 = puzzle_1(terrain)
    check_result(447, res1)

    # Puzzle 2
    ex_terrain = parse_input_to_directed_graph(example_input)
    ex_res = puzzle_2(ex_terrain)
    check_result(29, ex_res)
    terrain = parse_input_to_directed_graph(read_input_to_string(DAY))
    res2 = puzzle_2(terrain)
    check_result(446, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
