"""test_hybrid_abw.py - test the implementation of the hybrid
    Aldous-Broder/Wilson algorithm
Copyright 2022 by Eric Conrad

USAGE

    usage: test_hybrid_abw.py [-h] [-d DIM DIM]

    Test the hybrid Aldous-Broder first-entrance/Wilson circuit-erased
         random walk algorithm.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the cylindrical grid

    (Testing is done on a cylindrical grid.)

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
from cylinder_grid import CylinderGrid
from maze import Maze
from aldous_broder_wilson import HybridABW

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

    desc = 'Test the hybrid Aldous-Broder' + \
        ' first-entrance/Wilson circuit-erased random walk algorithm.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the cylindrical grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'The hybrid ABW algorithm on a cylindrical grid')
    print('cutoff density: 50%')
    grid = CylinderGrid(rows, cols)
    maze = Maze(grid)
    HybridABW.on(maze, debug=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print('Test 2)',
          'The hybrid ABW algorithm on a cylindrical grid')
    print('cutoff density: 75%')
    grid = CylinderGrid(rows, cols)
    maze = Maze(grid)
    HybridABW.on(maze, debug=True, density=0.75)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

# end of test_hybrid_abw.py
