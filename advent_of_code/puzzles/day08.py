"""Advent of Code 2022 – Day 8. Treetop Tree House."""

from typing import Final

import numpy as np
import numpy.typing as npt

from advent_of_code.checks import check_result
from advent_of_code.cli_helpers import print_results
from advent_of_code.data import read_input_to_string

DAY: Final[int] = 8
TITLE: Final[str] = "Treetop Tree House"

example_input = """
30373
25512
65332
33549
35390
"""


def parse_input_to_array(input_str: str) -> npt.NDArray[np.int_]:
    """Parse tree height data to a Numpy array."""
    data: list[list] = []
    for line in input_str.strip().splitlines():
        data.append([int(x) for x in line.strip()])
    return np.asarray(data, dtype=np.int_)


def mark_visible_trees_along_row_from_left(
    ary: npt.NDArray[np.int_], mask: npt.NDArray[np.bool_]
) -> npt.NDArray[np.bool_]:
    """Mark the visible trees along each row from the left.

    Args:
        ary (npt.NDArray[np.int_]): Tree heights array.
        mask (npt.NDArray[np.bool_]): Mask for whether a tree is visible or not.

    Returns:
        npt.NDArray[np.bool_]: Updated mask to mark if each tree is visible from the
        left.
    """
    for r in range(ary.shape[0]):
        row = ary[r, :].copy()
        mask_row = mask[r, :].copy()
        for i in range(len(row)):
            if mask_row[i]:
                continue
            if np.all(row[:i] < row[i]):
                mask_row[i] = True
        mask[r, :] = mask_row
    return mask


def puzzle_1(tree_heights: npt.NDArray[np.int_]) -> int:
    """Puzzle 1."""
    tree_heights = tree_heights.copy()
    mask = np.zeros_like(tree_heights, dtype=bool)
    for _ in range(4):
        mask = mark_visible_trees_along_row_from_left(tree_heights, mask)
        tree_heights = np.rot90(tree_heights)
        mask = np.rot90(mask)
    n_visible = np.sum(mask.astype(int))
    return n_visible


def score_trees_along_row_from_right(
    ary: npt.NDArray[np.int_], scores: npt.NDArray[np.int_]
) -> npt.NDArray[np.int_]:
    """Calculate the scenic score for each tree from the right.

    Args:
        ary (npt.NDArray[np.int_]): Tree height matrix.
        scores (npt.NDArray[np.int_]): Current scenic scores for each tree.

    Returns:
        npt.NDArray[np.int_]: Updated scenic score matrix for the view to the right of
        each tree.
    """
    for r in range(ary.shape[0]):
        row = ary[r, :].copy()
        row_scores = np.ones_like(row)
        for i in range(len(row)):
            h = row[i]
            to_right = row[(i + 1) :]
            next_tree = np.where(to_right >= h)[0]
            if len(next_tree) == 0:
                row_scores[i] = len(to_right)
            else:
                row_scores[i] = next_tree[0] + 1
        scores[r, :] = scores[r, :] * row_scores
    return scores


def puzzle_2(tree_heights: npt.NDArray[np.int_]) -> int:
    """Puzzle 2."""
    tree_heights = tree_heights.copy()
    scores = np.ones_like(tree_heights, dtype=int)
    for _ in range(4):
        scores = score_trees_along_row_from_right(tree_heights, scores)
        tree_heights = np.rot90(tree_heights)
        scores = np.rot90(scores)
    return np.max(scores)


def main() -> None:
    """Execute puzzles."""
    # Puzzle 1.
    ex_res = puzzle_1(parse_input_to_array(example_input))
    check_result(21, ex_res)
    res1 = puzzle_1(parse_input_to_array(read_input_to_string(DAY)))
    check_result(1801, res1)

    # Puzzle 2.
    ex_res = puzzle_2(parse_input_to_array(example_input))
    check_result(8, ex_res)
    res2 = puzzle_2(parse_input_to_array(read_input_to_string(DAY)))
    check_result(209880, res2)

    print_results(DAY, TITLE, result1=res1, result2=res2)


if __name__ == "__main__":
    main()
