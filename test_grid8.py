"""test_grid8.py - test the 8-connected rectangular grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_grid8.py [-h] [-d DIM DIM]

    Test the 8-connected rectangular grid.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the grid

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
from grid8 import Rectangular8Grid
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

    desc = 'Test the 8-connected rectangular grid.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(12, 15),
        help='the dimensions of the rectangular grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'Wilson\'s algorithm on an 8-connected rectangular grid')
    grid = Rectangular8Grid(rows, cols)
    maze = Maze(grid)
    Wilson.on(maze)
    chi = maze_characteristic(maze)
    if maze.k > 1:
        print('There are some isolated cells in the maze.')
    if maze.k == 1 and chi == 0:
        print('A perfect maze!')
    else:
        print('Oops! Not a spanning tree!')

    status = BellmanFord.on(maze, source=grid[(0,0)])
    max_dist = 0
    farthest = grid[(0,0)]
    for cell in grid.each_cell():
        if status[cell] > max_dist:
            farthest = cell
            max_dist = status[cell]
    print(f'farthest from lower left: {farthest.index} ' + \
        f'distance={max_dist}')

    status = BellmanFord.on(maze, source=farthest)
    max_dist = 0
    farthest2 = farthest
    for cell in grid.each_cell():
        if status[cell] > max_dist:
            farthest2 = cell
            max_dist = status[cell]
    print(f'farthest from {farthest}: {farthest2.index} ' + \
        f'distance={max_dist}')

    status = BellmanFord.on(maze, source=farthest2)
    max_dist = 0
    farthest3 = farthest2
    for cell in grid.each_cell():
        if status[cell] > max_dist:
            farthest3 = cell
            max_dist = status[cell]
    print(f'farthest from {farthest2}: {farthest3.index} ' + \
        f'distance={max_dist}')

    for cell in grid.each_cell():
        dist = status[cell]
        r = int(200 * (1 - dist/max_dist))
        g = int(175 * dist/max_dist)
        b = min(r, g)
        rgb = '#%02x%02x%02x' % (r, g, b)
        cell.color = rgb

    farthest3.color = "#00ff00"
    farthest2.color = "#ff0000"

    sketcher = MazeSketcher(maze, \
        title='Wilson\'s algorithm on an 8-connected rectangular grid')
    maze.sketch()

# end of test_grid8.py
