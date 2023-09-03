import unittest

from exception import AlreadyMarkedError
from nonogram import Nonogram, Mark


class TestNonogram(unittest.TestCase):
    def test_create_illegal_nonogram(self):
        with self.assertRaises(IndexError):
            new_puzzle = Nonogram([], [1], 'test')
        with self.assertRaises(IndexError):
            new_puzzle = Nonogram([5, 5, 4], [], 'test')

    def test_mark_illegal_index(self):
        new_puzzle = Nonogram([1, 2, 3, 4], [1, 2, 3, 4], 'test')
        with self.assertRaises(IndexError):
            new_puzzle.mark(5, 4, Mark.BLACK)
        with self.assertRaises(IndexError):
            new_puzzle.mark(-4, 1, Mark.BLACK)
        with self.assertRaises(IndexError):
            new_puzzle.mark(2, -1, Mark.BLACK)

    def test_already_marked_error(self):
        new_puzzle = Nonogram([1, 2, 3, 4], [1, 2, 3, 4], 'test')
        new_puzzle.mark(3, 3, Mark.BLACK)
        with self.assertRaises(AlreadyMarkedError):
            new_puzzle.mark(3, 3, Mark.WHITE)

    def test_mark(self):
        new_puzzle = Nonogram([1, 2, 3, 4], [1, 2, 3, 4], 'test')
        new_puzzle.mark(3, 3, Mark.BLACK)
        self.assertEqual(str(new_puzzle), "----\n----\n--1-\n----\n")
