from game.grid import BOARD_SIZE, get_empty_cells, max_tile

WEIGHTS = {
    "empty_cells": 2.7,
    "corner": 0.2,
    "monotonicity": 0.08,
    "smoothness": 0.1,
}


def empty_cells_score(grid: list[list[int]]) -> float:
    """Reward for having empty cells"""

    return len(get_empty_cells(grid)) / 16


def corner_score(grid: list[list[int]]) -> float:
    """Reward for having max tile in corner"""

    max_num = max_tile(grid)
    bonus = 0.0

    if grid[3][3] == max_num or grid[0][0] == max_num:
        bonus = max_num / 2048

    return bonus


def _line_score(line: list[int]) -> float:
    """Score monotonicity of a single row or column"""
    score = 0.0

    for i in range(len(line) - 1):
        current, next = line[i], line[i + 1]
        if current == 0 or next == 0:
            continue
        if current > next:
            score += next
        else:
            score += current

    return score


def monotonicity_score(grid: list[list[int]]) -> float:
    """Reward rows and columns that increase or decrease in value"""
    total = 0.0

    for row in grid:
        total += max(_line_score(row), _line_score(row[::-1]))

    for col_index in range(BOARD_SIZE):
        column = [grid[row][col_index] for row in range(BOARD_SIZE)]
        total += max(_line_score(column), _line_score(column[::-1]))

    return total / 100


def smoothness_penalty(grid: list[list[int]]) -> float:
    """Penalty for adjacent tiles with very different values."""
    penalty = 0.0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = grid[row][col]
            if value == 0:
                continue
            if col + 1 < BOARD_SIZE and grid[row][col + 1]:
                penalty += abs(value - grid[row][col + 1])
            if row + 1 < BOARD_SIZE and grid[row + 1][col]:
                penalty += abs(value - grid[row + 1][col])

    return penalty / 100


def evaluate(grid: list[list[int]]) -> float:
    """Evaluate the score of the grid"""

    return (
        WEIGHTS["empty_cells"] * empty_cells_score(grid)
        + WEIGHTS["corner"] * corner_score(grid)
        + WEIGHTS["monotonicity"] * monotonicity_score(grid)
        - WEIGHTS["smoothness"] * smoothness_penalty(grid)
    )
