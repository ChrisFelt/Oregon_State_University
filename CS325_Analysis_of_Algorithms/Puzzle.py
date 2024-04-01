# CS 325 - Analysis of Algorithms
# Graph Traversal - Portfolio Project
# Author: Christopher Felt
# Date: 20 May 2022
# Description: Function that finds and returns the shortest path in a given maze
# from a given starting point to a given ending point in that maze. Uses a
# breadth-first search approach.

from collections import deque


def solve_puzzle(board, source, dest):
    """
    :param board: 2-D array representation of a maze with open spaces marked as
                '-' and barriers marked as something else.
    :param source: starting coordinates in the maze as a tuple (row, col).
    :param dest: destination coordinates as a tuple (row, col).
    :return: a list of tuple coordinates of the shortest path from the source to
                the destination, and a string of the directions taken to get there.
    """
    # board dimensions
    row, col = len(board), len(board[0])

    # initialize set of visited coordinates
    visited = set()

    # initialize deque of coordinates to visit
    queue = deque()

    # start at source - append to deque
    queue.appendleft((source[0], source[1], [source], ''))

    # explore coordinates in deque
    while len(queue) > 0:
        # pop right side of deque and parse out contents
        cur_row, cur_col, path, direc = queue.pop()

        # return path and directions if at final cell
        if (cur_row, cur_col) == dest:
            return path, direc

        # skip if already visited
        if (cur_row, cur_col) in visited:
            continue

        # mark coordinates as visited
        visited.add((cur_row, cur_col))

        # append neighboring cells to deque for exploration
        for y, x, d in [[0, 1, 'R'], [0, -1, 'L'], [1, 0, 'D'], [-1, 0, 'U']]:

            # neighboring cell coordinates
            new_row, new_col = cur_row + y, cur_col + x

            # skip if coordinates outside board
            if new_row < 0 or new_row >= row or new_col < 0 or new_col >= col:
                continue

            # skip cell if it contains a barrier or has already been visited
            if board[new_row][new_col] != '-' or (new_row, new_col) in visited:
                continue

            # append neighbor to deque - add coordinates to path and direction to direction string
            queue.appendleft((new_row, new_col, path + [(new_row, new_col)], direc + d))
