#!/usr/bin/env python3
''' This module has functions for inverting binary trees and poly-trees. I deal with both
    left to right and up to down inversions.'''

def left_to_right_invert_tree(root_node):
    ''' invert a binary tree left to right '''
    root_node.lhs, root_node.rhs = root_node.rhs, root_node.lhs
    if root_node.lhs is not None:
        left_to_right_invert_tree(root_node.lhs)
    if root_node.rhs is not None:
        left_to_right_invert_tree(root_node.rhs)


def up_to_down_invert_polytree(root_node_list):
    ''' invert a polytree up to down '''
    all_nodes = set()
    new_root_node_list = []
    for node in root_node_list:
        updown_inversion_helper(None, node, all_nodes, new_root_node_list)
    return (new_root_node_list, all_nodes)


def updown_inversion_helper(parent, node, visited, new_root_node_list):
    ''' does work for up_down_invert_polytree '''
    is_new_root = True
    if node.lhs is not None:
        updown_inversion_helper(node, node.lhs, visited, new_root_node_list)
        is_new_root = False
    if node.rhs is not None:
        updown_inversion_helper(node, node.rhs, visited, new_root_node_list)
        is_new_root = False
    visited.add(node)
    if is_new_root:
        new_root_node_list.append(node)
    if parent is not None:
        if parent.lhs == node:
            node.rhs = parent
            node.lhs = None
        elif parent.rhs == node:
            node.rhs = None
            node.lhs = parent
