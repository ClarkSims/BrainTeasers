#!/usr/bin/env python3
import unittest
import bisect
import sys
import heapq
import math
import string
import random
from typing import List, Tuple


class Solution:
    def Valentines(self, hr_record: List[str]) -> List[Tuple]:
        dag = {}
        num_valentine = {}
        in_degree = {}
        for rec in hr_record:
            sup = rec[:6]
            emp = rec[6:]
            in_degree[emp] = 0
            in_degree[sup] = 0

        for rec in hr_record:
            sup = rec[:6]
            emp = rec[6:]
            if emp in dag:
                dag[emp].append(sup)
            else:
                dag[emp] = [sup]
            in_degree[sup] += 1
            num_valentine[sup] = 0

        lowest = set()
        for empid, degree in in_degree.items():
            if degree == 0:
                lowest.add(empid)

        next_lowest = set()
        while len(lowest) > 0:
            #print('lowest = ', lowest)
            for emp in lowest:
                if emp in dag:
                    for sup in dag[emp]:
                        num_valentine[sup] += 1
                        if emp in num_valentine:
                            num_valentine[sup] += num_valentine[emp]
                        next_lowest.add(sup)
            lowest = next_lowest
            next_lowest = set()

        ret_list = [(name, count) for name, count in num_valentine.items()]

        def key_rev_count(name_count):
            return -name_count[1]

        sorted_ret_list = sorted(ret_list, key=key_rev_count)
        return sorted_ret_list


class TestLeftRight(unittest.TestCase):
    @unittest.skip
    def test1(self):
        s = Solution()
        input = ['aaaaaabbbbbb', 'aaaaaacccccc', 'aaaaaadddddd']
        expected = [(3, 'aaaaaa')]
        output = s.Valentines(input)
        self.assertEqual(expected, output)

    def test2(self):
        input = ['aaaaaabbbbbb', 'aaaaaacccccc', 'aaaaaadddddd',
                 'zzzzzzbbbbbb', 'zzzzzzcccccc', 'zzzzzzdddddd',
                 'yyyyyyaaaaaa', 'yyyyyyzzzzzz']
        expected = [('yyyyyy', 8),
                    ('aaaaaa', 3),
                    ('zzzzzz', 3)]

        output = s.Valentines(input)
        self.assertEqual(expected, output)


def main():
    lines = []
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
            lines.append(line)
    s = Solution()
    output = s.Valentines(lines)
    for id_num in output:
        print('{} : {}'.format(*id_num))


if __name__ == '__main__':
    # unittest.main()
    main()
