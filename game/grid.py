import random

from game import moves

BOARD_SIZE = 4


def new_grid() -> list[list[int]]:
    """Create a new grid with two random tiles"""

    grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    grid = spawn_random_tile(grid)
    grid = spawn_random_tile(grid)

    return grid


def get_empty_cells(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Get the coordinates of empty cells in the grid"""

    return [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if grid[row][col] == 0]


def place_tile(grid: list[list[int]], row: int, col: int, value: int) -> list[list[int]]:
    """Place a tile in the grid at the given coordinates"""

    if grid[row][col] != 0:
        raise ValueError(f"Cell ({row}, {col}) is not empty")

    new_grid = [r[:] for r in grid]  # Shallow copy rows
    new_grid[row][col] = value

    return new_grid


def spawn_random_tile(grid: list[list[int]]) -> list[list[int]]:
    """Spawn a random tile in an empty cell"""

    empty_tiles = get_empty_cells(grid)

    if not empty_tiles:
        return [row[:] for row in grid]  # Shallow copy rows

    row, col = random.choice(empty_tiles)  # Random empty cell

    # 90% chance of spawning a 2, 10% chance of spawning a 4
    if random.random() < 0.9:
        value = 2
    else:
        value = 4

    return place_tile(grid, row, col, value)


def is_game_over(grid: list[list[int]]) -> bool:
    """Check if the game is over (no moves possible)"""

    move_fns = (moves.move_left, moves.move_right,
                moves.move_up, moves.move_down)

    return not any(move_fn(grid)[1] for move_fn in move_fns)


def max_tile(grid: list[list[int]]) -> int:
    """Return the maximum tile in the grid"""

    return max(max(row) for row in grid)
