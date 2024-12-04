import pygame
from sudoku_generator import *

class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp_value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set_value(self, value):
        self.value = value

    def set_temp_value(self, value):
        self.temp_value = value

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp_value != 0 and self.value == 0:
            text = font.render(str(self.temp_value), True, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 3)

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.board = generate_sudoku(9, difficulty)
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
        self.selected = None

    def draw(self, screen):
        gap = self.width / 9
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thickness)

        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def select(self, row, col):
        for row in self.cells:
            for cell in row:
                cell.selected = False
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def place_number(self, value):
        if self.selected:
            row, col = self.selected
            if self.cells[row][col].value == 0:
                self.cells[row][col].set_value(value)
                self.update_board()

    def update_board(self):
        self.board = [[self.cells[i][j].value for j in range(9)] for i in range(9)]

    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

def main():
    pygame.init()
    width, height = 540, 540
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku")
    board = Board(width, height, screen, 45)
    run = True

    while run:
        screen.fill((255, 255, 255))
        board.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
            if event.type == pygame.KEYDOWN:
                if board.selected:
                    if event.key == pygame.K_1:
                        board.place_number(1)
                    # Add similar code for keys 2 through 9

    pygame.quit()

if __name__ == "__main__":
    main()