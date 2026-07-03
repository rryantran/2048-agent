import argparse
import random
import statistics

from agent.expectimax import SEARCH_DEPTH, choose_move
from game.grid import is_game_over, max_tile, new_grid, spawn_random_tile
from game.moves import move_down, move_left, move_right, move_up

MOVE_FNS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}


def play_game(depth: int = SEARCH_DEPTH, game_number: int = 0) -> dict[str, int]:
    """Play one game and return score, max tile, and move count"""

    grid = new_grid()
    score = 0
    moves = 0

    while not is_game_over(grid):
        direction = choose_move(grid, depth=depth)
        if direction is None:
            break

        grid, moved, gained = MOVE_FNS[direction](grid)
        if not moved:
            break

        score += gained
        grid = spawn_random_tile(grid)
        moves += 1

    if game_number > 0:
        print(f"Game {game_number} finished")

    return {
        "score": score,
        "max_tile": max_tile(grid),
        "moves": moves,
    }


def print_board(grid: list[list[int]], score: int) -> None:
    print()

    for row in grid:
        cells = [f"{cell:4}" if cell else "   ." for cell in row]
        print(" ".join(cells))

    print(f"Score: {score}  |  Max tile: {max_tile(grid)}")
    print()


def simulate_verbose(depth: int = SEARCH_DEPTH) -> dict[str, int]:
    """Play one game with board printed after each move"""
    grid = new_grid()
    score = 0
    move_number = 0

    print("Initial board:")
    print_board(grid, score)

    while not is_game_over(grid):
        direction = choose_move(grid, depth=depth)
        if direction is None:
            break

        grid, moved, gained = MOVE_FNS[direction](grid)
        if not moved:
            break

        score += gained
        grid = spawn_random_tile(grid)
        move_number += 1

        print(f"Move {move_number}: {direction}")
        print_board(grid, score)

    result = {
        "score": score,
        "max_tile": max_tile(grid),
        "moves": move_number,
    }

    print(f"Game over after {result['moves']} moves")
    print(f"Final score: {result['score']}")
    print(f"Max tile: {result['max_tile']}")

    return result


def batch_simulate(games: int, depth: int = SEARCH_DEPTH, seed: int | None = None) -> list[dict[str, int]]:
    """Play multiple games and print aggregate stats"""

    if seed is not None:
        random.seed(seed)

    print(f"Playing {games} games...")
    print()

    results = [play_game(depth=depth, game_number=i+1) for i in range(games)]

    scores = [r["score"] for r in results]
    max_tiles = [r["max_tile"] for r in results]
    move_counts = [r["moves"] for r in results]

    print(f"Games played: {games}")
    print(f"Search depth: {depth}")
    if seed is not None:
        print(f"Seed: {seed}")
    print()

    print(f"Avg score:     {statistics.mean(scores):.1f}")
    print(f"Best score:    {max(scores)}")
    print(f"Avg max tile:  {statistics.mean(max_tiles):.1f}")
    print(f"Best max tile: {max(max_tiles)}")
    print(f"Avg moves:     {statistics.mean(move_counts):.1f}")
    print()
    print(f"512:  {sum(t >= 512 for t in max_tiles)}/{games} ({100 * sum(t >= 512 for t in max_tiles) / games:.0f}%)")
    print(f"1024: {sum(t >= 1024 for t in max_tiles)}/{games} ({100 * sum(t >= 1024 for t in max_tiles) / games:.0f}%)")
    print(f"2048: {sum(t >= 2048 for t in max_tiles)}/{games} ({100 * sum(t >= 2048 for t in max_tiles) / games:.0f}%)")
    print(f">2048: {sum(t > 2048 for t in max_tiles)}/{games} ({100 * sum(t > 2048 for t in max_tiles) / games:.0f}%)")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate 2048 games with expectimax agent")
    parser.add_argument(
        "-n", "--games",
        type=int,
        default=1,
        help="Number of games to play (default: 1)",
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=SEARCH_DEPTH,
        help=f"Expectimax search depth (default: {SEARCH_DEPTH})",
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible games",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Batch mode: no per-move output (default when --games > 1)",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.games == 1 and not args.quiet:
        simulate_verbose(depth=args.depth)
    else:
        batch_simulate(games=args.games, depth=args.depth, seed=args.seed)


if __name__ == "__main__":
    main()
