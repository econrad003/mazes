"""binary_tree.py - implementation of a lazy binary tree algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    This particular binary tree algorithm is designed exclusively
    for the rectangular grid. It may work on a few other grids, but
    it is guaranteed on a rectangular grid.

    Suppose we have an m*n rectangular grid. Stationed on each cell
    is a worker with a coin and a pickaxe.  A bell sounds and each
    worker flips his coin.  If it comes up heads, he carves a passage
    east; if tails, north.  Workers on the eastern frontier cannot
    cut eastward passages, no they carve northward passages.  Similarly
    workers on the northern frontier cut eastward passages.  The worker
    on the northeast cell simply takes a break and smokes a cigarette.

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

from random import random

class BinaryTree(object):
    """BinaryTree - implementation of a binary tree passage carver

    EXAMPLE

        +---+---+---+---+---+---+---+---+---+---+
        |                                       |
        +   +---+   +   +---+---+---+   +   +   +
        |   |       |   |               |   |   |
        +---+   +---+   +---+---+   +---+---+   +
        |       |       |           |           |
        +   +---+   +---+   +---+---+   +   +   +
        |   |       |       |           |   |   |
        +---+   +   +---+---+   +   +   +   +   +
        |       |   |           |   |   |   |   |
        +---+   +---+   +   +---+---+---+---+   +
        |       |       |   |                   |
        +---+---+---+---+---+---+---+---+---+---+
        Maze characteristic:
               number of nodes:         v = 60
               number of edges:         e = 59
          number of components:         k = 1
          Euler characteristic: v - e - k = 0    
"""

    @classmethod
    def on(cls, maze, directions=('east', 'north'), p=0.5):
        """carve a binary tree on a rectangular grid"""
        east, north = directions
        for cell in maze.grid.each_cell():
            nbr_east = cell[east]
            nbr_north = cell[north]

            if nbr_east and nbr_north:
                    # flip a coin and carve accordingly
                rand = random()     # heads with probability p
                nbr = nbr_east if rand < p else nbr_north
                cell.link(nbr)
                continue

            if nbr_north:
                    # carve northward
                cell.link(nbr_north)
                continue

            if nbr_east:
                    # carve eastward
                cell.link(nbr_east)
        return maze

# end of binary_tree.py
