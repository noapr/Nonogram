import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt

from nonogram_solver import NonogramSolver
from nonogram import Mark

CELL_SIZE = 25
MARK_TO_COLOR = {Mark.EMPTY: '#d3d3d3', Mark.BLACK: '#000000', Mark.WHITE: '#ffffff'}


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

        # Create and add row number labels
        max_length = (len(max(self.nonogram.rows, key=lambda x: len(x))))
        for i in range(self.nonogram.num_rows):
            row_label = QLabel((str(self.nonogram.rows[i])[1:-1]).replace(',', ''))
            row_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row_label.setStyleSheet("background-color: white;")
            row_label.setFixedSize(15 * max_length, CELL_SIZE)
            game_board_layout.addWidget(row_label, i + 1, 0)

        # Create and add columns number labels
        for i in range(self.nonogram.num_columns):
            column_label = QLabel((str(self.nonogram.columns[i])[1:-1]).replace(', ', '\n'))
            column_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
            column_label.setStyleSheet("background-color: white;")
            column_label.setFixedSize(CELL_SIZE, 15 * max_length)
            game_board_layout.addWidget(column_label, 0, i + 1)

        # Create and add cells to the game board grid layout
        self.cells = []
        for row in range(self.nonogram.num_rows):
            row_cells = []
            for col in range(self.nonogram.num_columns):
                cell = QPushButton('')
                cell.setFixedSize(CELL_SIZE, CELL_SIZE)
                cell.clicked.connect(lambda _, r=row, c=col: self.toggle_cell(r, c))
                cell.setContentsMargins(0, 0, 0, 0)
                cell.setStyleSheet("background-color: {};".format(MARK_TO_COLOR[Mark.EMPTY]))
                game_board_layout.addWidget(cell, row + 1, col + 1)
                row_cells.append(cell)
            self.cells.append(row_cells)
        self.game_board.setContentsMargins(0, 0, 0, 0)

        # Create buttons for controls
        control_layout = QHBoxLayout()
        solve_button = QPushButton('Solve')
        clear_button = QPushButton('Clear')
        check_button = QPushButton('Check')
        solve_button.clicked.connect(self.solve_nonogram)
        clear_button.clicked.connect(self.clear_board)
        check_button.clicked.connect(self.check_board)
        control_layout.addWidget(solve_button)
        control_layout.addWidget(clear_button)
        control_layout.addWidget(check_button)

        # Create a label for puzzle's name
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
        current_color = (self.cells[row][col].palette().color(self.cells[row][col].backgroundRole())).name()
        new_color = MARK_TO_COLOR[Mark.BLACK] if current_color in [MARK_TO_COLOR[Mark.EMPTY], MARK_TO_COLOR[Mark.WHITE]] else MARK_TO_COLOR[Mark.WHITE]
        self.cells[row][col].setStyleSheet("background-color: {new_color};".format(new_color=new_color))
        self.feedback_label.setText('')

    def solve_nonogram(self): # TODO: run background
        if self.nonogram is not None:
            if self.nonogram_solver.is_solved() is False:
                self.nonogram_solver.solve()
            self.display_solution()
            self.feedback_label.setText('')

    def check_board(self):
        flag = True
        if self.nonogram is not None:
            if self.nonogram_solver.is_solved() is False:
                self.nonogram_solver.solve()
            for row in range(self.nonogram.num_rows):
                for col in range(self.nonogram.num_columns):
                    mark = self.nonogram.get_board()[row][col]
                    if (self.cells[row][col].palette().color(self.cells[row][col].backgroundRole())).name() != MARK_TO_COLOR[mark]:
                        flag = False
            if flag:
                self.feedback_label.setText('Puzzle solved successfully!')
            else:
                self.feedback_label.setText('The board does not match the solution :(')

    def clear_board(self):
        for row in range(self.nonogram.num_rows):
            for col in range(self.nonogram.num_columns):
                self.cells[row][col].setStyleSheet("background-color: {};".format(MARK_TO_COLOR[Mark.EMPTY]))
        self.feedback_label.clear()

    def display_solution(self):
        for row in range(self.nonogram.num_rows):
            for col in range(self.nonogram.num_columns):
                mark = self.nonogram.get_board()[row][col]
                self.cells[row][col].setStyleSheet("background-color: {};".format(MARK_TO_COLOR[mark]))

    def fireworks_animation(self):
        self.fireworks_widget = FireworksWidget(self)
        self.setCentralWidget(self.fireworks_widget)
        self.fireworks_widget.start_animation()


def main():
    app = QApplication(sys.argv)
    selected_nonogram = None  # Initialize with the selected nonogram

    # Create the game window with the selected nonogram
    game = NonogramGame(selected_nonogram)
    game.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
