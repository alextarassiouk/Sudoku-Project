import pygame
import random

# Cell Class
class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 40)

        # Draw sketched value (top left corner)
        if self.sketched_value != 0 and self.value == 0:
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            screen.blit(text, (self.col * self.width + 5, self.row * self.height + 5))

        # Draw permanent value (centered)
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(
                text,
                (
                    self.col * self.width + self.width // 2 - text.get_width() // 2,
                    self.row * self.height + self.height // 2 - text.get_height() // 2,
                ),
            )

        # Highlight the selected cell
        if self.selected:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.col * self.width, self.row * self.height, self.width, self.height),
                3,
            )


# Sudoku Generator Class
class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.board = [[0] * row_length for _ in range(row_length)]
        self.removed_cells = removed_cells

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row - row % 3, col - col % 3, num)

    def fill_box(self, row_start, col_start):
        num_list = random.sample(range(1, 10), 9)
        idx = 0
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                self.board[row][col] = num_list[idx]
                idx += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.fill_remaining():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def remove_cells(self):
        count = self.removed_cells
        while count != 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

    def generate_sudoku(self):
        self.fill_diagonal()
        self.fill_remaining()
        self.remove_cells()


# Board Class
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.rows = 9
        self.cols = 9
        self.screen = screen
        self.difficulty = difficulty
        self.board_generator = SudokuGenerator(9, difficulty)
        self.board_generator.generate_sudoku()
        self.board = self.board_generator.get_board()
        self.selected_cell = None
        self.cells = [
            [Cell(self.board[row][col], row, col, width // self.cols, height // self.rows) for col in range(self.cols)]
            for row in range(self.rows)
        ]
        self.original = [[self.board[row][col] for col in range(self.cols)] for row in range(self.rows)]

    def draw(self):
        # Draw grid lines
        for i in range(self.rows + 1):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height // self.rows), (self.width, i * self.height // self.rows), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width // self.cols, 0), (i * self.width // self.cols, self.height), line_width)

        # Draw cells
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if x < self.width and y < self.height:
            row = y // (self.height // self.rows)
            col = x // (self.width // self.cols)
            return row, col
        return None, None

    def sketch(self, value):
        if self.selected_cell and self.original[self.selected_cell.row][self.selected_cell.col] == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.original[self.selected_cell.row][self.selected_cell.col] == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.set_sketched_value(0)
            self.update_board()

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                num = self.cells[row][col].value
                if num == 0 or not self.is_valid(row, col, num):
                    return False
        return True

    def is_valid(self, row, col, num):
        for i in range(self.cols):
            if i != col and self.cells[row][i].value == num:
                return False
        for i in range(self.rows):
            if i != row and self.cells[i][col].value == num:
                return False
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                if (i != row or j != col) and self.cells[i][j].value == num:
                    return False
        return True

    def update_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = self.cells[row][col].value

    def reset_to_original(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].set_cell_value(self.original[row][col])


# Main function to run the game
def main():
    pygame.init()
    width = 540
    height = 540
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku Game")

    clock = pygame.time.Clock()
    difficulty = 30  # Default to easy difficulty
    board = Board(width, height, screen, difficulty)

    running = True
    while running:
        screen.fill((255, 255, 255))

        # Draw the board
        board.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = board.click(x, y)
                if row is not None and col is not None:
                    board.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    board.sketch(1)
                elif event.key == pygame.K_2:
                    board.sketch(2)
                elif event.key == pygame.K_3:
                    board.sketch(3)
                elif event.key == pygame.K_4:
                    board.sketch(4)
                elif event.key == pygame.K_5:
                    board.sketch(5)
                elif event.key == pygame.K_6:
                    board.sketch(6)
                elif event.key == pygame.K_7:
                    board.sketch(7)
                elif event.key == pygame.K_8:
                    board.sketch(8)
                elif event.key == pygame.K_9:
                    board.sketch(9)

                if event.key == pygame.K_RETURN:
                    if board.selected_cell:
                        board.place_number(board.selected_cell.sketched_value)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()