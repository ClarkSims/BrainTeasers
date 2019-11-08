#!/usr/bin/env python3
import unittest
import bisect
import sys
import heapq
import math
import string
import random
from typing import List


class chain_of_command:
    def __init__(self, employee):
        assert len(employee) == 6
        self._employee = employee
        self._supervises = {}
        self._supervised_by = {}
        self._relation = []

    def add_relation(self, rel):
        assert len(rel) == 12
        supr = rel[:6]
        emp = rel[6:]
        self._relation.append((emp, supr))
        self._supervised_by[emp] = supr
        if supr in self._supervises:
            self._supervises[supr].append(emp)
        else:
            self._supervises[supr] = [emp]

    def get_supervisors(self):
        if len(self._supervises) == 0:
            self.populate_graphs()
        suprs = []
        eid = self._employee
        while eid in self._supervised_by:
            supr = self._supervised_by[eid]
            suprs.append(supr)
            eid = supr
        rv = list(reversed(suprs))
        return rv

    def get_employees(self):
        if len(self._supervises) == 0:
            self.populate_graphs()
        queue = [self._employee]
        employees = []
        while len(queue) > 0:
            eid = queue[0]
            queue.pop(0)
            if eid in self._supervises:
                queue += self._supervises[eid]
                employees += self._supervises[eid]
        return employees

    @classmethod
    def process_input_iter(cls, inputitr):
        begin = True
        for line in inputitr:
            if begin:
                begin = False
                retobj = chain_of_command(line)
            else:
                retobj.add_relation(line)


class TestChain(unittest.TestCase):
    def test1(self):
        a = 'aaaaaa'
        b = 'bbbbbb'
        c = 'cccccc'
        d = 'dddddd'
        z = 'zzzzzz'
        cc = chain_of_command(b)
        cc.add_relation(b + c)
        cc.add_relation(b + d)
        cc.add_relation(a + b)
        cc.add_relation(z + a)
        bosses = cc.get_supervisors()
        underlings = cc.get_employees()
        self.assertEqual([z, a], bosses)
        self.assertEqual([c, d], underlings)


if __name__ == '__main__':
    #unittest.main()
    empobj = chain_of_command.process_input_iter(sys.stdin)
    print('employee')
    print(empobj._employee)
    print('chain-of command')
    suprs = empobj.get_supervisors()
    for supr in suprs:
        print(supr)
    print('supervises')
    unders = empobj.get_employees()
    for undr in unders:
        print(undr)
