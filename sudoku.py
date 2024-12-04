import pygame
import sys
from sudoku_generator import SudokuGenerator
import random

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 36)


def draw_text(screen, text, position, color=(0, 0, 0)):
    label = FONT.render(text, True, color)
    screen.blit(label, position)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku")

    running = True
    while running:
        screen.fill(BG_COLOR)

        draw_text(screen, "Sudoku Game", (SCREEN_WIDTH // 2 - 80, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()