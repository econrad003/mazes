"""test_mask.py - test the MaskedGrid implementation
Copyright 2022 by Eric Conrad

USAGE

    usage: test_mask.py [-h]

    Test the MaskedGrid implementation.

    optional arguments:
        -h, --help
                          show this help message and exit

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
from grid import RectangularGrid
from maze import Maze
from wilson import Wilson
from masked_grid import MaskedGrid, make_mask
from maze_pillow import MazeSketcher

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

    desc = 'Test the MaskedGrid implementation.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(6, 10),
        help='the dimensions of the Moebius grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'Wilson\'s algorithm on a masked 5x7 rectangular grid')
    grid = RectangularGrid(5, 7)
    maze = Maze(grid)

    print('Cell (2,3) in the middle of the grid is hidden')
    masked_grid = MaskedGrid(grid)

    grid[(2, 3)].text = 'H'
    cell = masked_grid[(2, 3)]
    masked_grid.hide(cell)

    nbr = cell[RectangularGrid.NORTH]
    assert nbr.index == (3, 3)
    assert not nbr[RectangularGrid.SOUTH]

    nbr = cell[RectangularGrid.EAST]
    assert nbr.index == (2, 4)
    assert not nbr[RectangularGrid.WEST]

    masked_maze = Maze(masked_grid)
    Wilson.on(masked_maze)
    print(maze)
    chi = maze_characteristic(maze)
    assert maze.k == 2

    print('Test 2)',
          'Wilson\'s algorithm on a masked rectangular grid')
    filename = 'test_mask.txt'
    print(f'Template: {filename}')
    grid, masked_grid = make_mask(filename)
    assert grid.rows == 17 and grid.cols == 66

    for index in masked_grid.hidden:
        grid[index].color = 'grey'

    maze = Maze(masked_grid)
    Wilson.on(maze)

    maze = Maze(grid)
    grid._kwargs['cell_width'] = 20
    grid._kwargs['cell_height'] = 20
    sketcher = MazeSketcher(maze, \
        title='Wilson\'s algorithm on a masked rectangular grid')
    maze.sketch()

    print('Success!')
# end of test_mask.py
