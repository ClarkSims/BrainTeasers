#!/usr/bin/env python3
import unittest
import random
import copy
import sys


def flip(arr, i):
    start = 0
    flipped = [-val for val in reversed(arr[:(i + 1)])]
    arr[:(i + 1)] = flipped


# Returns index of the maximum
# element in arr[0..n-1] */


def findMax(arr, n):
    mi = 0
    cur_max = abs(arr[mi])
    for i in range(0, n):
        test_max = abs(arr[i])
        if test_max > cur_max:
            mi = i
            cur_max = test_max
    return mi


def printArray(arr):
    for val in arr:
        print("%d" % val, end=" ")
    print('')


# The main function that
# sorts given array
# using flip operations
def pancakeSort(arr, verbose=False, debug=False):
    if debug:
        verbose = True
    # Start from the complete
    # array and one by one
    # reduce current size
    # by one
    curr_size = len(arr)
    num_flip = 0
    while curr_size > 1:
        # Find biggest unsorted pancake
        mi = findMax(arr, curr_size)

        if mi != curr_size - 1 or arr[mi] < 0:

            # put largest pancake on top
            if mi != 0:
                num_flip += 1
                if verbose:
                    print('flipping:', arr[mi])
                flip(arr, mi)
                if debug:
                    printArray(arr)

            # make top pancake burn't side up
            if arr[0] > 0:
                num_flip += 1
                if verbose:
                    print('flipping:', arr[0])
                flip(arr, 0)
                if debug:
                    printArray(arr)

            # Now move the maximum
            # number to end by
            # reversing current array
            num_flip += 1
            if verbose:
                print('flipping:', arr[curr_size - 1])
            flip(arr, curr_size - 1)
            if debug:
                printArray(arr)

        curr_size -= 1

    # check that top pancake is bit burn't side up
    if arr[0] < 0:
        num_flip += 1
        if verbose:
            print('flipping:', arr[0])
        flip(arr, 0)
        if debug:
            printArray(arr)

    return num_flip


class TestPancake(unittest.TestCase):
    def test_demo(self):
        arr = [2, 1, 4, -6, 3, 5]
        num_flip = pancakeSort(arr)
        self.assertEqual(10, num_flip)

    def test_many_random(self):
        num_test = 1000
        for testcase in range(num_test):
            num_cakes = random.randint(1, 20)
            sorted_stack = [off + 1 for off in range(num_cakes)]
            unsorted_stack = copy.deepcopy(sorted_stack)
            random.shuffle(unsorted_stack)
            for off in range(num_cakes):
                if random.randint(0, 1) % 2 == 1:
                    unsorted_stack[off] *= -1
            pancakeSort(unsorted_stack)
            self.assertEqual(sorted_stack, unsorted_stack)


def commandline_main():
    run_unit_test = (len(sys.argv) > 0 and sys.argv[1] == '-u')
    verbose = (len(sys.argv) > 0 and sys.argv[1] == '-v')
    debug = len(sys.argv) > 0 and sys.argv[1] == '-vv'
    if run_unit_test:
        sys.argv = [sys.argv[0]]
        unittest.main()
    else:
        pancakes = []
        for line in sys.stdin:
            pansize = int(line)
            pancakes.append(pansize)
        num_flip = pancakeSort(pancakes, verbose, debug)
        print('moves:', num_flip)


if __name__ == '__main__':
    commandline_main()
    # unittest.main()
