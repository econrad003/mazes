"""test_grid.py - test grid implementation
Copyright 2022 by Eric Conrad

USAGE

    usage: test_grid.py [-h] [-d DIM DIM]

    Test grid implementation.

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

import mazelib
from cell import Cell, SquareCell
from grid import Grid, RectangularGrid
from maze import Maze
from binary_tree import BinaryTree

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

def maze_characteristic(maze, output=True):
    """determine the Euler characteristic of the maze

    Returns v - e - k.

    BUGS

        Will fail if there are one-way passages.
    """
    grid = maze.grid
    v = maze.v
    e = maze.e
    k = maze.k
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

    desc = 'Test grid implementation.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the rectangular grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)', 'a 2x3 test maze')
    grid = RectangularGrid(2, 3)
    cell = grid[(0,0)]
    north = grid[(1,0)]
    northeast = grid[(1,1)]
    south = grid[(-1,0)]
    east = grid[(0,1)]
    west = grid[(0,-1)]
    fareast = grid[(0,2)]
    ene = grid[(1,2)]

    assert isinstance(cell, Cell)
    assert isinstance(cell, SquareCell)
    assert isinstance(north, SquareCell)
    assert not isinstance(south, SquareCell)
    assert isinstance(east, SquareCell)
    assert not isinstance(west, SquareCell)
    assert not cell.isLinkedTo(north)
    assert not cell.isLinkedTo(south)
    assert not cell.isLinkedTo(east)
    assert not cell.isLinkedTo(west)
    
        # make a simple binary tree
    cell.link(east)
    east.link(northeast)
    north.link(northeast)
    fareast.link(ene)
    ene.link(northeast)
    cell.text = 'A'
    east.text = 'B'
    fareast.text = 'C'
    ene.text = 'D'
    northeast.text = 'E'
    north.text = 'F'
    maze = Maze(grid)
    print(maze)

    assert east.isLinkedTo(cell)
    assert not cell.isLinkedTo(north)
    assert not north.isLinkedTo(cell)
    hw = '+---+---+---+\n'
    toprow = '| F   E   D |\n'
    middlerow = '+---+   +   +\n'
    bottomrow = '| A   B | C |\n'
    assert str(grid) == hw + toprow + middlerow + bottomrow + hw[:-1]

        # checking Maze.components property
    foo = maze.components
    assert len(foo) == 1
    foo = list(foo)[0]
    assert foo == set(maze.grid.cells)

    bar = set([])
    for x in foo:
        bar.add(x.text)
    print(bar)
    assert bar == set(['A', 'B', 'C', 'D', 'E', 'F'])

    chi = grid_characteristic(maze)
    assert chi == 0
    chi = maze_characteristic(maze)
    assert chi == 0

    print()
    print('Testing exception handling')
    try:
        f = maze.f
        assert False, "Exception not raised"
    except ValueError as e:
        print('Successfuly raised exception:', repr(e))

        # clone the small binary tree maze
    print()
    print('Test 2)', 'cloning a maze.')
    maze2 = maze.clone()
    print(maze2)
    assert str(maze2) == str(grid)

        # construct a binary tree maze of the required dimensions
    print()
    print('Test 3)', 'construct a maze')
    grid = RectangularGrid(rows, cols)
    maze = Maze(grid)
    BinaryTree.on(maze, directions=('south', 'west'), p=0.7)
    print('binary tree - south/west with p=0.7, q=0.3')
    print(maze)
    assert grid[(0,0)].isLinkedTo(grid[(0,1)])
    assert grid[(0,0)].isLinkedTo(grid[(1,0)])

    hpassages = 0
    for i in range(rows):
        for j in range(cols):
            if not grid[(i,j)].isLinkedTo(grid[i, j+1]):
                hpassages += 1

    vpassages = 0
    for j in range(cols):
        for i in range(rows):
            if not grid[(i,j)].isLinkedTo(grid[i+1, j]):
                vpassages += 1

    orthogonals = hpassages + vpassages
    pct1 = hpassages / orthogonals
    pct2 = vpassages / orthogonals
    print(f'  vertical passages: {vpassages:5} ({pct2:5.2} %)')
    print(f'horizontal passages: {hpassages:5} ({pct1:5.2} %)')

    chi = grid_characteristic(maze)
    assert chi == 0
    chi = maze_characteristic(maze)
    assert chi == 0

    print('Success!')

# end of test_grid.py
