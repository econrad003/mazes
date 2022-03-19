"""test_binary_search.py - test binary search methods
Copyright 2022 by Eric Conrad

USAGE

    usage: test_binary_search.py [-h] [-d DIM DIM]

    Test binary search tree implementation.

    optional arguments:
          -h, --help
                        show this help message and exit
          -d DIM DIM, --dim DIM DIM
                        the dimensions of the rectangular grid

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
        <https://www.gnu.org/licenses/>.
"""

from random import random

import mazelib
from grid import RectangularGrid
from maze import Maze
from binary_search_tree import DFSBinaryTree, BFSBinaryTree, \
    BinarySearchTree
from maze_support import Heap

def maze_characteristic(maze, output=True):
    """determine the Euler characteristic of the maze

    Returns v - e - k.

    BUGS

        Will fail if there are one-way passages.
    """
    grid = maze.grid
    v = len(grid.cells)
    k = len(maze.components)

    ee = 0
    for cell in grid.each_cell():
        passages = set(cell.passages)
        ee += len(passages)
        if cell in passages:
            ee += 1         # loops are counted twice
     
    e = ee / 2 if ee % 2 else ee // 2
    chi = v - e - k
    if output:
        print('Maze characteristic:')
        print('       number of nodes:', '        v =', v)
        print('       number of edges:', '        e =', e)
        print('  number of components:', '        k =', k)
        print('  Euler characteristic:', 'v - e - k =', chi)
    return chi

if __name__ == '__main__':
    import argparse

    desc = 'Test binary search tree implementation.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the rectangular grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)', 'binary spanning tree using depth-first search')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    DFSBinaryTree.on(maze, mark_root='X')
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')

    print('Test 2)', 'binary spanning tree using breadth-first search')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    BFSBinaryTree.on(maze, mark_root='X')
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')

    print('Test 3)', 'binary spanning tree using random-first search')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    BinarySearchTree.on(maze, mark_root='X')
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')

    print('Test 4)', 'binary spanning tree using a heap')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)

        # assign weights
    maze.myweights = {}
    minwgt = float('inf')
    startcell = None
    for cell in maze.grid.each_cell():
        for nbr in cell.neighbors:
            key = frozenset([cell, nbr])
            if not key in maze.myweights:
                wgt = random()
                maze.myweights[key] = wgt
                if wgt < minwgt:
                    minwgt = wgt
                    startcell = cell

    pr = lambda maze, cell1, cell2: \
          maze.myweights[frozenset([cell1, cell2])]

    heap = Heap()

    BinarySearchTree.on(maze, root=startcell,
                        mark_root='X', queue=heap, priority=pr)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')

    print('Success!')

# end of test_grid.py
