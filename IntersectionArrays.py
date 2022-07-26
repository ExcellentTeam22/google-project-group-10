from functools import reduce

import numpy as np


class IntersectionArray:
    """
    Intersection betweens arrays
    """

    def intersect(self, arrays):
        """
        :param arrays: Arrays of word appearance
        :return: intersection of words arrays that appear in same line and file
        """
        nrows, ncols = arrays[0].shape
        dtype = {'names': ['f{}'.format(i) for i in range(ncols)],
                 'formats': ncols * [arrays[0].dtype]}
        arrays_to_check = (arr.view(dtype) for arr in arrays)
        intersected = reduce(np.intersect1d, arrays_to_check)
        return intersected


# Test

A = np.array([[1, 4], [1, 4], [2, 5], [3, 6], [5, 3]])
B = np.array([[1, 4], [3, 6], [7, 8]])
C = np.array([[2, 3], [40, 3], [1, 4], [3, 6]])

V = (A, B, C)
inter = IntersectionArray()
print(inter.intersect(V))
