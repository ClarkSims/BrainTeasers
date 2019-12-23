#!/usr/bin/env python3
import unittest
import copy
import bisect
import sys
import heapq
import math
import string
import random
from typing import List


def calc_used_length(number_occur):
    used_length = 0
    for off, num in enumerate(number_occur):
        used_length += (off + 1) * num
    return used_length


def calc_value(number_occur, values):
    value = 0
    for off, num in enumerate(number_occur):
        value += num * values[off]
    return value


def increment_number_occur(number_occur, max_len, upper_bounds):
    if len(upper_bounds) == 0:
        for off in range(max_len):
            upper_bounds.append(max_len // (off + 1))

    used_length = calc_used_length(number_occur)
    for off in range(max_len):
        if number_occur[off] < upper_bounds[off]:
            number_occur[off] += 1
            if off > 0:
                number_occur[:off] = [0] * off
            if calc_used_length(number_occur) <= max_len:
                return True

    return False


def demo_increment_number_occur(max_len):
    number_occur = [0] * max_len
    upper_bounds = []
    print(number_occur)
    while increment_number_occur(number_occur, max_len, upper_bounds):
        print(number_occur)


def brute_force_cutting_bars(values: List[int]) -> List[int]:
    len_values = len(values)
    number_occur = [0] * len_values
    max_value = 0
    max_number_occur = [0] * len_values
    upper_bounds = []

    while increment_number_occur(number_occur, len_values, upper_bounds):
        test_value = calc_value(number_occur, values)
        if test_value > max_value:
            max_value = test_value
            max_number_occur = copy.deepcopy(number_occur)

    # restate as items
    items = []
    off = len_values
    for num in reversed(max_number_occur):
        off -= 1
        if num > 0:
            items += [off + 1] * num

    return [max_value] + items


def cutting_bars(values: List[int]) -> List[int]:
    parents = {0: None}
    max_values = {0: 0}
    len_values = len(values)

    def iter_cutting_bars(max_len: int) -> int:
        nonlocal values, parents, max_values, len_values
        key = max_len
        if key in max_values:
            return max_values[key]
        max_off = None
        max_val = 0
        for off in range(len_values):
            reduced_max_len = max_len - (off + 1)
            if reduced_max_len >= 0:
                if reduced_max_len > 0:
                    test_val = iter_cutting_bars(reduced_max_len) + values[off]
                elif reduced_max_len == 0:
                    test_val = values[off]
                if test_val > max_val:
                    max_val = test_val
                    max_off = off
        parents[key] = max_off
        max_values[key] = max_val
        # print('for bar of length {} max_value is {}'.format(max_len, max_val))
        return max_val

    max_value = iter_cutting_bars(len_values)

    pnt = parents[len_values]
    bars = []
    remaining_len = len_values
    while remaining_len > 0 and pnt is not None:
        # print('pnt = ', pnt)
        bars.append(pnt + 1)
        remaining_len -= pnt + 1
        pnt = parents[remaining_len]
    return [max_value] + list(reversed(sorted(bars)))


class TestSimple(unittest.TestCase):
    def test1(self):
        values = [3, 6, 11, 12, 16, 18, 19, 21]
        output = cutting_bars(values)
        expected = [28, 3, 3, 1, 1]
        self.assertEqual(expected, output)

    def test2(self):
        values = [3, 6, 11, 12, 16, 18, 19, 21]
        output = brute_force_cutting_bars(values)
        expected = [28, 3, 3, 1, 1]
        self.assertEqual(expected, output)


class TestRandom(unittest.TestCase):
    def test1(self):
        for i in range(100):
            random.seed(i)
            max_len = random.randint(1, 10)
            values = random.choices(range(1, 100))
            dp_sol = cutting_bars(values)
            brute_sol = brute_force_cutting_bars(values)
            self.assertEqual(brute_sol, dp_sol)


def execute_from_console():
    line = sys.stdin.readline()
    strvals = line.split()
    ivals = [int(strval) for strval in strvals]
    output = cutting_bars(ivals)
    strout = " ".join(map(str, output))
    print(strout)


if __name__ == '__main__':
    # unittest.main()
    # demo_increment_number_occur(2)
    # demo_increment_number_occur(3)
    execute_from_console()
