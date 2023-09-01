import unittest

from exception import AlreadyMarkedError, CantSolveError
from nonogram import Nonogram, Mark
from nonogram_solver import NonogramSolver


class TestNonogramSolver(unittest.TestCase):
    def __convert_to_hashable(self, inner_list):
        return tuple('B' if item is Mark.BLACK else 'W' for item in inner_list)

    def test_calculate_possibilities(self):
        new_puzzle = Nonogram([[3, 2, 6]], [[1]] * 15)
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
        new_puzzle = Nonogram([[1]], [[1]] * 15)
        solver = NonogramSolver(new_puzzle)
        with self.assertRaises(CantSolveError):
            solver.solve()

    def test_solve_can_solve(self):
        new_puzzle = Nonogram(
            rows=[[5], [6], [4, 1, 4], [3, 2, 6], [3, 1, 1, 2, 3], [2, 1, 1, 1, 3], [3, 2, 1, 2], [3, 1, 1, 2], [2, 3, 5], [7, 1, 3], [2, 2, 2, 2], [2, 2, 3], [3, 5, 2], [4, 1],
                  [14]],
            columns=[[9], [9, 5], [5, 2, 6], [3, 2, 3], [2, 1, 2, 2], [3, 1, 3, 1], [5, 3, 1], [1, 2, 1], [2, 2, 1, 1], [2, 2, 1, 1, 1], [2, 1, 2, 1, 1], [2, 1, 2, 1], [4, 4, 1],
                     [11, 1], [7, 3]])
        solver = NonogramSolver(new_puzzle)
        solver.solve()
        self.assertEqual(str(new_puzzle),
                         "111110000000000\n111111000000000\n111101000011110\n111001100111111\n111010101100111\n110000101010111\n111001100100011\n111000100100011\n110111000011111\n001111111010111\n011001101100110\n011000110001110\n011100011111011\n011110000000001\n011111111111111\n")
