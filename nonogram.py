from enum import Enum

from exception import AlreadyMarkedError


class Mark(Enum):
    BLACK = 1
    WHITE = 0
    EMPTY = '-'


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
        self.__board = [[Mark.EMPTY for x in range(num_columns)] for x in range(num_rows)]

    def mark(self, row, column, mark_type):
        """
        :param row: 1,2,3,4,...,n
        :param column: 1,2,3,4,...,m
        """
        if row > self.num_rows or column > self.num_columns or row <= 0 or column <= 0:
            raise IndexError

        row -= 1
        column -= 1
        if self.__board[row][column] is Mark.EMPTY:
            self.__board[row][column] = mark_type
        elif self.__board[row][column] != mark_type:
            message = "The square in row {} and column {} is already marked with {}".format(row + 1, column + 1, self.__board[row][column])
            raise AlreadyMarkedError(message)

    def __str__(self):
        ret = ''
        for row in self.__board:
            for s in row:
                ret += str(s.value)
            ret += '\n'
        return ret

    def get_board(self):
        return self.__board
