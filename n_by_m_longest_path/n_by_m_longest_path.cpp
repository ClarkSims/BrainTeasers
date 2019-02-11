#include <iostream>
#include <assert.h>
#include <string.h>
#include <limits>
#include "n_by_m_longest_path.h"

/**
  * Calls 4 separate flavors of solveLongestRun
  */
void NbyMLongestPathSolver::solveLongestRun( Line& answer) {
    Line test;
    solveLongestColumn(answer);
    solveLongestRow(test);
    if (test._length > answer._length) {
        answer = test;
    }
    solveLongestDiagonalWithPositiveSlope(test);
    if (test._length > answer._length) {
        answer = test;
    }
    solveLongestDiagonalWithNegativeSlope(test);
    if (test._length > answer._length) {
        answer = test;
    }
}

/**
  * Column is synonymous with big stride. This function loops through the set of
  * all columns and finds the longest run within each subset, by calling kadane.
  * It returns the maximum run among all columns.
  */
void NbyMLongestPathSolver::solveLongestColumn( Line& answer) {
    VectorWithinMatrix vect;
    Line test;
    int col_offset;

    vect._matrix = _matrix;
    vect._small_stride_begin = 0;
    vect._del_small_stride = 1;
    vect._del_big_stride = 0;

    if (_matrix && _matrix->_big_stride_max) {
        vect._big_stride_begin = 0;
        vect.kadane(answer);
    } else {
        answer.set_null();
    }
    for (col_offset = 1; col_offset < _matrix->_big_stride_max; ++col_offset) {
        vect._big_stride_begin = col_offset; 
        vect.kadane( test);
        if (test._length > answer._length) {
            answer = test;
        }
    }
}

/**
  * Row is synonymous with small stride. This function loops through the set of
  * all rows and finds the longest run within each subset, by calling kadane.
  * It returns the maximum run among all rows.
  */
void NbyMLongestPathSolver::solveLongestRow( Line& answer) {
    VectorWithinMatrix vect;
    Line test;
    int row_offset;

    vect._matrix = _matrix;
    vect._big_stride_begin = 0;
    vect._del_small_stride = 0;
    vect._del_big_stride   = 1;

    if (_matrix && _matrix->_small_stride_max) {
        vect._small_stride_begin = 0;
        vect.kadane(answer);
    } else {
        answer.set_null();
    }
    for (row_offset = 1; row_offset < _matrix->_small_stride_max; ++row_offset) {
        vect._small_stride_begin = row_offset; 
        vect.kadane( test);
        if (test._length > answer._length) {
            answer = test;
        }
    }
}

/**
  * This function loops through the set of
  * all diagonals with positive slope and finds the longest run within each 
  * subset, by calling kadane. It returns the maximum run among all diagonals 
  * with positive slope.
  */
void NbyMLongestPathSolver::solveLongestDiagonalWithPositiveSlope( Line& answer) {
    VectorWithinMatrix vect;
    Line test;
    int row_offset, col_offset;

    vect._matrix = _matrix;
    vect._big_stride_begin = 0;
    vect._del_small_stride = 1;
    vect._del_big_stride   = 1;

    if (_matrix && _matrix->_small_stride_max) {
        vect._small_stride_begin = 0;
        vect.kadane(answer);
    } else {
        answer.set_null();
    }
    for (row_offset = 0; row_offset < _matrix->_small_stride_max; ++row_offset) {
        vect._small_stride_begin = row_offset; 
        vect.kadane(test);
        if (test._length > answer._length) {
            answer = test;
        }
    }
    for (col_offset = 0; col_offset < _matrix->_big_stride_max; ++col_offset) {
        vect._big_stride_begin = row_offset; 
        vect.kadane(test);
        if (test._length > answer._length) {
            answer = test;
        }
    }
}

/**
  * This function loops through the set of
  * all diagonals with negative slope and finds the longest run within each 
  * subset, by calling kadane. It returns the maximum run among all diagonals 
  * with negative slope.
  */
void NbyMLongestPathSolver::solveLongestDiagonalWithNegativeSlope( Line& answer) {
}


