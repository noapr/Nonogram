import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt
from nonogram_solver import NonogramSolver
from nonogram import Nonogram, Mark

CELL_SIZE = 25


class NonogramGame(QMainWindow):
    def __init__(self, nonogram):
        super().__init__()

        self.nonogram = nonogram
        self.nonogram_solver = NonogramSolver(nonogram)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Nonogram Game')
        self.setGeometry(700, 300, CELL_SIZE * (self.nonogram.num_columns + 1), CELL_SIZE * (self.nonogram.num_rows + 1))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        game_board_layout = QGridLayout()
        game_board_layout.setSpacing(0)
        game_board_layout.setContentsMargins(0, 0, 0, 0)
        self.game_board = QWidget()
        self.game_board.setLayout(game_board_layout)

        # Create and add cells to the game board grid layout
        self.cells = []
        for row in range(self.nonogram.num_rows):
            row_cells = []
            for col in range(self.nonogram.num_columns):
                cell = QPushButton('')
                cell.setFixedSize(CELL_SIZE, CELL_SIZE)
                cell.clicked.connect(lambda _, r=row, c=col: self.toggle_cell(r, c))
                cell.setContentsMargins(0, 0, 0, 0)
                game_board_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        self.game_board.setContentsMargins(0, 0, 0, 0)

        # Create buttons for controls
        control_layout = QHBoxLayout()
        solve_button = QPushButton('Solve')
        clear_button = QPushButton('Clear')
        solve_button.clicked.connect(self.solve_nonogram)
        clear_button.clicked.connect(self.clear_board)
        control_layout.addWidget(solve_button)
        control_layout.addWidget(clear_button)

        # Create an input field for puzzle definition
        self.puzzle_name = QLabel(self.nonogram.name)
        self.puzzle_name.setAlignment(Qt.AlignCenter)
        self.puzzle_name.setStyleSheet("font-size: 28px; color: blue;")

        # Create a label for feedback
        self.feedback_label = QLabel('')

        # Add widgets to the main layout
        layout.addWidget(self.puzzle_name)
        layout.addWidget(self.feedback_label)
        layout.addWidget(self.game_board)
        layout.addLayout(control_layout)

        central_widget.setLayout(layout)

    def toggle_cell(self, row, col):
        current_text = self.cells[row][col].text()
        new_text = 'X' if current_text == '' else ''
        self.cells[row][col].setText(new_text)

    def solve_nonogram(self):
        if self.nonogram is not None:
            self.nonogram_solver.solve()
            if self.nonogram_solver.is_solved() is not False:
                self.display_solution()
                self.feedback_label.setText('Puzzle solved successfully!')
            else:
                self.feedback_label.setText('Unable to solve the puzzle.')
        else:
            self.feedback_label.setText('No nonogram selected.')

    def clear_board(self):
        self.puzzle_name.clear()
        for row in self.cells:
            for cell in row:
                cell.setText('')
        self.feedback_label.clear()

    def display_solution(self):
        for row in range(self.nonogram.num_rows):
            for col in range(self.nonogram.num_columns):
                if self.nonogram.get_board()[row][col] == Mark.BLACK:
                    self.cells[row][col].setText('X')
                elif self.nonogram.get_board()[row][col] == Mark.WHITE:
                    self.cells[row][col].setText('')

    @staticmethod
    def create_nonogram(puzzle_definition):
        # Implement a method to create a Nonogram from the puzzle_definition string
        # You can use your nonogram class here
        pass


def main():
    app = QApplication(sys.argv)
    selected_nonogram = None  # Initialize with the selected nonogram

    # Create the game window with the selected nonogram
    game = NonogramGame(selected_nonogram)
    game.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
