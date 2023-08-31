from sympy.utilities.iterables import multiset_permutations
from exception import CantSolveError, AlreadyMarkedError
from nonogram import Mark, Nonogram



class NonogramSolver:
    def __init__(self, nonogram):
        self.nonogram = nonogram
        self.__solved = False

        self.__rows_possibilities = []
        self.__cols_possibilities = []

    def solve(self):
        self.__rows_possibilities = self.calculate_possibilities(self.nonogram.rows, self.nonogram.num_columns)
        self.__cols_possibilities = self.calculate_possibilities(self.nonogram.columns, self.nonogram.num_rows)

        while not self.__solved:
            for i in range(self.nonogram.num_rows):
                if len(self.__rows_possibilities[i]) == 1:
                    self.__iteration(i, 0)
            for i in range(self.nonogram.num_columns):
                if len(self.__cols_possibilities[i]) == 1:
                    self.__iteration(i, 1)
            self.__solved = self.__is_solved()
            if self.__is_running_out_of_possibilities():
                raise CantSolveError()

    def __iteration(self, ext_iter, type):
        """
        :param ext_iter: external iteration number
        :param type: 0 for row 1 for column
        """
        nonogram_size = [self.nonogram.num_columns, self.nonogram.num_rows]
        possibilities = [self.__rows_possibilities, self.__cols_possibilities]
        for j in range(nonogram_size[type]):
            if (possibilities[type])[ext_iter][0][j] == Mark.BLACK:
                try:
                    if type == 0:
                        self.nonogram.mark(ext_iter + 1, j + 1)
                    if type == 1:
                        self.nonogram.mark(j + 1, ext_iter + 1)
                except AlreadyMarkedError:
                    continue
            for perm in (possibilities[abs(type - 1)])[j]:
                if perm[ext_iter] != (possibilities[type])[ext_iter][0][j]:
                    (possibilities[abs(type - 1)])[j].remove(perm)

    def __is_solved(self):
        for i in range(self.nonogram.num_rows):
            if len(self.__rows_possibilities[i]) != 1:
                return False
        for i in range(self.nonogram.num_columns):
            if len(self.__cols_possibilities[i]) != 1:
                return False
        return True

    def __is_running_out_of_possibilities(self):
        for i in range(self.nonogram.num_rows):
            if len(self.__rows_possibilities[i]) == 0:
                return True
        for i in range(self.nonogram.num_columns):
            if len(self.__cols_possibilities[i]) == 0:
                return True
        return False

    def calculate_possibilities(self, values, num):
        possibilities = []

        for v in values:
            inner_possibilities=[]
            num_empty = num - sum(v)
            marks = [[Mark.BLACK] * x for x in v]
            unmarks = [[Mark.WHITE]] * num_empty
            perms = multiset_permutations(marks + unmarks)
            for p in list(perms):
                if self.__is_permutation_legal(p, v):
                    flattened_list = [item for sublist in p for item in sublist]
                    if flattened_list not in inner_possibilities:
                        inner_possibilities.append(flattened_list)
            possibilities.append(inner_possibilities)
        return possibilities

    def __is_permutation_legal(self, permutation, values):
            flag = False
            indx = 0
            for x in permutation:
                if x[0].value == Mark.WHITE.value:
                    if flag:
                        flag = False
                if x[0].value == Mark.BLACK.value:
                    if len(x) != values[indx]:
                        return False
                    indx += 1
                    if flag:
                        return False
                    flag = True
            return True