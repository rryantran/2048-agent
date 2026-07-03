from game.grid import get_empty_cells, is_game_over, place_tile
from game.moves import move_down, move_left, move_right, move_up

from agent.heuristic import evaluate

MAX_SEARCH_DEPTH = 2
ADAPTIVE_EMPTY_THRESHOLD = 6

DIRECTIONS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}

SPAWN_PROBS = [(2, 0.9), (4, 0.1)]

# Key is a tuple of the grid and depth, value is utility
_max_cache = {}
_chance_cache = {}


def _grid_key(grid: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    """Return a tuple of the grid"""

    return tuple(tuple(row) for row in grid)


def clear_cache() -> None:
    """Clear cache for new move"""

    _max_cache.clear()
    _chance_cache.clear()


def search_depth(grid: list[list[int]], max_depth: int = MAX_SEARCH_DEPTH) -> int:
    """Use max depth on crowded boards, one less on sparse boards for performance"""

    if max_depth < 3:
        return max_depth

    if len(get_empty_cells(grid)) <= ADAPTIVE_EMPTY_THRESHOLD:
        return max_depth

    return max_depth - 1


def choose_move(grid: list[list[int]], depth: int = MAX_SEARCH_DEPTH) -> str | None:
    """Return the direction with the highest expected utility"""

    clear_cache()

    depth = search_depth(grid, depth)

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

    key = (_grid_key(grid), depth)

    # Return cached value
    if key in _max_cache:
        return _max_cache[key]

    if depth == 0 or is_game_over(grid):
        result = evaluate(grid)
    else:
        util = float("-inf")

        for move_fn in DIRECTIONS.values():
            new_grid, moved, _ = move_fn(grid)

            if not moved:
                continue

            util = max(util, _chance_node(new_grid, depth - 1))

        result = util

    _max_cache[key] = result

    return result


def _chance_node(grid: list[list[int]], depth: int) -> float:
    """Return the expected utility of the chance node"""

    key = (_grid_key(grid), depth)

    # Return cached value
    if key in _chance_cache:
        return _chance_cache[key]

    if is_game_over(grid):
        result = evaluate(grid)
    else:
        empty_cells = get_empty_cells(grid)

        cell_prob = 1.0 / len(empty_cells)
        util = 0.0

        for row, col in empty_cells:
            for value, spawn_prob in SPAWN_PROBS:
                child = place_tile(grid, row, col, value)
                util += cell_prob * spawn_prob * _max_node(child, depth)

        result = util

    _chance_cache[key] = result

    return result
