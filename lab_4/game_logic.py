import pygame

from constants import Constants
from grid import create_grid, clear_rows, check_lost
from piece import get_shape
from ui import draw_window, draw_next_shape, draw_text_middle, draw_current_piece_on_grid


class TetrisGame:
    def __init__(self):
        pygame.init()
        self.locked_positions = {}
        self.run = True
        self.current_piece = None
        self.next_piece = None
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0
        self.window = None

    def init_game(self):
        self.locked_positions.clear()
        self.run = True
        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0

        if self.window is None:
            self.window = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
            pygame.display.set_caption('Tetris')

    def update_game_timing(self):
        self.fall_time += self.clock.get_rawtime()
        self.level_time += self.clock.get_rawtime()
        self.clock.tick()

    def increase_game_difficulty(self):
        if self.level_time / 1000 > Constants.LEVEL_UP_TIME_SECONDS:
            self.level_time = 0
            if Constants.FALL_SPEED > Constants.FALL_SPEED_MIN:
                Constants.FALL_SPEED -= Constants.FALL_SPEED_DECREMENT

    def move_piece_down(self):
        change_piece = False
        if self.fall_time / 1000 >= Constants.FALL_SPEED:
            self.fall_time = 0
            self.current_piece.y += 1
            grid = create_grid(self.locked_positions)
            if not (self.current_piece.valid_space(grid)) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                change_piece = True
        return change_piece

    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return

            if event.type == pygame.KEYDOWN:
                self.handle_single_keypress(event)

    def handle_single_keypress(self, event):
        grid = create_grid(self.locked_positions)
        match event.key:
            case pygame.K_LEFT:
                self.current_piece.x -= 1
                if not self.current_piece.valid_space(grid):
                    self.current_piece.x += 1

            case pygame.K_RIGHT:
                self.current_piece.x += 1
                if not self.current_piece.valid_space(grid):
                    self.current_piece.x -= 1

            case pygame.K_UP:
                self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
                if not self.current_piece.valid_space(grid):
                    self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)

            case pygame.K_DOWN:
                self.current_piece.y += 1
                if not self.current_piece.valid_space(grid):
                    self.current_piece.y -= 1

    def lock_piece_to_grid(self, shape_pos):
        grid = create_grid(self.locked_positions)

        for pos in shape_pos:
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color

        self.current_piece = self.next_piece
        self.next_piece = get_shape()

        rows_cleared = clear_rows(grid, self.locked_positions)
        if rows_cleared > 0:
            self.score += rows_cleared * Constants.SCORE_PER_ROW

    def run_game(self):
        self.init_game()

        self.window.fill(Constants.COLOR_BLACK)
        draw_text_middle('Press any key to start!', 40, Constants.COLOR_WHITE, self.window)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    waiting = False

        while self.run:
            grid = create_grid(self.locked_positions)
            self.update_game_timing()
            self.increase_game_difficulty()
            change_piece = self.move_piece_down()
            self.handle_player_input()

            shape_pos = draw_current_piece_on_grid(self.current_piece, grid)

            if change_piece:
                self.lock_piece_to_grid(shape_pos)

            draw_window(self.window, grid)
            draw_next_shape(self.next_piece, self.window)
            pygame.display.update()

            if check_lost(self.locked_positions):
                self.run = False

        draw_text_middle("You Lost", 40, Constants.COLOR_WHITE, self.window)
        pygame.display.update()
        pygame.time.delay(Constants.GAME_OVER_DELAY_MS)
