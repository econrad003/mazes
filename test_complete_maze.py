"""test_complete_maze.py - test the Kuratowski complete grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_complete_maze.py [-h] [-n n]

    Test the Kuratowski complete grid K(n).

    optional arguments:
        -h, --help
                          show this help message and exit
        -n N
                          the number of cells

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
from kuratowski_grid import CompleteGrid
from maze import Maze
from wilson import Wilson
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'Test the Kuratowski complete grid K(n).'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', type=int, default=10,
        help='the number of cells')
    args = parser.parse_args()

    n = args.n

        # The grid will have n cells and n(n-1)/2 grid edges.
        # For the default n=10, n(n-1)/2=45.

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          f'The complete grid K({n})')
    grid = CompleteGrid(n, wall_builder=True, cell_radius=10)
    assert len(grid.cells) == n
    assert len(grid[0].neighbors) == n-1, \
        f'Cell 0 has {len(grid[0].neighbors)} neighbors'
    maze = Maze(grid)
    sketcher = MazeSketcher(maze, \
        title=f'The complete grid K({n})')
    maze.sketch()

    print('Test 2)',
          f'Wilson\'s algorithm on the complete grid K({n})')
#    kwargs = {}
#    grid = CompleteGrid(n, **kwargs)
    grid = CompleteGrid(n)
    assert len(grid.cells) == n
    assert len(grid[0].neighbors) == n-1, \
        f'Cell 0 has {len(grid[0].neighbors)} neighbors'
    maze = Maze(grid)
    Wilson.on(maze)
    sketcher = MazeSketcher(maze, \
        title=f'Wilson\'s algorithm on the complete grid K({n})')
    maze.sketch()

    print('Success!')

# end of test_complete_maze.py
