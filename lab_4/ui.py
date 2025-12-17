import pygame
from constants import Constants


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2),
    Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - label.get_height() / 2
    ))

def draw_grid(surface, row, col):
    sx = Constants.TOP_LEFT_X
    sy = Constants.TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, Constants.COLOR_GRAY, (sx, sy + i * Constants.BLOCK_SIZE),
                         (sx + Constants.PLAY_WIDTH, sy + i * Constants.BLOCK_SIZE))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, Constants.COLOR_GRAY, (sx + j * Constants.BLOCK_SIZE, sy),
                             (sx + j * Constants.BLOCK_SIZE, sy + Constants.PLAY_HEIGHT))  # vertical lines


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, Constants.COLOR_WHITE)

    sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
    sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * Constants.BLOCK_SIZE,
                                  sy + i * Constants.BLOCK_SIZE,
                                  Constants.BLOCK_SIZE,
                                  Constants.BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid):
    surface.fill(Constants.COLOR_BLACK)
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, Constants.COLOR_WHITE)

    surface.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (Constants.TOP_LEFT_X + j * Constants.BLOCK_SIZE,
                              Constants.TOP_LEFT_Y + i * Constants.BLOCK_SIZE,
                              Constants.BLOCK_SIZE, Constants.BLOCK_SIZE), 0)

    # draw grid and border
    draw_grid(surface, Constants.GRID_ROWS, Constants.GRID_COLS)
    pygame.draw.rect(surface, Constants.COLOR_RED,
                     (Constants.TOP_LEFT_X, Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)
    # pygame.display.update()


def draw_current_piece_on_grid(current_piece, grid):
    shape_pos = current_piece.convert_shape_format()

    for i in range(len(shape_pos)):
        x, y = shape_pos[i]
        if y > -1:
            grid[y][x] = current_piece.color
    return shape_pos
