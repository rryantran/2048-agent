from agent.expectimax import choose_move
from game.grid import is_game_over, new_grid, spawn_random_tile
from game.moves import move_down, move_left, move_right, move_up

MOVE_FNS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}


def max_tile(grid: list[list[int]]) -> int:
    return max(max(row) for row in grid)


def print_board(grid: list[list[int]], score: int) -> None:
    print()

    for row in grid:
        cells = [f"{cell:4}" if cell else "   ." for cell in row]
        print(" ".join(cells))

    print(f"Score: {score}  |  Max tile: {max_tile(grid)}")
    print()


def simulate():
    grid = new_grid()
    score = 0
    move_number = 0

    print("Initial board:")
    print_board(grid, score)

    while not is_game_over(grid):
        direction = choose_move(grid)
        grid, _, gained = MOVE_FNS[direction](grid)

        score += gained
        grid = spawn_random_tile(grid)

        move_number += 1

        print(f"Move {move_number}: {direction}")
        print_board(grid, score)

    print(f"Game over after {move_number} moves")
    print(f"Final score: {score}")
    print(f"Max tile: {max_tile(grid)}")


if __name__ == "__main__":
    simulate()
