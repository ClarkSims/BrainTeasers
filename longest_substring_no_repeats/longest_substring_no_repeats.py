#!/usr/bin/env python3
"""
https://leetcode.com/problems/longest-substring-without-repeating-characters/
https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/
"""
import unittest
import string
import random


def all_unique(astring: str) -> bool:
    '''Test if all characters in a string occur only once.'''
    hist = [False for _ in range(256)]
    for val in astring:
        off = ord(val)
        if hist[off]:
            return False
        hist[off] = True
    return True


def brute_force(astr: str) -> int:
    '''Calls all_unique on all substrings, to find longest unique substring.
    This is an O(N^3) algorithm. Note, 2 for loops, order N, and one string
    copy order N, combine to make it N^3.
    '''
    longest = 0
    for i in range(0, len(astr)):
        for j in range(i + 1, len(astr) + 1):
            substr = astr[i:j]
            if all_unique(substr) and (j - i) > longest:
                longest = j - i
    return longest


class Solution:
    """LeetCode driver class"""

    def lengthOfLongestSubstring(self, input_str: str) -> int:
        """
        Implements an O(N) algorithm to find longest unique substring.
        Each longest substring at element i, is equal to the longest substring
        at i - 1, plus one char, if the char is not in the previous substring.
        If the char is in the previous substring, the longest at that point,
        starts at the previous occurance + 1.
        Loop over all i, save the maximum length at each iteration.

        https://leetcode.com/submissions/detail/281362570/
        Runtime: 48 ms, faster than 98.34% of Python3 online submissions for
        Longest Substring Without Repeating Characters.
        Memory Usage: 12.7 MB, less than 100.00% of Python3 online submissions
        for Longest Substring Without Repeating Characters.
        """
        last_occurance = [-1] * 256
        longest = 0
        curbegin = -1
        for off, val in enumerate(input_str):
            ascii_code = ord(val)
            if (last_occurance[ascii_code] != -1 \
                and last_occurance[ascii_code] > curbegin):
                curbegin = last_occurance[ascii_code]
                last_occurance[ascii_code] = off
            else:
                last_occurance[ascii_code] = off
                if off - curbegin > longest:
                    longest = off - curbegin
        return longest


class TestLeftRight(unittest.TestCase):
    """Manually specified cases."""

    def test1(self):
        """Explanation: The answer is "abc", with the length of 3"""
        sol = Solution()
        test_input = "abcabcbb"
        output = sol.lengthOfLongestSubstring(test_input)
        brute = brute_force(test_input)
        expected = 3
        self.assertEqual(expected, output)
        self.assertEqual(expected, brute)

    def test2(self):
        """
        test_input: "bbbbb"
        Output: 1
        Explanation: The answer is "b", with the length of 1."""
        sol = Solution()
        test_input = "bbbbb"
        output = sol.lengthOfLongestSubstring(test_input)
        expected = 1
        # Explanation: The answer is "abc", with the length of 3.
        self.assertEqual(expected, output)

    def test3(self):
        """test_input: "pwwkew"
        Output: 3
        Explanation: The answer is "wke", with the length of 3."""
        sol = Solution()
        test_input = "pwwkew"
        output = sol.lengthOfLongestSubstring(test_input)
        expected = 3
        self.assertEqual(expected, output)

    def test4(self):
        """Edge Case: string of length 1"""
        sol = Solution()
        test_input = " "
        output = sol.lengthOfLongestSubstring(test_input)
        expected = 1
        self.assertEqual(expected, output)

    def test5(self):
        """Explanation: mzuxt is longest substring, so answer is 5."""
        sol = Solution()
        test_input = "tmmzuxt"
        output = sol.lengthOfLongestSubstring(test_input)
        expected = 5
        # Explanation: The answer is "abc", with the length of 3.
        self.assertEqual(expected, output)


class TestRandom(unittest.TestCase):
    """Monte Carlo test, compares brute force solution to optimized solution"""

    def test_many(self):
        """Monte Carlo test, compares brute force solution to optimized solution"""
        import time

        sol = Solution()
        test_length = 100
        number_test = 1000
        total_time = 0
        for i in range(number_test):
            random.seed(i)
            test_input = "".join(
                random.choices(
                    string.ascii_lowercase,
                    k=test_length))
            start = time.time()
            output = sol.lengthOfLongestSubstring(test_input)
            end = time.time()
            total_time += end - start
            brute = brute_force(test_input)
            if output != brute:
                print("seed = ", i)
                print(test_input)
                print(output)
                print(brute)
                return
            self.assertEqual(output, brute)
        print("total time = {}".format(total_time))
        average_time = float(total_time) / number_test
        print("average_time = {}".format(average_time))


if __name__ == "__main__":
    unittest.main()
