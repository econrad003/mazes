"""test_bellman_ford.py - test the Bellman/Ford shortest path
    implementation
Copyright 2022 by Eric Conrad

USAGE

    usage: test_bellman_ford.py [-h] [-d DIM DIM]

    Test the implementation of the Bellman/Ford shortest path algorithm.

    optional arguments:
        -h, --help
                          show this help message and exit
        -d DIM DIM, --dim DIM DIM
                          the dimensions of the Moebius grid

    (Testing is done on a Moebius strip grid.)

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
from maze_pillow import MazeSketcher
from distances import BellmanFord

if __name__ == '__main__':
    import argparse

    desc = 'Test the implementation of the Bellman/Ford' + \
        ' shortest path algorithm.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', type=int, nargs=2,
        default=(15, 25),
        help='the dimensions of the Moebius grid')
    args = parser.parse_args()

    rows, cols = args.dim

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          'Bellman/Ford on a rectangular maze')
    grid = RectangularGrid(rows, cols, cell_width=25, cell_height=25)
    maze = Maze(grid)
    Wilson.on(maze)
    source = grid[(0, 0)]
    source.color = "red"
    target = grid[(rows-1, cols-1)]
    target.color = "green"
    status = BellmanFord.on(maze, source=source)
    assert status[source] == 0
    print('distance to target:', status[target])
    curr = target
    while True:
        prev = status.predecessor(curr)
        if prev == source:
            break
        prev.color = "coral"
        curr = prev
    sketcher = MazeSketcher(maze, \
        title=f'Bellman/Ford shortest path (length: {status[target]})')
    maze.sketch()

    print('Test 2)',
          'For documentation')
    grid = RectangularGrid(6, 10)
    maze = Maze(grid)
    Wilson.on(maze)
    source = grid[(0, 0)]
    source.text = "S"
    target = grid[(5, 9)]
    target.text = "T"
    status = BellmanFord.on(maze, source=source)
    assert status[source] == 0
    print('distance to target:', status[target])
    curr = target
    while True:
        prev = status.predecessor(curr)
        if prev == source:
            break
        prev.text = "*"
        curr = prev
    print(maze)

# end of test_bellman_ford.py
