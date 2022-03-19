"""test_wilson.py - test the implementation of Wilson's algorithm
Copyright 2022 by Eric Conrad

USAGE

    usage: test_dead_end.py [-h] [-d DIM DIM]

    Test the dead end method and the removal algorithms.

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
from grid import RectangularGrid
from maze import Maze
from wilson import Wilson
from dead_end import DeadEnds, DeadEndRemoval
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'Test the dead end method and the removal algorithms.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(16, 25),
        help='the dimensions of the Moebius grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'dead ends on a uniformly random maze')
    grid = RectangularGrid(rows, cols, cell_width=25, cell_height=25)
    maze = Maze(grid)
    Wilson.on(maze)
    dead_ends = DeadEnds.on(maze)
    n = len(dead_ends)
    for cell in dead_ends:
        cell.text = 'X'
        cell.color = "red"
    MazeSketcher(maze, \
        title=f'1) uniform maze, n={n} dead ends marked in red')
    maze.sketch()

    print('Test 2)',
          'added passages to all dead ends')
    clone = maze.clone()
    DeadEndRemoval.on(clone)
    n = DeadEnds.count(clone)
    MazeSketcher(clone, \
        title=f'2) added passages to dead ends with p=1.0 (n={n})')
    clone.sketch()

    print('Test 3)',
          'added passages to dead ends, probability p=0.5')
    clone = maze.clone()
    DeadEndRemoval.on(clone, p=0.5)
    n = DeadEnds.count(clone)
    MazeSketcher(clone, \
        title=f'3) added passages to dead ends with p=0.5 (n={n})')
    clone.sketch()

    print('Test 4)',
          'N/S passages to dead ends, probability p=0.5')
    clone = maze.clone()
    DeadEndRemoval.on(clone, method=DeadEndRemoval.directed_passage,
                      p=0.5, directions=['north', 'south'])
    n = DeadEnds.count(clone)
    MazeSketcher(clone, \
        title=f'4) N/S passages to dead ends with p=0.5 (n={n})')
    clone.sketch()

    print('Test 5)',
          'roundabout passages to dead ends, probability p=0.5')
    clone = maze.clone()
    DeadEndRemoval.on(clone, method=DeadEndRemoval.roundabout,
                      p=0.5)
    n = DeadEnds.count(clone)
    MazeSketcher(clone, \
        title=f'5) roundabouts to dead ends with p=0.5 (n={n})')
    clone.sketch()

# end of test_wilson.py
