from game.grid import get_empty_cells, is_game_over, place_tile
from game.moves import move_down, move_left, move_right, move_up

from agent.heuristic import evaluate

SEARCH_DEPTH = 2

DIRECTIONS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}

SPAWN_PROBS = [(2, 0.9), (4, 0.1)]


def choose_move(grid: list[list[int]], depth: int = SEARCH_DEPTH) -> str:
    """Return the direction with the highest expected utility"""

    best_direction = None
    best_value = float("-inf")

    # Explore all possible moves with search depth and find the move with highest expected utility
    for direction, move_fn in DIRECTIONS.items():
        new_grid, moved, _ = move_fn(grid)

        if not moved:
            continue

        value = _chance_node(new_grid, depth - 1)

        if value > best_value:
            best_value = value
            best_direction = direction

    return best_direction


def _max_node(grid: list[list[int]], depth: int) -> float:
    """Return the maximum utility of the max node"""

    if depth == 0 or is_game_over(grid):
        return evaluate(grid)

    best_value = float("-inf")

    for move_fn in DIRECTIONS.values():
        new_grid, moved, _ = move_fn(grid)
        if not moved:
            continue

        best_value = max(best_value, _chance_node(new_grid, depth - 1))

    return best_value


def _chance_node(grid: list[list[int]], depth: int) -> float:
    """Return the expected utility of the chance node"""

    if is_game_over(grid):
        return evaluate(grid)

    empty_cells = get_empty_cells(grid)

    cell_prob = 1.0 / len(empty_cells)
    expected_value = 0.0

    for row, col in empty_cells:
        for value, spawn_prob in SPAWN_PROBS:
            child = place_tile(grid, row, col, value)
            expected_value += cell_prob * spawn_prob * _max_node(child, depth)

    return expected_value
