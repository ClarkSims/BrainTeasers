#!/usr/bin/env python3
""" This is the question: given a rectangle of 1's and 0's find the longest run of 1's
    within a row, diagonal or column, and return a list of the form:
    [length_of_longest_run, coordinates_of_begin_of_run, coordinates_of_end_of_run]
    I solved the problem as follows:
     1) I coded up Kadan's algorithm to find the longest run in a list.
     2) I then coded up a function, find_longest_list, to loop through a list of list and
    and return the longest list.
     3) I then coded up 4 transformations to calculate the longest row, column and deagonals
        in either direction
     4) the final function find longest run, calls the previous 4 functions, and returns
        the longest run.
"""
import unittest
import pdb
from copy import deepcopy

class Line:
    """
        Class to save longest run in set of runs within a matrix. This is a 
        Euclidean line on a grid, ie. two points and all points between.
     """
    def __init__(
            self,
            length=0,
            small_stride_begin=None,
            big_stride_begin=None,
            small_stride_back=None,
            big_stride_back=None):
        self.length = length
        self.small_stride_begin = small_stride_begin
        self.big_stride_begin = big_stride_begin
        self.small_stride_back = small_stride_back
        self.big_stride_back = big_stride_back


    def __repr__(self):
        return "length={}, small_stride_begin={}, big_stride_begin={}, i_back={},"\
        "big_stride_back={}".format(\
            self.length,\
            self.small_stride_begin, self.big_stride_begin,\
            self.small_stride_back, self.big_stride_back)


    def __eq__(self, rhs):
        return self.length == rhs.length and\
            self.small_stride_begin == rhs.small_stride_begin and\
            self.big_stride_begin == rhs.big_stride_begin and\
            self.small_stride_back == rhs.small_stride_back and\
            self.big_stride_back == rhs.big_stride_back


    def __ne__(self, rhs):
        return not self.__eq__(rhs)


    def set_null(self):
        """ uninitialize all values """
        self.__init__(0, None, None, None, None)


class VectorWithinMatrix:
    """
        Class to represent a linear path within a matrix. It starts at
        (small_stride_begin, big_stride_begin), it has slope
        d_big_stride/d_small_stride, has a length of num_steps, and ends at
        (i, j). in_bounds represents weather the end is within the matrix or
        not. This is a classical vector, put into a grid, ie a starting point,
        a direction and a magnitude.
    """
    def __init__(self, matrix, small_stride_begin, big_stride_begin,
                 d_small_stride, d_big_stride):
        self._matrix = matrix
        self.small_stride_max = len(matrix[0])
        self.big_stride_max = len(matrix)
        self.small_stride_begin = small_stride_begin
        self.big_stride_begin = big_stride_begin
        self.d_small_stride = d_small_stride
        self.d_big_stride = d_big_stride
        self.num_steps = 0
        self.small_stride = small_stride_begin
        self.big_stride = big_stride_begin
        self.in_bounds = self.small_stride < self.small_stride_max and\
            self.big_stride < self.big_stride_max and self.small_stride >= 0\
            and self.big_stride >= 0


    def __repr__(self):
        return "small_stride_begin={} big_stride_begin={} d_small_stride={} "\
            "d_big_stride={} num_steps={} small_stride={} big_stride={}".format(
                self.small_stride_begin,
                self.big_stride_begin,
                self.d_small_stride,
                self.d_big_stride,
                self.num_steps,
                self.small_stride,
                self.big_stride)


    def step(self, num_steps):
        """
            calculate end of line after num_steps, and whether it is still
            in bounds
        """
        self.num_steps = num_steps
        self.small_stride = self.small_stride_begin + num_steps*self.d_small_stride
        self.big_stride = self.big_stride_begin + num_steps*self.d_big_stride
        self.in_bounds = self.small_stride < self.small_stride_max and\
            self.big_stride < self.big_stride_max and self.small_stride >= 0\
            and self.big_stride >= 0


    def kadane(self):
        """
            Implements Kadan's algorithm to find the longest run starting at
            (small_stride_begin, big_stride_begin) which has the slope
            d_big_stride/d_small_stride
        """
        if not self.in_bounds:
            raise ValueError("starting point of kadane out of bounds")
        if self._matrix[self.big_stride][self.small_stride] == 0:
            test = Line(0, None, None, None, None)
        else:
            test = Line(1, self.small_stride, self.big_stride,
                              self.small_stride, self.big_stride)
        longest = deepcopy(test)
        n_step = 0
        self.step(n_step)
#        track = 0
        while True:
            n_step = n_step + 1
            self.step(n_step)
            if not self.in_bounds:
                break
#            track = track + 1
#            print("\ntrack={}\n".format(track))
#            if track == 1:
#                print("here is trouble")
#                pdb.set_trace()
            atest = self._matrix[self.big_stride][self.small_stride]
            if atest != 0:
                if test.small_stride_begin is None:
                    test.length = 1
                    test.small_stride_begin = test.small_stride_back = self.small_stride
                    test.big_stride_begin = test.big_stride_back = self.big_stride
                else:
                    test.length = test.length+1
                    test.small_stride_back = self.small_stride
                    test.big_stride_back = self.big_stride
                if test.length > longest.length:
                    longest = deepcopy(test)
            else:
                test.set_null()
        return longest


class NbyMLongestPathSolver:
    """ class for finding the longest run of 1's within a matrix """
    def __init__(self, matrix=None):
        if matrix is not None:
            self._num_columns = len(matrix) #number of columns
            if self._num_columns > 0:
                self._num_rows = len(matrix[0])
            else:
                self._num_rows = 0
            self._matrix = matrix


    def solve_longest_row(self):
        """ loop through rows, find row with longest run """
        longest = Line()
        for row_offset in range(self._num_rows):
            line = VectorWithinMatrix(self._matrix, row_offset, 0, 0, 1)
#            pdb.set_trace()
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        return longest


    def solve_longest_column(self):
        """ loop through column, find column with longest run """
        longest = Line()
        for col_offset in range(self._num_columns):
            line = VectorWithinMatrix(self._matrix, 0, col_offset, 1, 0)
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        return longest


    def solve_longest_diagonal_positive_slope(self):
        """ loop through diagonals with posive slope, find the longest run """
        longest = Line()
        for row_offset in range(self._num_rows):
            line = VectorWithinMatrix(self._matrix, row_offset, 0, 1, 1)
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        for col_offset in range(1, self._num_columns):
            line = VectorWithinMatrix(self._matrix, 0, col_offset, 1, 1)
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        return longest


    def solve_longest_diagonal_negative_slope(self):
        """ loop through diagonals with negative slope, find the longest run """
        longest = Line()
        for col_offset in range(self._num_columns):
            line = VectorWithinMatrix(self._matrix, 0, col_offset, 1, -1)
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        for row_offset in range(1, self._num_rows):
            line = VectorWithinMatrix(self._matrix, row_offset, self._num_columns-1, 1, -1)
            test = line.kadane()
            if test.length > longest.length:
                longest = test
        return longest


    def solve_longest_run(self):
        """ loop through all linear subsets, find longest run """
        longest = self.solve_longest_row()
        test = self.solve_longest_column()
        if test.length > longest.length:
            longest = test
        test = self.solve_longest_diagonal_positive_slope()
        if test.length > longest.length:
            longest = test
        test = self.solve_longest_diagonal_negative_slope()
        if test.length > longest.length:
            longest = test
        return longest


class TestLine(unittest.TestCase):
    ''' simple test for Line'''
    def test_empty(self):
        """ test that default constructor works, and set_null works,
            test __eq__ and __ne__ also """
        empty1 = Line()
        empty2 = Line(1, 1, 1, 1, 1)
        empty2.set_null()
        self.assertEqual(empty1, empty2)
        self.assertFalse(empty1 != empty2)


def transpose(mtrx):
    ''' used to calculate transpose of matrices, which are used for testing, this is not used
        for the calculation of longest runs '''
    return [[col[i] for col in mtrx] for i in range(len(mtrx[0]))]


class TestVectorWithinMatrix(unittest.TestCase):
    ''' test of kadane's algorithm in class VectorWithinMatrix '''

    def test_one(self):
        """ test that constructor and kadane work for 1 element array """
        mtrx = [[1]]
        line = VectorWithinMatrix(mtrx, 0, 0, 1, 0)
        maxlen = line.kadane()
        correctlen = Line(1, 0, 0, 0, 0)
        self.assertEqual(maxlen, correctlen)


    def test_one_column(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            mtrx = [col]
            line = VectorWithinMatrix(mtrx, 0, 0, d_small_stride=1, d_big_stride=0)
            self.assertEqual(line.small_stride_max, col_len)
            max_len = line.kadane()
            correctlen = Line(col_len, 0, 0, col_len-1, 0)
            self.assertEqual(correctlen, max_len)


    def test_one_column_with_trailing_0(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            col.append(0)
            mtrx = [col]
            line = VectorWithinMatrix(mtrx, 0, 0, d_small_stride=1, d_big_stride=0)
            self.assertEqual(line.small_stride_max, col_len+1)
            max_len = line.kadane()
            correctlen = Line(col_len, 0, 0, col_len-1, 0)
            self.assertEqual(correctlen, max_len)


    def test_one_column_with_leading_0(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            col = [0] + col
            mtrx = [col]
#            line = VectorWithinMatrix(mtrx, 0, 1, 0, 1)
            line = VectorWithinMatrix(mtrx, 1, 0, d_small_stride=1, d_big_stride=0)
            self.assertEqual(line.small_stride_max, col_len+1)
            max_len = line.kadane()
            correct = Line(col_len, 1, 0, col_len, 0)
#            print("*******************")
#            print("\ncorrect = ", correct)
#            print("max_len = {}\n".format(max_len))
#            print("*******************")
            self.assertEqual(correct, max_len)


    def test_one_row(self):
        """ runs kadane on a single row """
        for row_len in range(2, 10):
            col = [1 for offset in range(row_len)]
            mtrx = transpose([col])
            line = VectorWithinMatrix(mtrx, 0, 0, 0, 1)
            self.assertEqual(line.big_stride_max, row_len)
            max_len = line.kadane()
            correct = Line(row_len, 0, 0, 0, row_len-1)
#            print("*******************")
#            print("\ncorrect = {}".format(correct))
#            print("max_len = {}\n".format(max_len))
#            print("*******************")
            self.assertEqual(correct, max_len)


    def test_one_row_trailing_0(self):
        """ runs kadane on a single column """
        for row_len in range(2, 10):
            col = [1 for offset in range(row_len)]
            col.append(0)
            mtrx = transpose([col])
            line = VectorWithinMatrix(mtrx, 0, 0, 0, 1)
            self.assertEqual(line.big_stride_max, row_len+1)
            max_len = line.kadane()
            correctlen = Line(row_len, 0, 0, 0, row_len-1)
            self.assertEqual(correctlen, max_len)


    def test_one_row_leading_0(self):
        """ runs kadane on a single column """
        for row_len in range(2, 10):
            col = [1 for offset in range(row_len)]
            col = [0] + col
            mtrx = transpose([col])
            line = VectorWithinMatrix(mtrx, 0, 1, 0, 1)
            self.assertEqual(line.big_stride_max, row_len+1)
            self.assertEqual(line.small_stride_max, 1)
            max_len = line.kadane()
            correctlen = Line(row_len, 0, 1, 0, row_len)
            self.assertEqual(correctlen, max_len)


    def test_central_diagonal(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            mtrx = [col for offset in range(col_len)] #square matrix all 1's
            line = VectorWithinMatrix(mtrx, 0, 0, d_small_stride=1, d_big_stride=1)
            self.assertEqual(line.small_stride_max, col_len)
            max_len = line.kadane()
            correctlen = Line(col_len, 0, 0, col_len-1, col_len-1)
            self.assertEqual(correctlen, max_len)


    def test_off_diagonals(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            mtrx = [col for offset in range(col_len)] #square matrix all 1's
            for offset in range(1, col_len):
                line = VectorWithinMatrix(mtrx, 0, offset, d_small_stride=1,
                            d_big_stride=1)
                max_len = line.kadane()
                correctlen = Line(col_len-offset, 0, offset,
                                        col_len-1-offset, col_len-1)
                self.assertEqual(correctlen, max_len)
                line = VectorWithinMatrix(mtrx, offset, 0, d_small_stride=1,
                            d_big_stride=1)
                max_len = line.kadane()
                correctlen = Line(col_len-offset, offset, 0,
                                        col_len-1, col_len-1-offset)
                self.assertEqual(correctlen, max_len)


class TestNbyMLongestPathSolver(unittest.TestCase):
    """ Test longest path within test matrices """
    def test_one(self):
        """ test that constructor and kadane work for 1 element array """
        mtrx = [[1]]
        longest_solver = NbyMLongestPathSolver(mtrx)
        maxlen = longest_solver.solve_longest_run()
        correctlen = Line(1, 0, 0, 0, 0)
        self.assertEqual(maxlen, correctlen)


    def test_one_column(self):
        """ runs kadane on a single column """
        for col_len in range(2, 10):
            col = [1 for offset in range(col_len)]
            mtrx = [col]
            longest_solver = NbyMLongestPathSolver(mtrx)
            #check longest column
            max_len = longest_solver.solve_longest_column()
#            print("\nmax_len    =", max_len)
            correct_len = Line(col_len, 0, 0, col_len-1, 0)
#            print("correct_len=", correct_len)
            self.assertEqual(correct_len, max_len)
            max_len = longest_solver.solve_longest_row()
            correct_len = Line(1, 0, 0, 0, 0)
            self.assertEqual(correct_len, max_len)
            max_len = longest_solver.solve_longest_diagonal_positive_slope()
            self.assertEqual(correct_len, max_len)
            max_len = longest_solver.solve_longest_diagonal_negative_slope()
            self.assertEqual(correct_len, max_len)
            max_len = longest_solver.solve_longest_run()
            correct_len = Line(col_len, 0, 0, col_len-1, 0)
            self.assertEqual(correct_len, max_len)


    def test_central_diagonal(self):
        """ runs kadane on a single diagonal """
        kronecker_delta = lambda i, j: 1 if i == j else 0
        for col_len in range(2, 10):
            mtrx = [[kronecker_delta(i, j) for i in range(col_len)] for j in range(col_len)]
            longest_solver = NbyMLongestPathSolver(mtrx)
            max_len = longest_solver.solve_longest_run()
            correctlen = Line(col_len, 0, 0, col_len-1, col_len-1)
            self.assertEqual(correctlen, max_len)


    def test_off_diagonals(self):
        """ test an off center diagonal """
        for col_len in range(3, 10):
            for offset in range(1, col_len-1):
                kronecker_delta = lambda i, j: 1 if i == (j + offset) else 0
                #this is a matrix which has one diagonal from (small=offset,big=0) to 
                #(small=col_len-offset,big=col_len)
                mtrx = [[kronecker_delta(sml, bg) for sml in range(col_len)] \
                         for bg in range(col_len)]
                longest_solver = NbyMLongestPathSolver(mtrx)
                max_len = longest_solver.solve_longest_run()
                correctlen = Line(col_len-offset, offset, 0,
                                  col_len-1, col_len-1-offset)
#                print( "\n")
#                print( "correctlen = ", correctlen)
#                print( "max_len    = ", max_len)
#                print( "\n")
                self.assertEqual(correctlen, max_len)
                #test opposite side
                kronecker_delta = lambda i, j: 1 if (i+offset) == j else 0
                mtrx = [[kronecker_delta(sml, bg) for sml in range(col_len)] \
                         for bg in range(col_len)]
                longest_solver = NbyMLongestPathSolver(mtrx)
                max_len = longest_solver.solve_longest_run()
                correctlen = Line(col_len-offset, 0, offset,
                                  col_len-1-offset, col_len-1)
#                print( "\n")
#                print( "correctlen = ", correctlen)
#                print( "max_len    = ", max_len)
#                print( "\n")
                self.assertEqual(correctlen, max_len)


    def test_off_central_diagonals_neg_slope(self):
        """ test single diagonal with negative slope"""
        kronecker_delta = lambda i, j: 1 if i == j else 0
        for col_len in range(3, 10):
            for offset in range(1, col_len-1):
                mtrx = [[kronecker_delta(i+offset, col_len-1-j) for i in \
                         range(col_len)] for j in range(col_len)]
                longest_solver = NbyMLongestPathSolver(mtrx)
                max_len = longest_solver.solve_longest_run()
                correctlen = Line(col_len-offset, 0, col_len-1-offset,
                                  col_len-1-offset, 0)
#                print( "\n")
#                print( "correctlen = ", correctlen)
#                print( "max_len    = ", max_len)
#                print( "\n")
                self.assertEqual(correctlen, max_len)
                mtrx = [[kronecker_delta(i+offset, j) for i in \
                         range(col_len)] for j in range(col_len)]
                longest_solver = NbyMLongestPathSolver(mtrx)
                max_len = longest_solver.solve_longest_run()
                correctlen = Line(col_len-offset, 0, offset,
                                  col_len-1-offset, col_len-1)
#                print( "\n")
#                print( "correctlen = ", correctlen)
#                print( "max_len    = ", max_len)
#                print( "\n")
                self.assertEqual(correctlen, max_len)


    def test_central_diagonal_neg_slope(self):
        """ test single diagonal with negative slope which is off center """
        kronecker_delta = lambda i, j: 1 if i == j else 0
        for col_len in range(2, 10):
            mtrx = [[kronecker_delta(i, col_len-1-j) for i in range(col_len)] for j in range(col_len)]
            longest_solver = NbyMLongestPathSolver(mtrx)
            max_len = longest_solver.solve_longest_run()
            correctlen = Line(col_len, 0, col_len-1, col_len-1, 0)
            self.assertEqual(correctlen, max_len)


if __name__ == "__main__":
    unittest.main()
