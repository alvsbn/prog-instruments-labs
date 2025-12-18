from constants import Constants


def create_grid(locked_positions={}):
    grid = [[Constants.COLOR_BLACK for x in range(Constants.GRID_COLS)] for x in range(Constants.GRID_ROWS)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if Constants.COLOR_BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
