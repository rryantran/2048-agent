from unittest.mock import patch

import pytest

from game import grid


def test_get_empty_cells_all_empty():
    g = [[0] * 4 for _ in range(4)]
    assert len(grid.get_empty_cells(g)) == 16


def test_get_empty_cells_none_empty():
    g = [[2] * 4 for _ in range(4)]
    assert grid.get_empty_cells(g) == []


def test_get_empty_cells_some_empty():
    g = [
        [2, 0, 0, 0],
        [0, 4, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert grid.get_empty_cells(g) == [
        (0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3),
        *((r, c) for r in range(2, 4) for c in range(4)),
    ]


def test_place_tile_without_mutating_original():
    g = [[0] * 4 for _ in range(4)]
    new_g = grid.place_tile(g, 1, 2, 4)

    assert new_g[1][2] == 4
    assert g[1][2] == 0
    assert new_g is not g
    assert new_g[0] is not g[0]


def test_place_tile_raises_on_occupied_cell():
    g = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    with pytest.raises(ValueError):
        grid.place_tile(g, 0, 0, 2)


def test_spawn_random_tile_no_spawn_on_full_board():
    g = [[2] * 4 for _ in range(4)]
    new_g = grid.spawn_random_tile(g)

    assert new_g == g
    assert new_g is not g


@patch("game.grid.random.random", return_value=0.0)
@patch("game.grid.random.choice", return_value=(2, 3))
def test_spawn_random_tile_spawns_two(_choice, _random):
    g = [[0] * 4 for _ in range(4)]
    new_g = grid.spawn_random_tile(g)

    assert new_g[2][3] == 2


@patch("game.grid.random.random", return_value=0.95)
@patch("game.grid.random.choice", return_value=(0, 0))
def test_spawn_random_tile_spawns_four(_choice, _random):
    g = [[0] * 4 for _ in range(4)]
    new_g = grid.spawn_random_tile(g)

    assert new_g[0][0] == 4


@patch("game.grid.random.random", return_value=0.0)
@patch("game.grid.random.choice", side_effect=[(0, 0), (3, 3)])
def test_new_grid_starts_with_two_tiles(_choice, _random):
    g = grid.new_grid()
    tile_count = sum(cell != 0 for row in g for cell in row)

    assert tile_count == 2
    assert g[0][0] == 2
    assert g[3][3] == 2
