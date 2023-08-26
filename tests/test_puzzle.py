import unittest

from exception import AlreadyMarkedError
from puzzle import Puzzle, Mark


class TestPuzzle(unittest.TestCase):
    def test_create_illegal_puzzle(self):
        with self.assertRaises(IndexError):
            new_puzzle = Puzzle([], [1])
        with self.assertRaises(IndexError):
            new_puzzle = Puzzle([5, 5, 4], [])

    def test_mark_illegal_index(self):
        new_puzzle = Puzzle([1, 2, 3, 4], [1, 2, 3, 4])
        with self.assertRaises(IndexError):
            new_puzzle.mark(5, 4)
        with self.assertRaises(IndexError):
            new_puzzle.mark(-4, 1)
        with self.assertRaises(IndexError):
            new_puzzle.mark(2, -1)

    def test_already_marked_error(self):
        new_puzzle = Puzzle([1, 2, 3, 4], [1, 2, 3, 4])
        new_puzzle.mark(3, 3)
        with self.assertRaises(AlreadyMarkedError):
            new_puzzle.mark(3, 3)
