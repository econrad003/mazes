"""sidewinder.py - implementation of the sidewinder algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    This particular perfect maze (spanning tree) algorithm is designed
    exclusively for the rectangular grid. It may work on a few other
    grids, but it is guaranteed on a rectangular grid.

    Suppose we have an m*n rectangular grid. Stationed at the beginning
    of each row is a worker.  The worker flips a coin.  If it comes up
    with a head, the worker carves a passage eastward, and repeats the
    process.  If it comes up with its tail side, the worker picks a
    random cell in the current run and carves a northward passage or
    rise.  The worker is then transported to the cell after the run.
    On reaching the end of the row, he carves a rise somewhere in this
    last run.  Afterwards he takes a break and smokes a cigarette.

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

from random import random, choice

class Sidewinder(object):
    """Sidewinder - the sidewinder maze passage carver

    EXAMPLE

        spanning tree using the sidewinder algorithm
    +---+---+---+---+---+---+---+---+---+---+
    |                                       |
    +   +---+---+---+   +   +   +---+---+   +
    |       |           |   |       |       |
    +   +---+---+---+   +---+   +   +---+   +
    |   |                   |   |       |   |
    +   +---+---+   +   +   +---+---+   +   +
    |           |   |   |   |           |   |
    +   +---+   +   +   +---+---+---+---+   +
    |       |   |   |                   |   |
    +---+   +   +---+   +---+---+---+   +   +
    |       |       |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+
        Maze characteristic:
               number of nodes:         v = 60
               number of edges:         e = 59
          number of components:         k = 1
          Euler characteristic: v - e - k = 0
"""

    @classmethod
    def on(cls, maze, p=0.5):
        """carve a sidewinder tree on a rectangular grid"""
        east, north = 'east', 'north'
        grid = maze.grid
        for i in range(grid.rows-1):
            run = []
            for j in range(grid.cols-1):
                run.append(j)
                rand = random()       # the digger flips a coin
                if rand < p:              # heads it is!
                    cell = grid[(i,j)]
                    cell.link(cell[east])
                    continue
                k = choice(run)       # carve north somewhere
                cell = grid[(i,k)]
                cell.link(cell[north])
                run = []              # close the run

                # end of row
            j = grid.cols-1           # last cell in row
            run.append(j)
            k = choice(run)
            cell = grid[(i,k)]
            cell.link(cell[north])

        i = grid.rows - 1
        for j in range(grid.cols-1):
            cell = grid[(i, j)]
            cell.link(cell[east])

        return maze

# end of binary_tree.py
