"""test_backtracker.py - test the recursive backtracker methods
Copyright 2022 by Eric Conrad

USAGE

    usage: test_backtracker.py [-h] [-d DIM DIM]

    Test spanning tree search algorithms.

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
from recursive_backtracker import DFSSpanningTree, BFSSpanningTree, \
    RFSSpanningTree, Prim, FalsePrim

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

    desc = 'Test spanning tree search algorithms.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the rectangular grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)', 'DFS spanning tree on a rectangular grid')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    DFSSpanningTree.on(maze, mark_root=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 2)', 'DFS spanning tree (no shuffling)')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    DFSSpanningTree.on(maze, mark_root=True, shuffle_hood=False)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 3)', 'BFS spanning tree on a rectangular grid')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    BFSSpanningTree.on(maze, mark_root=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 4)', 'BFS spanning tree (no shuffling)')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    BFSSpanningTree.on(maze, mark_root=True, shuffle_hood=False)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Success!')

    print('Test 5)', 'RFS spanning tree')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    RFSSpanningTree.on(maze, mark_root=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 6)', 'Prim\'s minimum weight spanning tree')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    priorities = {}
    for cell in grid.cells:
        for nbr in cell.neighbors:
            key = frozenset([cell, nbr])
            if key in priorities:
                continue
            priorities[key] = 1 + random()
    Prim.on(maze, mark_root=True, priority=priorities)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')
    net_weight = 0
    for wall in priorities:
        if len(wall) < 2:
            continue
        cell1, cell2 = list(wall)
        if cell1.isLinkedTo(cell2):
            net_weight += priorities[wall]
    print('Weight of maze:', net_weight)
    print('Weight per edge:', net_weight/(maze.v - 1))

    print('Test 7)', 'False Prim spanning tree (using cell weights)')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    priorities = {}
    for cell in grid.cells:
        priorities[cell] = 1 + random()
    FalsePrim.on(maze, mark_root=True, priority=priorities)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

        # first metric
    net_weight = 0
    for cell in priorities:
        net_weight += len(cell.passages) * priorities[cell]
    net_weight /= 2       # since each edge has been counted twice
    print('Weight of maze:', net_weight)
    print('Weight per cell:', net_weight/maze.v)

        # second metric
    net_weight = 0
    e = 0
    for cell in grid.each_cell():
        for nbr in cell.passages:
            priority = min(priorities[cell], priorities[nbr])
            net_weight += priority
            e += 1
    net_weight /= 2
    e //= 2
    print('Alternate weight:', net_weight)
    print('Weight per edge:', net_weight / e)

    print('Success!')

# end of test_cylinder.py
