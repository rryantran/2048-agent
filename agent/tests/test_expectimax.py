from agent.expectimax import choose_move
from game.moves import move_down, move_left, move_right, move_up

MOVE_FNS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}


def test_choose_move_prefers_merge():
    grid = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert choose_move(grid, depth=1) == "left"


def test_choose_move_returns_valid_direction_on_stuck_board():
    grid = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    direction = choose_move(grid, depth=1)
    assert direction in MOVE_FNS


def test_choose_move_result_is_legal_move():
    grid = [
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 0, 0],
    ]
    direction = choose_move(grid, depth=2)
    _, moved, _ = MOVE_FNS[direction](grid)
    assert moved
