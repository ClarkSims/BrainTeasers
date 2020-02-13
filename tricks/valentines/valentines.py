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

        lowest = set()
        num_valentine = {}
        for empid, degree in in_degree.items():
            if degree == 0:
                lowest.add(empid)
            else:
                num_valentine[empid] = 0

        while len(lowest) > 0:
            next_lowest = set()
            for empid in lowest:
                # give valentines from subordinates to first supervisor
                if empid in num_valentine and empid in dag:
                    supid = dag[empid][0]
                    num_valentine[supid] += num_valentine[empid]
                # write one valentine to each supervisor
                if empid in dag:
                    for supid in dag[empid]:
                        num_valentine[supid] += 1
                        in_degree[supid] -= 1
                        if in_degree[supid] == 0:
                            next_lowest.add(supid)
            lowest = next_lowest

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
        expected = [('aaaaaa', 3)]
        output = s.Valentines(input)
        self.assertEqual(expected, output)

    def test2(self):
        s = Solution()
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
