class SudokuGenerator:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.box_length = int(height ** 0.5)  # Assuming a square grid (e.g., 9x9 grid => box_length is 3)
        self.fill_values()

    def is_safe(self, row, col, num):
        # Check the row for duplicates
        if num in self.board[row]:
            return False

        # Check the column for duplicates
        for r in range(len(self.board)):
            if self.board[r][col] == num:
                return False

        # Check the 3x3 box for duplicates
        start_row = (row // self.box_length) * self.box_length
        start_col = (col // self.box_length) * self.box_length

        for r in range(start_row, start_row + self.box_length):
            for c in range(start_col, start_col + self.box_length):
                if self.board[r][c] == num:
                    return False

        return True

    def fill_values(self):
        # This function starts the process of filling the board
        self.fill_remaining(0, 0)

    def fill_remaining(self, row, col):
        # This method recursively tries to fill the board
        if row >= len(self.board):  # If row goes beyond the grid, we have completed the board
            return True
        if col >= len(self.board[row]):  # If column goes beyond the row length, move to the next row
            return self.fill_remaining(row + 1, 0)
        if self.board[row][col] != 0:  # Skip already filled cells
            return self.fill_remaining(row, col + 1)

        # Try numbers 1 to 9
        for num in range(1, 10):
            if self.is_safe(row, col, num):  # Check if placing num is safe
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):  # Move to the next cell
                    return True
                self.board[row][col] = 0  # Backtrack if placing num didn't work

        return False

def generate_sudoku(width, height, difficulty):
    generator = SudokuGenerator(width, height, difficulty)
    return generator.board
