import pygame
from constants import Constants
from ui import draw_window, draw_next_shape, draw_text_middle, draw_current_piece_on_grid
from piece import get_shape
from grid import create_grid, clear_rows, check_lost


def update_game_timing(fall_time, level_time, clock):
    fall_time += clock.get_rawtime()
    level_time += clock.get_rawtime()
    clock.tick()
    return fall_time, level_time


def increase_game_difficulty(level_time):
    if level_time / 1000 > Constants.LEVEL_UP_TIME_SECONDS:
        level_time = 0
        if Constants.FALL_SPEED > Constants.FALL_SPEED_MIN:
            Constants.FALL_SPEED -= Constants.FALL_SPEED_DECREMENT
    return level_time


def move_piece_down(current_piece, grid, fall_time):
    change_piece = False
    if fall_time / 1000 >= Constants.FALL_SPEED:
        fall_time = 0
        current_piece.y += 1
        if not (current_piece.valid_space(grid)) and current_piece.y > 0:
            current_piece.y -= 1
            change_piece = True
    return fall_time, change_piece


def handle_player_input(current_piece, grid, run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            handle_single_keypress(event, current_piece, grid)
    return run


def handle_single_keypress(event, current_piece, grid):
    if event.key == pygame.K_LEFT:
        current_piece.x -= 1
        if not current_piece.valid_space(grid):
            current_piece.x += 1

    elif event.key == pygame.K_RIGHT:
        current_piece.x += 1
        if not current_piece.valid_space(grid):
            current_piece.x -= 1
    elif event.key == pygame.K_UP:
        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
        if not current_piece.valid_space(grid):
            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

    if event.key == pygame.K_DOWN:
        current_piece.y += 1
        if not current_piece.valid_space(grid):
            current_piece.y -= 1


def lock_piece_to_grid(shape_pos, current_piece, locked_positions, next_piece, grid, score):
    for pos in shape_pos:
        p = (pos[0], pos[1])
        locked_positions[p] = current_piece.color

    current_piece = next_piece
    next_piece = get_shape()
    change_piece = False

    if clear_rows(grid, locked_positions):
        score += 10

    return current_piece, next_piece, change_piece, score


def main():
    locked_positions = {}
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    win = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        grid = create_grid(locked_positions)
        fall_time, level_time = update_game_timing(fall_time, level_time, clock)
        level_time = increase_game_difficulty(level_time)
        fall_time, change_piece = move_piece_down(current_piece, grid, fall_time)
        run = handle_player_input(current_piece, grid, run)
        shape_pos = draw_current_piece_on_grid(current_piece, grid)

        if change_piece:
            current_piece, next_piece, change_piece, score = lock_piece_to_grid(
                shape_pos, current_piece, locked_positions, next_piece, grid, score
            )

        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, Constants.COLOR_WHITE, win)
    pygame.display.update()
    pygame.time.delay(Constants.GAME_OVER_DELAY_MS)