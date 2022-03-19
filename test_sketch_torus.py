"""test_sketch_torus.py - test sketching toroidal mazes
Copyright 2022 by Eric Conrad

USAGE

    usage: test_sketch_torus.py [-h] [-d DIM DIM]

    Try sketching some toroidal mazes.

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
from torus_grid import TorusGrid
from maze import Maze
from wilson import Wilson
from recursive_backtracker import DFSSpanningTree
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'Try sketching some toroidal mazes.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(12, 25),
        help='the dimensions of the grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------

    print('Test 1) A uniformly random spanning tree')
    grid = TorusGrid(rows, cols, cell_width=25, cell_height=25)
    maze = Maze(grid)
    Wilson.on(maze)
    sketcher = MazeSketcher(maze, \
        title='Wilson\'s Algorithm on a torus')
    maze.sketch()

    print('Test 2) A depth-first search spanning tree')
    grid = TorusGrid(rows, cols, cell_width=25, cell_height=25)
    maze = Maze(grid)
    Wilson.on(maze)
    sketcher = MazeSketcher(maze, \
        title='Recursive Backtracker (DFS) on a torus')
    maze.sketch()

# end of test_sketch_cylinder.py
