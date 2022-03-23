"""test_petersen_maze.py - test the Petersen grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_Petersen_maze.py [-h] [-n n]

    Test the Petersen complete grid K(n).

    optional arguments:
        -h, --help
                          show this help message and exit
        -n N
                          the number of cells in either ring
                              (default: 5)

        -k k              the relative number of the neighbor in
                          the inner ring
                              (default: 2)

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
from petersen_grid import PetersenGrid
from maze import Maze
from wilson import Wilson
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'Test the Kuratowski complete grid K(n).'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', type=int, default=5,
        help='the number of cells in either ring')
    parser.add_argument('-k', type=int, default=2,
        help='the relative number of the inner ring neighbor')
    args = parser.parse_args()

    n, k = args.n, args.k

        # The grid will have n cells and 3n grid edges.

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          f'The Petersen grid G({n},{k})')
    grid = PetersenGrid(n, k, wall_builder=True, cell_radius=10)
    assert len(grid.cells) == 2*n
    assert len(grid[(0,0)].neighbors) == 3, \
        f'Cell 0 has {len(grid[(0,0)].neighbors)} neighbors'
    maze = Maze(grid)
    sketcher = MazeSketcher(maze, \
        title=f'The Petersen grid G({n},{k})')
    maze.sketch()

    print('Test 2)',
          f'Wilson\'s algorithm on the Petersen grid G({n},{k})')
    grid = PetersenGrid(n, k)
    assert len(grid.cells) == 2*n
    assert len(grid[(0,0)].neighbors) == 3, \
        f'Cell 0 has {len(grid[(0,0)].neighbors)} neighbors'
    maze = Maze(grid)
    Wilson.on(maze)
    sketcher = MazeSketcher(maze, \
        title=f'Wilson\'s algorithm on the Petersen grid G({n},{k})')
    maze.sketch()

    print('Success!')

# end of test_petersen_maze.py
