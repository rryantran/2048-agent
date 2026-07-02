from game.grid import get_empty_cells

WEIGHTS = {
    "empty_cells": 1.0,
}


def empty_cells_score(grid: list[list[int]]) -> float:
    """Score based on the number of empty cells"""

    return len(get_empty_cells(grid))


def evaluate(grid: list[list[int]]) -> float:
    """Evaluate the score of the grid"""

    return (WEIGHTS["empty_cells"] * empty_cells_score(grid))
