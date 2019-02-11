#!/usr/bin/env python3
''' Question: Write a function to calculate all of the possible final 
    positions of a knight on a chess board, in a given number of moves.
'''
import sys

def knights_moves( prev_set, N=1):
    ''' This is an iterative function, which returns a set of tuples,
        which are possible coordinates on a chess board, of a knight 
        after N moves '''
    moves = [ (2, 1), (2, -1), (-2, 1), (-2, -1), \
        (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for i in range(0,N):
        next_set = set()
        for pos in prev_set:
            for move in moves:
                x, y = pos[0]+move[0], pos[1]+move[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    next_set.add((x, y))
        prev_set = next_set
    return prev_set


if __name__=='__main__':
    ''' simple demo / test of function '''
    no_move = set({(4,4)})
    one_move = knights_moves(no_move)
    print( "one move={");
    for pos in one_move:
        print(pos)
    print( "}")
    two_moves = knights_moves(one_move)
    print( "two moves={");
    for pos in two_moves:
        print(pos)
    print( "}")
    three_moves = knights_moves(two_moves)
    print( "three moves={");
    for pos in three_moves:
        print(pos)
    print( "}")
    print( "two_moves as vector");
    sys.stdout.write( "int two_moves[{}] = {{".format( 2*len(two_moves)))
    for pos in two_moves:
        sys.stdout.write("{}, {}, ".format(pos[0], pos[1]))
    sys.stdout.write( "}");
    sys.stdout.flush();

