#!/usr/bin/env python3
import unittest
from invert_binary_tree import left_to_right_invert_tree as left_to_right
from invert_binary_tree import up_to_down_invert_polytree as up_to_down

class Node:
    def __init__(self, datum, lhs=None, rhs=None):
        self.lhs = lhs
        self.rhs = rhs
        self.datum = datum

class TestLeftRight(unittest.TestCase):
    def test_3(self):
        lhs = Node(0)
        rhs = Node(2)
        head = Node(1,lhs,rhs)
        left_to_right(head)
        self.assertEqual(1,head.datum)
        self.assertEqual(2,head.lhs.datum)
        self.assertEqual(0,head.rhs.datum)


class TestUpDown(unittest.TestCase):
    def test_3(self):
        lhs = Node(0)
        rhs = Node(2)
        head = Node(1,lhs,rhs)
        head_list, node_set = up_to_down([head])
        self.assertEqual(2, len(head_list))
        self.assertEqual(0, head_list[0].datum)
        self.assertEqual(2, head_list[1].datum)


if __name__ == '__main__':
    unittest.main()
