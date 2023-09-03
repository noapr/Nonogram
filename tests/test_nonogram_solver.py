import unittest

from database import DATABASE
from exception import AlreadyMarkedError, CantSolveError
from nonogram import Nonogram, Mark
from nonogram_solver import NonogramSolver


class TestNonogramSolver(unittest.TestCase):
    def __convert_to_hashable(self, inner_list):
        return tuple('B' if item is Mark.BLACK else 'W' for item in inner_list)

    def test_calculate_possibilities(self):
        new_puzzle = Nonogram([[3, 2, 6]], [[1]] * 15, 'test')
        solver = NonogramSolver(new_puzzle)
        output = solver.calculate_possibilities(new_puzzle.rows, new_puzzle.num_columns)
        expected = [[[Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6 + [Mark.WHITE] * 2,
                     [Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] * 2 + [Mark.BLACK] * 6 + [Mark.WHITE],
                     [Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] * 3 + [Mark.BLACK] * 6,
                     [Mark.BLACK] * 3 + [Mark.WHITE] * 2 + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6 + [Mark.WHITE],
                     [Mark.BLACK] * 3 + [Mark.WHITE] * 2 + [Mark.BLACK] * 2 + [Mark.WHITE] * 2 + [Mark.BLACK] * 6,
                     [Mark.BLACK] * 3 + [Mark.WHITE] * 3 + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6,
                     [Mark.WHITE] + [Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6 + [Mark.WHITE],
                     [Mark.WHITE] + [Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] * 2 + [Mark.BLACK] * 6,
                     [Mark.WHITE] + [Mark.BLACK] * 3 + [Mark.WHITE] * 2 + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6,
                     [Mark.WHITE] * 2 + [Mark.BLACK] * 3 + [Mark.WHITE] + [Mark.BLACK] * 2 + [Mark.WHITE] + [Mark.BLACK] * 6]]
        hashable_output = [self.__convert_to_hashable(inner) for inner in output]
        hashable_expected = [self.__convert_to_hashable(inner) for inner in expected]
        hashable_output.sort()
        hashable_expected.sort()
        self.assertListEqual(hashable_output, hashable_expected)

    def test_solve_cant_solve(self):
        new_puzzle = Nonogram([[1]], [[1]] * 15, 'test')
        solver = NonogramSolver(new_puzzle)
        with self.assertRaises(CantSolveError):
            solver.solve()

    def test_solve_can_solve(self):
        for i in range(len(DATABASE)):
            new_puzzle = Nonogram(
                rows=DATABASE[i].get('rows'),
                columns=DATABASE[i].get('columns'),
                name=DATABASE[i].get('name'))
            solver = NonogramSolver(new_puzzle)
            solver.solve()
            self.assertEqual(str(new_puzzle), DATABASE[i].get('solution'))
