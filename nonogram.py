from enum import Enum

from exception import AlreadyMarkedError


class Mark(Enum):
    BLACK = 1
    WHITE = 0


class Nonogram:
    def __init__(self, rows, columns):

        num_rows = len(rows)
        num_columns = len(columns)
        if num_rows <= 0 or num_columns <= 0:
            raise IndexError

        self.num_rows = num_rows
        self.num_columns = num_columns
        self.rows = rows
        self.columns = columns
        self.__board = [[Mark.WHITE for x in range(num_columns)] for x in range(num_rows)]

    def mark(self, row, column):
        if row > self.num_rows or column > self.num_columns or row <= 0 or column <= 0:
            raise IndexError

        row -= 1
        column -= 1
        if self.__board[row][column] is Mark.WHITE:
            self.__board[row][column] = Mark.BLACK
        else:
            raise AlreadyMarkedError(f"The square in row {row} and column {column} is already marked")

    def __str__(self):
        ret = ''
        for row in self.__board:
            for s in row:
                ret += str(s.value)
            ret += '\n'
        return ret
