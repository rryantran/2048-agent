from game import moves


def test_move_left_slide_without_merge():
    g = [
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 0, 0],
    ]
    new_g, moved, score = moves.move_left(g)

    assert moved
    assert score == 0
    assert new_g[0] == [2, 0, 0, 0]
    assert new_g[3] == [4, 0, 0, 0]


def test_move_left_merge_pair():
    g = [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_left(g)

    assert moved
    assert score == 4
    assert new_g[0] == [4, 0, 0, 0]


def test_move_left_double_merge_does_not_chain():
    g = [[2, 2, 4, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_left(g)

    assert moved
    assert score == 12
    assert new_g[0] == [4, 8, 0, 0]


def test_move_left_triple_twos():
    g = [[2, 2, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_left(g)

    assert moved
    assert score == 4
    assert new_g[0] == [4, 2, 0, 0]


def test_move_left_no_op():
    g = [[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_left(g)

    assert not moved
    assert score == 0
    assert new_g == g


def test_move_right_slide_and_merge():
    g = [[0, 0, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_right(g)

    assert moved
    assert score == 4
    assert new_g[0] == [0, 0, 0, 4]


def test_move_up_slide_column():
    g = [
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 4],
    ]
    new_g, moved, score = moves.move_up(g)

    assert moved
    assert score == 0
    assert new_g[0] == [0, 0, 0, 2]
    assert new_g[1] == [0, 0, 0, 4]


def test_move_up_merge_column():
    g = [[2, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    new_g, moved, score = moves.move_up(g)

    assert moved
    assert score == 4
    assert new_g[0] == [4, 0, 0, 0]


def test_move_down_slide_column():
    g = [
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 0, 0],
    ]
    new_g, moved, score = moves.move_down(g)

    assert moved
    assert score == 0
    assert new_g[3] == [0, 4, 2, 0]


def test_move_down_merge_column():
    g = [[0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [2, 0, 0, 0]]
    new_g, moved, score = moves.move_down(g)

    assert moved
    assert score == 4
    assert new_g[3] == [4, 0, 0, 0]


def test_slide_merge_row_empty():
    row, score = moves._slide_merge_row([0, 0, 0, 0])
    assert row == [0, 0, 0, 0]
    assert score == 0
