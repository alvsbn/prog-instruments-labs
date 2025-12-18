import pygame
from ui import  draw_text_middle
from constants import Constants

from game_logic import main


pygame.font.init()


def main_menu():
    run = True
    win = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        win.fill(Constants.COLOR_BLACK)
        draw_text_middle('Press any key to begin.', 60, Constants.COLOR_WHITE, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

if __name__ == "__main__":
    main_menu()
