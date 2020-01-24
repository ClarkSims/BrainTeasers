#!/usr/bin/env python3
import unittest
import sys
import copy
import random


def test_then_append(xtest, ytest, dim, visited, boundary):
    if xtest >= 0 and xtest < dim and \
            ytest >= 0 and ytest < dim:
        if not visited[xtest][ytest]:
            boundary.append((xtest, ytest))


def get_next_boundary(xcoord, ycoord, dim, visited):

    boundary = []

    xtest = xcoord - 1
    ytest = ycoord
    test_then_append(xtest, ytest, dim, visited, boundary)
    xtest = xcoord + 1
    test_then_append(xtest, ytest, dim, visited, boundary)

    xtest = xcoord
    ytest = ycoord - 1
    test_then_append(xtest, ytest, dim, visited, boundary)
    ytest = ycoord + 1
    test_then_append(xtest, ytest, dim, visited, boundary)

    return boundary


def bug_walk(seed, dim):
    visited = []
    all_false = [False] * dim
    visited = [all_false]
    for _ in range(1, dim):
        visited.append(copy.deepcopy(all_false))
    visited[0][0] = True
    boundary = [(0, 1), (1, 0)]
    random.seed(seed)
    finished = False
    steps = 0
    while boundary and not finished:
        choice = random.randint(0, len(boundary) - 1)
        steps += 1
        xcoord = boundary[choice][0]
        ycoord = boundary[choice][1]
        if xcoord == dim - 1 and ycoord == dim - 1:
            finished = True
            break
        visited[xcoord][ycoord] = True
        boundary = get_next_boundary(xcoord, ycoord, dim, visited)

    return (finished, steps)


def simulation(dim, num_iter):
    num_finished = 0
    num_steps = 0
    for seed in range(num_iter):
        (finished, steps) = bug_walk(seed, dim)
        if finished:
            num_finished += 1
            num_steps += steps
        #print(seed, finished, steps)

    if num_finished:
        prob_finish = float(num_finished) / num_iter
        average_len = float(num_steps) / num_finished
        return (prob_finish, average_len)
    else:
        return (0, 0)


def main():
    for dim in range(3, 10):
        prob_finish, average_len = simulation(dim, 10000)
        print(prob_finish, average_len)


main()
