"""test_polar_grid.py - test the polar grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_polar_grid.py [-h] [-d DIM DIM]

    Test the polar grid.

    optional arguments:
        -h, --help
                          show this help message and exit.
        -r ROWS, --rows ROWS
                          the number of radial rows in the grid.
        -p POLES, --poles POLES
                          the number of cells at the pole.
                          If 0 or 1, there is a single pole cell.
        -s SPLIT, --split SPLIT
                          the splitting factor.
                          It is a value (at least 1) which is used to
                          determine the number of outward neighbors.

    The number of columns in each radial row is nondecreasing as
    the row number increases.  In a given radial row, except the last,
    each cell has at least one outward neighbor.  Each cell in every
    row beyond the first row, the row containing all cells at the pole,
    has exactly one inward neighbor.

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
from polar_grid import PolarGrid, InWinder
from maze import Maze
from wilson import Wilson
from maze_pillow import MazeSketcher
from distances import BellmanFord

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

    desc = 'Test the polar grid.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-r', '--rows', type=int, default=5,
        help='the number of radial rows in the grid')
    parser.add_argument('-p', '--poles', type=int, default=1,
        help='the number of cells at the pole')
    parser.add_argument('-s', '--split', type=float, default=1,
        help='the splitting factor')

    args = parser.parse_args()

    rows = args.rows
    poles = args.poles
    split = args.split
    
        # --------- TESTING STARTS HERE ----------
    print('Test 1) a polar grid')
    grid = PolarGrid(rows, poles, cell_ratio=split, wallbuilder=True)
    cell1 = grid[(0,0)]
    cell2 = grid[(1,0)]
    cell3 = grid[(1,1)]
    cell4 = grid[(2,0)]
    assert cell2['in'] == cell1
    assert cell1['out0'] == cell2
    cell1.color = 'green'
    cell2.color = 'blue'
    cell3.color = 'yellow'
    cell4.color = 'magenta'
    grid.set_edge_color(cell1, cell2, 'red')
    grid.set_edge_color(cell2, cell3, 'orange')
    grid.set_edge_color(cell4, cell2, 'cyan')
    maze = Maze(grid)
    #Wilson.on(maze)
    #chi = maze_characteristic(maze)
    #if maze.k == 1 and chi == 0:
    #    print('A perfect maze!')
    #else:
    #    print('Oops! Not a spanning tree!')
    sketcher = MazeSketcher(maze, title=f'polar grid ({poles}, {split})')
    maze.sketch()

    print('Test 2) Wilson\'s algorithm on a polar grid')
    grid = PolarGrid(rows, poles, cell_ratio=split)
    maze = Maze(grid)
    Wilson.on(maze)
    chi = maze_characteristic(maze)
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')
    start = grid[(rows-1, 0)]
    start.color = 'yellow'
    finish = grid[(0,0)]
    finish.color = 'red'
    sketcher = MazeSketcher(maze, title='Ariadne\'s map' + \
      f' (Wilson\'s algorithm on a polar grid)')
    maze.sketch()

    status = BellmanFord.on(maze, source=start)
    curr = finish
    dist = status[finish]
    r1, g1, b1 = 255, 255, 0      # start - yellow
    r2, g2, b2 = 255, 0, 0        # finish - red
    while curr != start:
        prev = status.predecessor(curr)
        d = status[curr]
        r = int((1-d/dist)*r1 + (d/dist)*r2)
        g = int((1-d/dist)*g1 + (d/dist)*g2)
        b = int((1-d/dist)*b1 + (d/dist)*b2)
        curr.color = '#%02x%02x%02x' % (r, g, b)
        grid.set_edge_color(curr, prev, curr.color)
        curr = prev
        # print(curr.color)
    sketcher = MazeSketcher(maze, title='Theseus\'s solution' + \
      f' (Wilson\'s algorithm on a polar grid)')
    maze.sketch()

    print('Test 3) Inward winder algorithm on a polar grid')
    grid = PolarGrid(rows, poles, cell_ratio=split)
    maze = Maze(grid)
    InWinder.on(maze, p=0.7)
    chi = maze_characteristic(maze)
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')
    start = grid[(rows-1, 0)]
    start.color = 'yellow'
    finish = grid[(0,0)]
    finish.color = 'red'
    sketcher = MazeSketcher(maze, title='Ariadne\'s map' + \
      f' (Inward Winder algorithm on a polar grid)')
    maze.sketch()

    print('Test 4) Outward winder algorithm on a polar grid')
    grid = PolarGrid(rows, poles, cell_ratio=split)
    maze = Maze(grid)
    InWinder.on(maze, p=0.7)
    chi = maze_characteristic(maze)
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')
    start = grid[(rows-1, 0)]
    start.color = 'yellow'
    finish = grid[(0,0)]
    finish.color = 'red'
    sketcher = MazeSketcher(maze, title='Ariadne\'s map' + \
      f' (Outward Winder algorithm on a polar grid)')
    maze.sketch()

# end of test_polar_grid.py
