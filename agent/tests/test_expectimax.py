from agent.expectimax import _chance_cache, _max_cache, choose_move, clear_cache, search_depth
from game.moves import move_down, move_left, move_right, move_up

MOVE_FNS = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down,
}


def test_search_depth_adaptive():
    crowded = [
        [2, 4, 8, 16],
        [4, 8, 16, 32],
        [8, 16, 32, 64],
        [16, 32, 64, 128],
    ]
    open_board = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert search_depth(crowded, max_depth=3) == 3
    assert search_depth(open_board, max_depth=3) == 2
    assert search_depth(open_board, max_depth=2) == 2


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


def test_choose_move_populates_cache():
    grid = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    clear_cache()
    choose_move(grid, depth=2)
    assert len(_max_cache) > 0
    assert len(_chance_cache) > 0


def test_clear_cache_empties_transposition_table():
    grid = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    choose_move(grid, depth=2)
    clear_cache()
    assert len(_max_cache) == 0
    assert len(_chance_cache) == 0
