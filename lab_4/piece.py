import random

from constants import Constants


class Piece(object):

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = Constants.SHAPE_COLORS[Constants.SHAPES.index(shape)]
        self.rotation = 0

    def convert_shape_format(self):
        positions = []
        format = self.shape[self.rotation % len(self.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((self.x + j, self.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, grid):
        accepted_positions = [[(j, i) for j in range(Constants.GRID_COLS) if
                               grid[i][j] == Constants.COLOR_BLACK] for i in range(Constants.GRID_ROWS)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.convert_shape_format()

        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False

        return True


def get_shape():
    return Piece(Constants.START_POSITION_X,
                 Constants.START_POSITION_Y,
                 random.choice(Constants.SHAPES))
