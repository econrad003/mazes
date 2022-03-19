"""cocktail_shaker_tree.py - another binary tree algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    This particular binary tree algorithm is designed exclusively
    for the rectangular grid. It may work on a few other grids, but
    it is guaranteed on a rectangular grid.

    Suppose we have an m*n rectangular grid. Stationed on each cell
    is a worker with a coin and a pickaxe.  A bell sounds and each
    worker flips his coin.  If it comes up heads, he carves a passage
    east or west depending on whether the row is even or odd; if tails,
    north.  Workers on the frontier who cannot carve the required east
    or west passage must instead carve northward, if possible. Workers
    on the northern frontier must similarly carve an east or west
    passage (with direction depending on the row number).
    cut eastward passages, no they carve northward passages. The worker
    on the tail end of the northmost row cell simply takes a break and
    smokes a cigarette.

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

class CocktailShakerTree(object):
    """CocktailShakerTree - implementation of a binary tree passage
        carver

    EXAMPLE

        +---+---+---+---+---+---+---+---+---+---+
        |                                       |
        +   +---+---+   +---+---+---+---+   +---+
        |           |                   |       |
        +   +---+---+---+---+---+   +---+---+   +
        |   |                       |           |
        +   +---+   +---+   +   +   +---+---+---+
        |       |       |   |   |               |
        +---+---+   +---+---+   +---+---+   +   +
        |           |           |           |   |
        +   +---+---+---+---+   +---+---+   +   +
        |                   |           |   |   |
        +---+---+---+---+---+---+---+---+---+---+
          Maze characteristic:
                 number of nodes:         v = 60
                 number of edges:         e = 59
            number of components:         k = 1
            Euler characteristic: v - e - k = 0
    """

    @classmethod
    def on(cls, maze, p=0.5):
        """carve a cocktail shaker tree on a rectangular grid"""
        east, west, north = 'east', 'west', 'north'
        grid = maze.grid
        for i in range(grid.rows):
            for j in range(grid.cols):
                cell = grid[(i, j)]
                nbr_side = cell[east] if i % 2 else cell[west]
                nbr_north = cell[north]

                if nbr_side and nbr_north:
                        # flip a coin and carve accordingly
                    rand = random()     # heads with probability p
                    nbr = nbr_side if rand < p else nbr_north
                    cell.link(nbr)
                    continue

                if nbr_north:
                        # carve northward
                    cell.link(nbr_north)
                    continue

                if nbr_side:
                        # carve eastward
                    cell.link(nbr_side)

        return maze

# end of cocktail_shaker_tree.py
