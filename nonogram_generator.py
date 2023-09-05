import os

from PIL import Image
import numpy as np

from exception import CantSolveError
from nonogram import Mark, Nonogram
from nonogram_solver import NonogramSolver


class NonogramGenerator:
    def __init__(self, image_path, width, height, threshold=200):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.threshold = threshold
        self.image_array = []
        self.__load_image()

    def __load_image(self):
        image = Image.open(self.image_path)
        resized_image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        bw_image = resized_image.convert("L")

        bw_array = np.array(bw_image)
        self.image_array = np.where(bw_array >= self.threshold, Mark.WHITE, Mark.BLACK)

        image.close()
        resized_image.close()
        bw_image.close()

    def get_image_as_array(self):
        return self.image_array

    def get_rows_and_columns_nonogram_header(self):
        rows = [self.__find_lengths(row) for row in self.image_array]
        transposed_array = list(map(list, zip(*self.image_array)))
        columns = [self.__find_lengths(column) for column in transposed_array]
        return rows, columns

    def __find_lengths(self, arr):
        lengths = []
        count = 0
        for value in arr:
            if value == Mark.BLACK:
                count += 1
            elif count > 0:
                lengths.append(count)
                count = 0
        if count > 0:
            lengths.append(count)
        if len(lengths) == 0:
            lengths.append(0)
        return lengths

    def is_nonogram_solvable(self):
        nonogram = self.get_nonogram()
        solver = NonogramSolver(nonogram)
        try:
           solver.solve()
        except CantSolveError:
            return False
        return True

    def get_nonogram(self):
        rows, columns = self.get_rows_and_columns_nonogram_header()
        file_name_with_extension = os.path.basename(self.image_path)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        nonogram = Nonogram(rows, columns, file_name)
        return nonogram
