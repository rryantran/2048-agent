import math
from game.grid import BOARD_SIZE, get_empty_cells

WEIGHTS = {
    "empty_cells": 1.0,
    "monotonicity": 1.0,
    "smoothness": 1.0,
}


def empty_cells_score(grid: list[list[int]]) -> float:
    """Reward for having empty cells"""

    return len(get_empty_cells(grid)) / (BOARD_SIZE ** 2)


def _line_penalty(line: list[int]) -> float:
    """Penalty for one row or column; picks the better of the two"""

    def increasing_penalty(seq: list[int]) -> float:
        penalty = 0.0
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]

            if a == 0 or b == 0:
                continue

            if a > b:
                penalty += math.log2(a) - math.log2(b)

        return penalty

    return min(increasing_penalty(line), increasing_penalty(line[::-1]))


def _monotonicity_penalty(grid: list[list[int]]) -> float:
    """Sum best row and column penalties (lower is more monotonic)"""

    penalty = sum(_line_penalty(row) for row in grid)

    for col in range(BOARD_SIZE):
        column = [grid[row][col] for row in range(BOARD_SIZE)]
        penalty += _line_penalty(column)

    return penalty


def _smoothness_penalty(grid: list[list[int]]) -> float:
    """Sum log gaps between adjacent tiles (lower is smoother)."""

    penalty = 0.0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            a = grid[row][col]

            if a == 0:
                continue

            if col + 1 < BOARD_SIZE:
                b = grid[row][col + 1]

                if b != 0:
                    penalty += abs(math.log2(a) - math.log2(b))

            if row + 1 < BOARD_SIZE:
                b = grid[row + 1][col]

                if b != 0:
                    penalty += abs(math.log2(a) - math.log2(b))

    return penalty


def evaluate(grid: list[list[int]]) -> float:
    """Evaluate the score of the grid"""

    return (
        WEIGHTS["empty_cells"] * empty_cells_score(grid)
        - WEIGHTS["monotonicity"] * _monotonicity_penalty(grid)
        - WEIGHTS["smoothness"] * _smoothness_penalty(grid)
    )
