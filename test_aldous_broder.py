"""test_aldous_broder.py - test the Aldous-Broder implementation
Copyright 2022 by Eric Conrad

USAGE

    usage: test_aldous_broder.py [-h] [-d DIM DIM]

    Test the implementation of the Aldous-Broder maze algorithm.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the toroidal grid

    (Testing is done on toroidal grids.)

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

import mazelib
from torus_grid import TorusGrid
from maze import Maze
from aldous_broder import AldousBroder

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

    desc = 'Test the Aldous-Broder maze algorithm.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the cylindrical grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'plain (first-entrance) Aldous-Broder on a toroidal grid')
    grid = TorusGrid(rows, cols)
    maze = Maze(grid)
    AldousBroder.on(maze, method=AldousBroder.plain)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 2)',
          'vanilla (last-exit) Aldous-Broder on a toroidal grid')
    grid = TorusGrid(rows, cols)
    maze = Maze(grid)
    AldousBroder.on(maze, method=AldousBroder.vanilla)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print()
    print('Test 3)',
          'blueberry (first-entrance) Aldous-Broder on a toroidal grid')
    grid = TorusGrid(rows, cols)
    maze = Maze(grid)
    print('set breakpoint after 30 cells...')
    AldousBroder.on(maze, method=AldousBroder.blueberry,
        init=True, debug=True,
        min_cells = len(grid.cells) // 2)
    print(maze)
    chi = maze_characteristic(maze)

    print('set breakpoint after 15 cells...')
    AldousBroder.on(maze, method=AldousBroder.blueberry,
        debug=True,
        min_cells = len(maze.unvisited) // 2)
    print(maze)
    chi = maze_characteristic(maze)

    print('finish run...')
    AldousBroder.on(maze, method=AldousBroder.blueberry,
        debug=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

# end of test_aldous_broder.py
