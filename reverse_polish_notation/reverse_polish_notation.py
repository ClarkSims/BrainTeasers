#!/usr/bin/env python3
import unittest

import sys
import heapq
import math
import string
import random
from builtins import classmethod
from typing import List


class Solution:
    def applyOp(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if a * b < 0:
                return -(abs(a) // abs(b))
            return a // b

    def evalRPN(self, tokens: List[str]) -> int:
        values = []
        stack = []
        ops = set(["+", "-", "*", "/"])

        for token in tokens:
            if token in ops:
                arg2 = stack.pop()
                arg1 = stack.pop()
                result = self.applyOp(arg1, arg2, token)
                stack.append(result)
            else:
                stack.append(int(token))

        return stack.pop()


class TestLeftRight(unittest.TestCase):
    def test1(self):
        s = Solution()
        input = ["2", "1", "+", "3", "*"]
        expected = 9
        output = s.evalRPN(input)
        self.assertEqual(expected, output)

    def test2(self):
        s = Solution()
        input = ["4", "13", "5", "/", "+"]
        expected = 6
        output = s.evalRPN(input)
        self.assertEqual(expected, output)

    def test3(self):
        s = Solution()
        input = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
        expected = 22
        output = s.evalRPN(input)
        self.assertEqual(expected, output)

    def test4(self):
        s = Solution()
        from test4 import INPUT

        expected = 7143937
        output = s.evalRPN(INPUT)
        self.assertEqual(expected, output)

    def test5(self):
        s = Solution()
        from test5 import INPUT

        expected = -231
        output = s.evalRPN(INPUT)
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
    # inputline = sys.
