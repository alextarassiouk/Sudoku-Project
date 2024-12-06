import pygame
import random

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

# Constants
WIDTH = 540
HEIGHT = 600  # Increased height to fit buttons
ROWS, COLS = 9, 9
CELL_SIZE = WIDTH // COLS
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_COLOR = (100, 150, 255)
BUTTON_HOVER_COLOR = (50, 100, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 40)
LARGE_FONT = pygame.font.SysFont("comicsans", 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action  # Action to perform on click

    def draw(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check if mouse is over button
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Draw the text
        text_surface = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def click(self):
        if self.is_hovered() and self.action:
            self.action()

# Sudoku Generator Class
class SudokuGenerator:
    def __init__(self, row_length=9, removed_cells=30):
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.fill_values()

    def get_board(self):
        return self.board

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for row in range(3):
            for col in range(3):
                if self.board[row_start + row][col_start + col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row - row % 3, col - col % 3, num)

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = numbers.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.fill_remaining():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        for _ in range(self.removed_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0


# Main Menu Function
def main_menu():
    run = True
    while run:
        screen.fill(BACKGROUND_COLOR)

        # Title Text
        title_text = LARGE_FONT.render("Sudoku Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Buttons for difficulty
        easy_button = Button("Easy", WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: game_loop(difficulty=30))
        medium_button = Button("Medium", WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: game_loop(difficulty=40))
        hard_button = Button("Hard", WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: game_loop(difficulty=50))

        easy_button.draw()
        medium_button.draw()
        hard_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                easy_button.click()
                medium_button.click()
                hard_button.click()

        pygame.display.update()


# Game Loop
def game_loop(difficulty):
    # Create Sudoku puzzle
    generator = SudokuGenerator(removed_cells=difficulty)
    board = generator.get_board()

    selected_cell = None
    sketch = None
    run = True

    # Buttons on the game screen
    reset_button = Button("Reset", 20, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: game_loop(difficulty))
    restart_button = Button("Restart", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: main_menu())
    exit_button = Button("Exit", WIDTH - BUTTON_WIDTH - 20, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: pygame.quit())

    while run:
        screen.fill(BACKGROUND_COLOR)
        draw_board(board, selected_cell)

        reset_button.draw()
        restart_button.draw()
        exit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = get_selected_cell(event.pos)
                reset_button.click()
                restart_button.click()
                exit_button.click()
            elif event.type == pygame.KEYDOWN:
                if selected_cell is not None:
                    row, col = selected_cell
                    if event.key == pygame.K_RETURN and sketch is not None:  # Submit number
                        if board[row][col] == 0:  # If not a pre-filled cell
                            board[row][col] = sketch
                            sketch = None  # Clear sketch
                    elif event.key == pygame.K_BACKSPACE:  # Clear the number
                        sketch = None
                    elif event.unicode.isdigit() and len(event.unicode) == 1:
                        sketch = int(event.unicode)  # Set sketch value

        pygame.display.update()


def draw_board(board, selected_cell):
    for row in range(9):
        for col in range(9):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 1)

            value = board[row][col]
            if value != 0:
                text = FONT.render(str(value), True, WHITE)
                screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 3))

            if selected_cell == (row, col):
                pygame.draw.rect(screen, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 3)


def get_selected_cell(mouse_pos):
    x, y = mouse_pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


# Run the main menu
if __name__ == "__main__":
    main_menu()
