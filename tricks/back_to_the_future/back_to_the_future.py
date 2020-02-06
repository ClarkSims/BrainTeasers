#!/usr/bin/env python3
import unittest
import bisect
import sys
import heapq
import math
import string
import random
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        test_profit = 0
        lag_price = prices[0]
        for off in range(1, len(prices)):
            test_profit = math.log(prices[off] / lag_price)
            if test_profit > max_profit:
                max_profit = test_profit
            elif test_profit < 0:
                test_profit = 0
                lag_price = prices[off]
        return math.exp(max_profit) - 1


def read_prices():
    prices = []
    for line in sys.stdin:
        aprice = float(line)
        prices.append(aprice)
    return prices


def main():
    sol = Solution()
    prices = read_prices()
    max_gain = sol.maxProfit(prices)
    print(max_gain * 1000)


if __name__ == '__main__':
    main()
