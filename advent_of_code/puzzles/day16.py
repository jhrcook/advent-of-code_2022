"""Advent of Code 2022 – Day 16. Proboscidea Volcanium."""

from __future__ import annotations

import re
from collections.abc import Iterable
from copy import copy
from dataclasses import dataclass
from itertools import product
from typing import Final

import networkx as nx

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string
from advent_of_code.utilities import timer

DAY: Final[int] = 16
TITLE: Final[str] = "Proboscidea Volcanium"

example_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


class Valve:
    """Valve in the volcano."""

    def __init__(self, id: str, flow_rate: int, leads_to: tuple[str, ...]) -> None:
        self.id = id
        self.flow_rate = flow_rate
        self.leads_to = leads_to

    def __str__(self) -> str:
        msg = f"valve {self.id} has flow rate {self.flow_rate}\n"
        msg += f"  connections: {', '.join(self.leads_to)}"
        return msg

    def __repr__(self) -> str:
        return str(self)


def parse_valve_data(input_str: str) -> dict[str, Valve]:
    """Parse input data into a collection of valves."""
    valves: dict[str, Valve] = {}
    for line in input_str.strip().splitlines():
        _split_line = line.split("; ")
        assert len(_split_line) == 2
        valve_info, connections_info = _split_line[0], _split_line[1]
        _id = re.findall(r"(?<=Valve )\w+", valve_info)[0].strip()
        _rate = int(re.findall(r"(?<=rate=)\d+", valve_info)[0].strip())
        _leads_to_regex = (
            "tunnels lead to valves"
            if "tunnels" in connections_info
            else "tunnel leads to valve"
        )
        _leads_to = (
            re.findall(rf"(?<={_leads_to_regex} ).+", connections_info)[0]
            .strip()
            .split(", ")
        )
        assert _id not in valves, f"Duplicate valve IDs: {_id}"
        valves[_id] = Valve(id=_id, flow_rate=_rate, leads_to=tuple(_leads_to))
    return valves


def _open_node_name(v: Valve) -> str:
    return f"open_{v.id}"


def convert_valve_info_to_directed_multigraph(
    valves: Iterable[Valve],
) -> nx.MultiDiGraph:
    """Convert a collection of valves into a graph structure.

    The opening of a valve is represented as a different node from the valve itself.
    This node is only included for valves with flow rates > 0.

    Args:
        valves (Iterable[Valve]): Collection of valves with their flow rates and
        connections.

    Returns:
        nx.MultiDiGraph: Graph representation of the valves.
    """
    gr = nx.MultiDiGraph()
    # Add all nodes with edges between valves location and opening action.
    for valve in valves:
        gr.add_node(valve.id, type="valve")
        if valve.flow_rate > 0:
            open_node = _open_node_name(valve)
            gr.add_node(open_node, type="open", flow_rate=valve.flow_rate)
            gr.add_edge(valve.id, open_node)

    # Add all edges.
    for valve in valves:
        for connection in valve.leads_to:
            gr.add_edge(valve.id, connection)
            if valve.flow_rate > 0:
                gr.add_edge(_open_node_name(valve), connection)
    return gr


@dataclass
class ValvePath:
    """Valve path."""

    def __init__(
        self, nodes: list[str], steps_left: int, score: int, opened_valves: set[str]
    ) -> None:
        self.nodes = sorted(copy(nodes))
        self.steps_left = steps_left
        self.score = score
        self.opened_valves = copy(opened_valves)

    def __copy__(self) -> ValvePath:
        return ValvePath(
            nodes=copy(self.nodes),
            steps_left=self.steps_left,
            score=self.score,
            opened_valves=copy(self.opened_valves),
        )

    def step(self, to_nodes: list[str], gr: nx.Graph) -> None:
        """Take a step to neighboring nodes.

        Args:
            to_nodes (list[str]): New nodes to step to.
            gr (nx.Graph): Graph of the network (is not changed).
        """
        self.nodes = sorted(copy(to_nodes))
        self.steps_left -= 1
        for node in to_nodes:
            if "open" in node:
                self.score += self.steps_left * gr.nodes[node]["flow_rate"]
                self.opened_valves.add(node)

    @property
    def id(self) -> str:
        """Identifier string for the valve."""
        opened_valves_id = "__".join(sorted(list(self.opened_valves)))
        return f"{self.nodes}__{self.steps_left}__{self.score}__{opened_valves_id}"

    def __hash__(self) -> int:
        return hash(self.id)


class PathTracker:
    """Tracker of paths through the volcano."""

    def __init__(self) -> None:
        self.top_score: int = 0
        self.n_paths: int = 0
        self.path_states: set[ValvePath] = set()

    def have_seen_path(self, path: ValvePath) -> bool:
        """Has the state already been seen?

        The current path is added to the collection if it has not been seen yet.

        Args:
            path (ValvePath): Current path to check or add.

        Returns:
            bool: Whether the path state has already been seen.
        """
        if path in self.path_states:
            return True
        self.path_states.add(copy(path))
        return False

    def update(self, path: ValvePath) -> None:
        """Update the tracker logging data with a finished path."""
        if path in self.path_states:
            self.path_states.add(copy(path))
        self.top_score = max(self.top_score, path.score)
        self.n_paths += 1


_shortest_path_lengths: dict[tuple[str, str], int] = {}


def _memoize_shortest_path_for_immutable_graph(
    gr: nx.Graph, source: str, target: str
) -> int:
    path = (source, target)
    if path in _shortest_path_lengths:
        return _shortest_path_lengths[path]

    path_len = nx.shortest_path_length(gr, source=source, target=target)
    assert isinstance(path_len, int)
    _shortest_path_lengths[path] = path_len
    return path_len


def _find_shortest_dist(gr: nx.Graph, nodes: Iterable[str], target: str) -> int:
    return min(
        [_memoize_shortest_path_for_immutable_graph(gr, n, target) for n in nodes]
    )


def calculate_potential_max_score(gr: nx.Graph, path: ValvePath) -> int:
    """Calculate the maximum possible flow rate from the current state.

    Args:
        gr (nx.Graph): Graph of valves.
        path (ValvePath): Current path state.

    Returns:
        int: Maximum possible flow rate if the shortest paths between all remaining
        valves could be taken.
    """
    potential_score = path.score
    for valve in gr.nodes:
        if "open" not in valve or valve in path.opened_valves:
            continue
        remaining_time = path.steps_left - _find_shortest_dist(gr, path.nodes, valve)
        if remaining_time <= 0:
            continue
        potential_score += remaining_time * gr.nodes[valve]["flow_rate"]
    return potential_score


def find_max_flow_path(
    gr: nx.Graph, path: ValvePath, tracker: PathTracker, all_valves: set[str]
) -> None:
    """Score paths through the cave to maximize flow rate.

    Args:
        gr (nx.Graph): Graph of valves.
        path (ValvePath): Current state of the path through the cave.
        tracker (PathTracker): Tracker of maximum score.
        all_valves (set[str]): Set of all valves that can be opened.
    """
    # Finish criteria:
    #   1. If the state has already been seen.
    #   2. If there are no steps left
    #   3. If all the valves have been visited already.
    #   4. If possible maximum score is less than the current max score.
    if (
        tracker.have_seen_path(path)
        or path.steps_left == 0
        or path.steps_left == all_valves
        or calculate_potential_max_score(gr, path) <= tracker.top_score
    ):
        tracker.update(path)
        return

    # Iterate over possible next steps and recurse into this function.
    for neighbors in product(*[gr.neighbors(n) for n in path.nodes]):
        if any([n in path.opened_valves for n in neighbors]):
            continue
        if len(neighbors) != len(set(neighbors)):
            continue
        new_path = copy(path)
        new_path.step(to_nodes=list(neighbors), gr=gr)
        find_max_flow_path(gr=gr, path=new_path, tracker=tracker, all_valves=all_valves)


def _collect_all_valve_names(gr: nx.Graph) -> set[str]:
    openable_valves: set[str] = set()
    for n in gr.nodes:
        if "open" in n:
            openable_valves.add(n)
    return openable_valves


@timer
def puzzle_1(valves: Iterable[Valve], depth: int) -> int:
    """Puzzle 1."""
    gr = convert_valve_info_to_directed_multigraph(valves)
    tracker = PathTracker()
    find_max_flow_path(
        gr,
        path=ValvePath(["AA"], depth, score=0, opened_valves=set()),
        tracker=tracker,
        all_valves=_collect_all_valve_names(gr),
    )
    return tracker.top_score


@timer
def puzzle_2(valves: Iterable[Valve], depth: int) -> int:
    """Puzzle 2."""
    gr = convert_valve_info_to_directed_multigraph(valves)
    tracker = PathTracker()
    find_max_flow_path(
        gr,
        path=ValvePath(["AA", "AA"], depth, score=0, opened_valves=set()),
        tracker=tracker,
        all_valves=_collect_all_valve_names(gr),
    )
    return tracker.top_score


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_valves = parse_valve_data(example_input)
    ex_res = puzzle_1(ex_valves.values(), depth=30)
    check_result(1651, ex_res)
    valves = parse_valve_data(read_input_to_string(DAY))
    res1 = puzzle_1(valves.values(), depth=30)
    check_result(1701, res1)

    # Puzzle 2.
    ex_valves = parse_valve_data(example_input)
    ex_res = puzzle_2(ex_valves.values(), depth=26)
    check_result(1707, ex_res)
    valves = parse_valve_data(read_input_to_string(DAY))
    res2 = puzzle_2(valves.values(), depth=26)
    check_result(2455, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
