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
                    for j in range(self.nonogram.num_columns):
                        self.nonogram.mark(i + 1, j + 1, self.__rows_possibilities[i][0][j])
            for i in range(self.nonogram.num_columns):
                if len(self.__cols_possibilities[i]) == 1:
                    for j in range(self.nonogram.num_rows):
                        self.nonogram.mark(j + 1, i + 1, self.__rows_possibilities[i][0][j])

            self.__remove_not_suitable_possibilities()
            if self.__is_running_out_of_possibilities():
                raise CantSolveError()

            self.__partial_marking()

            self.__remove_not_suitable_possibilities()
            if self.__is_running_out_of_possibilities():
                raise CantSolveError()

            self.__solved = self.__is_solved()

            print(self.nonogram)
            print('')

    def __remove_not_suitable_possibilities(self):
        for i in range(self.nonogram.num_rows):
            for j in range(self.nonogram.num_columns):
                self.__rows_possibilities[i] = [perm for perm in self.__rows_possibilities[i] if perm[j] == self.nonogram.get_board()[i][j]]
                self.__cols_possibilities[j] = [perm for perm in self.__cols_possibilities[j] if perm[i] == self.nonogram.get_board()[i][j]]

    def __partial_marking(self):
        for i in range(self.nonogram.num_rows):
            common_marks = self.__rows_possibilities[i][0]
            for perm in self.__rows_possibilities[i][1:]:
                for j in range(self.nonogram.num_columns):
                    if common_marks[j] != perm[j]:
                        common_marks[j] = Mark.EMPTY
            for j in range(self.nonogram.num_columns):
                if common_marks[j] != Mark.EMPTY:
                    self.nonogram.mark(i + 1, j + 1, common_marks[j])

        for i in range(self.nonogram.num_columns):
            common_marks = self.__cols_possibilities[i][0]
            for perm in self.__cols_possibilities[i][1:]:
                for j in range(self.nonogram.num_rows):
                    if common_marks[j] != perm[j]:
                        common_marks[j] = Mark.EMPTY
            for j in range(self.nonogram.num_rows):
                if common_marks[j] != Mark.EMPTY:
                    self.nonogram.mark(j + 1, i + 1, common_marks[j])

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
            inner_possibilities = []
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


if __name__ == '__main__':
    new_puzzle = Nonogram(
        rows=[[5], [6], [4, 1, 4], [3, 2, 6], [3, 1, 1, 2, 3], [2, 1, 1, 1, 3], [3, 2, 1, 2], [3, 1, 1, 2], [2, 3, 5], [7, 1, 3], [2, 2, 2, 2], [2, 2, 3], [3, 5, 2], [4, 1],
              [14]],
        columns=[[9], [9, 5], [5, 2, 6], [3, 2, 3], [2, 1, 2, 2], [3, 1, 3, 1], [5, 3, 1], [1, 2, 1], [2, 2, 1, 1], [2, 2, 1, 1, 1], [2, 1, 2, 1, 1], [2, 1, 2, 1], [4, 4, 1],
                 [11, 1], [7, 3]])
    solver = NonogramSolver(new_puzzle)
    solver.solve()
    print(solver.nonogram)
