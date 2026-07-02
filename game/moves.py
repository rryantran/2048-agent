def _slide_merge_row(row: list[int]) -> tuple[list[int], int]:
    """Slide and merge a single row left, returning (merged row, score gained)"""

    tiles = [value for value in row if value != 0]
    merged = []
    score = 0
    skip_next = False

    for i, value in enumerate(tiles):
        if skip_next:
            skip_next = False
            continue

        if i + 1 < len(tiles) and value == tiles[i + 1]:
            merged_value = value * 2
            merged.append(merged_value)
            score += merged_value
            skip_next = True  # Skip next value to avoid double merging
        else:
            merged.append(value)

    # Pad with zeros to original length
    merged.extend([0] * (len(row) - len(merged)))

    return merged, score


def _rotate_cw(grid: list[list[int]]) -> list[list[int]]:
    """Rotate grid 90 degrees clockwise"""

    # Reverse grid rows
    # Transpose grid using zip(*grid)
    return [list(row) for row in zip(*grid[::-1])]


def _rotate_ccw(grid: list[list[int]]) -> list[list[int]]:
    """Rotate grid 90 degrees counter-clockwise"""

    # Transpose grid using zip(*grid)
    # Reverse grid rows
    return [list(row) for row in zip(*grid)][::-1]


def move_left(grid: list[list[int]]) -> tuple[list[list[int]], bool, int]:
    """Move all tiles left, merging adjacent tiles of the same value"""

    new_grid = []
    score_gained = 0

    for row in grid:
        merged_row, row_score = _slide_merge_row(row)
        new_grid.append(merged_row)
        score_gained += row_score

    moved = (new_grid != grid)

    return new_grid, moved, score_gained


def move_right(grid: list[list[int]]) -> tuple[list[list[int]], bool, int]:
    """Move all tiles right, merging adjacent tiles of the same value"""

    rotated = _rotate_cw(_rotate_cw(grid))
    new_rotated, moved, score_gained = move_left(rotated)

    return _rotate_cw(_rotate_cw(new_rotated)), moved, score_gained


def move_up(grid: list[list[int]]) -> tuple[list[list[int]], bool, int]:
    """Move all tiles up, merging adjacent tiles of the same value"""

    rotated = _rotate_ccw(grid)
    new_rotated, moved, score_gained = move_left(rotated)

    return _rotate_cw(new_rotated), moved, score_gained


def move_down(grid: list[list[int]]) -> tuple[list[list[int]], bool, int]:
    """Move all tiles down, merging adjacent tiles of the same value"""

    rotated = _rotate_cw(grid)
    new_rotated, moved, score_gained = move_left(rotated)

    return _rotate_ccw(new_rotated), moved, score_gained
