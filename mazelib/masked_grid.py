"""masked_grid.py - to hide parts of a grid
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class MaskedCell
    class MaskedGrid
    function make_mask

DESCRIPTION

    A mask allows us to apply algorithms to selected parts of a
    grid.  General algorithms (such as Wilson, Aldous/Broder, the
    recursive backtracker and related growing tree algorithms,
    and hunt and kill) will work well on masked mazes.  Algorithms
    taylored to a particular grid type will tend to fail, sometimes
    even crashing, when the grid is masked.

EXAMPLE

    Wilson's algorithm on a masked 5x7 rectangular grid
    Cell (2,3) in the middle of the grid is hidden

        +---+---+---+---+---+---+---+
        |   |   |                   |
        +   +   +---+---+   +   +---+
        |       |       |   |       |
        +   +   +   +---+   +---+---+
        |   |       | H |           |
        +---+   +---+---+   +---+   +
        |                       |   |
        +   +---+---+   +---+   +---+
        |           |       |       |
        +---+---+---+---+---+---+---+

                Maze characteristic:
                       number of nodes:         v = 35
                       number of edges:         e = 33
                  number of components:         k = 2
                  Euler characteristic: v - e - k = 0

    On the visible portion of the grid is a spanning tree, as
        v = 34 (since cell H is invisible)
        e = 33 (since there are no passages entering or leaving cell H)
        k = 1 (since H is an isolated cell and H is invisible)
    The visible part is connected and also, since v-e=1, forms a tree.

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

from cell import Cell
from grid import Grid, RectangularGrid

class MaskedCell(Cell):
    """hiding parts of the cell information"""

    def __init__(self, index, grid, cell, *args, **kwargs):
        """constructor"""
        super().__init__(*args, **kwargs)
        self._index = index
        self._grid = grid
        self._cell = cell

    @property
    def parent(self):
        """return the grid"""
        return self._grid

    @property
    def child(self):
        """return the cell"""
        return self._cell

    @property
    def index(self):
        """return the index"""
        return self._index

        # The Neighborhood
        #   Masking hides parts of the grid topology.  We do not
        #   allow the mask to change the grid topology.  All we
        #   allow is for the mask to make certain neighbors
        #   invisible.

    def __getitem__(self, direction):
        """retrieve the neighbor in the indicated direction

        Invisible neighbors are hidden from this view.
        """
        nbr = self.child[direction]
        if not nbr:
            return None
        index = nbr.index
        masked_nbr = self.parent[index]
        if masked_nbr:
            return masked_nbr
        return None

    def __setitem__(self, direction, cell):
        """set the neighbor in the indicated direction

        We do not permit the mask to change the grid topology.
        """
        raise NotImplementedError('__setitem__ illegal for for masks')

    @property
    def directions(self):
        """the directions in which neighbors can be found

        Invisible neighbors are hidden from this view.
        """
        directions = self.child.directions
        new_directions = []
        for direction in directions:
            nbr = self.child[direction]
            index = nbr.index
            masked_nbr = self.parent[index]
            if masked_nbr:
                new_directions.append(direction)
        return new_directions

    @property
    def neighbors(self):
        """the cell's neighbors

        Invisible neighbors are hidden from this view.
        """
        directions = self.child.directions
        neighbors = []
        for direction in directions:
            nbr = self.child[direction]
            index = nbr.index
            masked_nbr = self.parent[index]
            if masked_nbr:
                neighbors.append(masked_nbr)
        return neighbors

        # Link information is not hidden except in the passages
        # property.

    def weight(self, cell):
        """return the weight of a link"""
        return self.child._passages[cell.child]

    def linkto(self, cell, weight=1):
        """carve a directed link to another cell"""
        if cell:
            self.child._passages[cell.child] = weight

    def isLinkedTo(self, cell):
        """is there a link?"""
        return cell.child in self.child._passages

    def unlinkto(self, cell):
        """remove a one-way passage"""
        if cell.child in self.child._passages:
            del self.child_passages[cell.child]

    @property
    def passages(self):
        """return a list of exits to neighboring cells

        Here we hide any invisible neighbors from view.
        """
        passages = self.child.passages
        new_passages = []
        for cell in passages:
            index = cell.index
            masked_nbr = self.parent[index]
            if masked_nbr:
                new_passages.append(masked_nbr)
        return new_passages

class MaskedGrid(Grid):
    """hiding parts of a grid"""

    def initialize(self):
        """initialization

        Only a small amount of topological information is available
        at this level.  Basically we can either hide or expose a cell,
        and we can use basic grid and cell properties to query a
        cell that is visible.

        KEYWORD ARGUMENTS (from constructor)

            grid - the grid being masked
        """
        self.grid = grid = self._args[0]
        if not isinstance(grid, Grid):
            raise TypeError('Missing grid argument')

        for cell in grid.each_cell():
            index = cell.index
            masked_cell = MaskedCell(index, self, cell)
            self[index] = masked_cell
        self.hidden = {}

    def hide(self, masked_cell):
        """hide a cell from view"""
        index = masked_cell.index
        if self[index]:
            self[index] = None
            self.hidden[index] = masked_cell

    def expose(self, masked_cell):
        """expose a cell to make it visible"""
        index = masked_cell.index
        if self.hidden.get(masked_cell):
            del self.hidden[masked_cell]
            self[index] = masked_cell

def make_mask(filename, GridType=RectangularGrid):
    """create a rectangular grid and a mask using a text file

    ARGUMENTS

        filename - a text file which gives a representation of the
            grid and the mask
                'X' or 'x' - represent a visible cell
                other characters - represent a hidden cell

    RETURNS

        a rectangular grid and a masked grid
            the dimensions of the rectangular grid will be
            the number of lines by the number of characters in
            the longest line. 
    """
    rows = 0
    columns = 0
    lines = []
    with open(filename, 'r') as fp:
        for line in fp:
            lines.append(line[:-1])
            rows += 1
            columns = max(columns, len(line)-1)

    print(f'make_mask: {rows} rows and {columns} columns in grid')
    if rows < 1 or columns < 1:
        raise ValueError(f'{filename} has no data')

    grid = GridType(rows, columns)
    masked_grid = MaskedGrid(grid)
    for i in range(rows):
        for j in range(columns):
            line = lines[rows - i - 1]
            if j >= len(line) or not line[j] in ['x', 'X']:
                cell = masked_grid[(i, j)]
                masked_grid.hide(cell)

    return grid, masked_grid

# end of masked_grid.py
