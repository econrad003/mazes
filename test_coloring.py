"""test_coloring.py - test the map coloring methods
Copyright 2022 by Eric Conrad

USAGE

    usage: test_coloring.py [-h] [-d DIM DIM]

    Test the map coloring methods.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the toroidal grid

    (Testing is done on a toroidal grid.)

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
import coloring
from maze_pillow import MazeSketcher
from maze_support import Queue

if __name__ == '__main__':
    import argparse

    desc = 'Test the map coloring methods.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(15, 20),
        help='the dimensions of the toroidal grid')
    args = parser.parse_args()

    rows, cols = args.dim
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo',
              'violet']

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'Simple greedy coloring using depth-first search')
    grid = TorusGrid(rows, cols, cell_width=21, cell_height=21)
    maze = Maze(grid)
    Wilson.on(maze)

            # The maze is a spanning tree so the chromatic
            # number is 2.
    colormap, n = coloring.GreedyColoring.on(maze)
    print(f'Two colors are required, {n} colors were used.')

    assert coloring.validColoring(colormap)
    coloring.applyPaint(colormap, colors)

    sketcher = MazeSketcher(maze, \
        title=f'DFS Greedy coloring, 2 colors required, {n} used')
    maze.sketch()

    print('Test 2)',
          'Simple greedy coloring using breadth-first search')
    grid = TorusGrid(rows, cols, cell_width=21, cell_height=21)
    maze = Maze(grid)
    Wilson.on(maze)

            # The maze is a spanning tree so the chromatic
            # number is 2.
    colormap, n = coloring.GreedyColoring.on(maze, queuing=Queue())
    print(f'Two colors are required, {n} colors were used.')

    assert coloring.validColoring(colormap)
    coloring.applyPaint(colormap, colors)

    sketcher = MazeSketcher(maze, \
        title=f'BFS Greedy coloring, 2 colors required, {n} used')
    maze.sketch()

    print('Test 3)',
          'Tree coloring using distances')
    grid = TorusGrid(rows, cols, cell_width=21, cell_height=21)
    maze = Maze(grid)
    Wilson.on(maze)

            # The maze is a spanning tree so the chromatic
            # number is 2.
    colormap, n = coloring.TreeColor.on(maze)
    print(f'Two colors are required, {n} colors were used.')

    assert coloring.validColoring(colormap)
    coloring.applyPaint(colormap, colors)

    sketcher = MazeSketcher(maze, \
        title=f'Tree coloring, 2 colors required, {n} used')
    maze.sketch()

    print('Test 4)',
          'Welsh/Powell coloring')
    grid = TorusGrid(rows, cols, cell_width=21, cell_height=21)
    maze = Maze(grid)
    Wilson.on(maze)

            # The maze is a spanning tree so the chromatic
            # number is 2.
    colormap, n = coloring.WelshPowell.on(maze)
    print(f'Two colors are required, {n} colors were used.')

    assert coloring.validColoring(colormap)
    coloring.applyPaint(colormap, colors)

    sketcher = MazeSketcher(maze, \
        title=f'Welsh/Powell coloring, 2 colors required, {n} used')
    maze.sketch()

    print('Success!')
# end of test_wilson.py
