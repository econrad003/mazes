"""test_Moebius_strip.py - test Moebius strip grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_Moebius_strip.py [-h] [-d DIM DIM]

    Test the Moebius strip grid.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the fundamental rectangle

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
from Moebius_grid import MoebiusGrid
from maze import Maze
from binary_search_tree import DFSBinaryTree

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

def grid_characteristic(maze, output=True):
    """determine the Euler characteristic of the grid

    Returns v - e + f - k.
    """
    grid = maze.grid
    v = grid.v
    e = grid.e
    f = grid.f
    k = grid.k
    expect = v - e + f - k
    chi = grid.Euler_chi
    if output:
        print('Grid characteristic:')
        print('       number of nodes:', '            v =', v)
        print('       number of edges:', '            e =', e)
        print('       number of faces:', '            f =', f)
        print('  number of components:', '            k =', k)
        print('  Euler characteristic:', 'v - e + f - k =', chi)
    assert chi == expect, f'characteristic {chi}, expected {expect}'
    return chi

if __name__ == '__main__':
    import argparse

    desc = 'Test the Moebius strip grid.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the fundamental rectangle')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)', 'some east/west pairs on a Moebius strip grid')
    grid = MoebiusGrid(rows, cols)
    maze = Maze(grid)

    cell = grid[(0,0)]
    cell.text = '1'
    cell['west'].text = '1'

    cell = grid[(3,3)]
    cell.text = '2'
    cell['west'].text = '2'

    cell = grid[(0,cols-1)]
    cell.text = '3'
    cell['east'].text = '3'

    print(maze)

    print()
    print('Test 2)', 'a binary spanning maze on a Moebius strip grid')
    grid = MoebiusGrid(rows, cols)
    maze = Maze(grid)
    DFSBinaryTree.on(maze, mark_root=True)
    print(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    print()
    print('Test 3)', 'grid characteristic')
    chi = grid_characteristic(maze)

    print('Success!')

# end of test_cylinder.py
