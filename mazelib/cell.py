"""cell.py - implementation of the Cell class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class Cell
    class SquareCell

DESCRIPTION

    A cell is both a face in a grid and a vertex in a maze.  A base
    class Cell is provided largely as a stub.  The SquareCell class,
    derived from the basic Cell class and also provided in this module,
    is a good starting point for rectangular mazes.

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

class Cell(object):
    """Cell - implementation of a simple cell class

    DESCRIPTION

        A cell is the repository for the information about the grid
        and or maze that contains it.  It is part of several graphs:

            1) The grid is an embedding of a graph on a manifold,
               typically a surface such as a plane, a cylinder, a
               torus, or a Moebius strip.  The vertices of the
               grid are the facial corners or nodes of the grid. The
               walls that bound the cell are the edges of the grid.
               The faces of the grid are the cells themselves.

               If the manifold is unbounded, then the grid has one
               additional face which is not a cell, namely the
               unbounded region or "the unknown".

            2) The dual grid is a graph where the cells are vertices
               and the walls separating the cells are the edges.

            3) The maze is a subgraph of the dual grid consisting of
               the cells of the grid as vertices and a subset of the
               walls, namely the passages, as edges.

            4) The complementary maze is a subgraph of the dual grid
               consisting of the cells of the grid as vertices and a
               subset of the walls, namely those which are not passages,
               as edges.
    """

    def __init__(self, *args, **kwargs):
        """constructor

        OPTIONAL ARGUMENTS

            Reserved for subclasses

        KEYWORD ARGUMENTS

            Reserved for subclasses

        DATA ITEMS

            _nodes - list of facial corners - set by the grid
            _walls - dictionary of facial edges - set by the grid
                          direction : (node1, node2)
            _neighbors - dictionary of neighbors - set by the grid
                          direction : cell
            _passages - dictionary of passages - maintained by various
                algorithms
                          cell : weight
            text - a single character - for string representation of a
                maze
            color - an RGB value or None for the face color in an image
                representation of the maze
            _args - passed optional arguments
            _kwargs - passed keyword arguments
        """
        self._nodes = set([])         # facial corners
        self._walls = {}              # facial edges
        self._neighbors = {}          # neighboring cells
        self._passages = {}           # the incident passages
        self.text = ' '
        self.color = None

        self._args = args
        self._kwargs = kwargs

        self.initialize()             # subclass initialization

    def initialize(self):
        """stub - for subclasses"""
        pass

        # vertices (the bounding nodes)

    @property
    def nodes(self):
        """return the list of nodes"""
        return list(self._nodes)

    def set_node(self, node):
        """add a node"""
        self._nodes.add(node)

    def remove_node(self, node):
        """discard a node"""
        self._nodes.discard(node)

        # edges (the bounding walls)

    @property
    def walls(self):
        """return the dictionary of walls"""
        return self._walls.copy()

    def get_wall(self, direction):
        """return the wall in the given direction

        EXCEPTIONS

            KeyError if there is no wall in the indicated direction.
        """
        return self._walls[direction]

    def set_wall(self, direction, wall):
        """add a wall"""
        self._walls[direction] = wall

        # faces (the cells themselves)

    def __getitem__(self, direction):
        """return a neighbor

        RETURNS

            a cell (if the indicated wall is an internal wall) or None
            (if the indicated wall is a boundary wall)
        """
        return self._neighbors.get(direction)

    def __setitem__(self, direction, cell):
        """assign a neighbor"""
        if cell:
            self._neighbors[direction] = cell
        elif direction in self._neighbors:
            del self._neighbors[direction]
        return cell

        # the neighborhood

    @property
    def directions(self):
        """the directions in which neighbors can be found"""
        return list(self._neighbors.keys())

    @property
    def neighbors(self):
        """the cell's neighbors"""
        return list(self._neighbors.values())

        # passages of the maze

    def weight(self, cell):
        """return the weight of a link"""
        return self._passages[cell]

    def linkto(self, cell, weight=1):
        """carve a directed link to another cell"""
        if cell:
            self._passages[cell] = weight

    def link(self, cell, weight=1):
        """carve an undirected link with another cell"""
        self.linkto(cell, weight)
        cell.linkto(self, weight)

    def isLinkedTo(self, cell):
        """is there a link?"""
        return cell in self._passages

    def unlinkto(self, cell):
        """remove a one-way passage"""
        if cell in self._passages:
            del self._passages[cell]

    def unlink(self, cell):
        """remove any passage with the cell"""
        self.unlinkto(cell)
        cell.unlinkto(self)

    @property
    def passages(self):
        """return a list of exits to neighboring cells"""
        return list(self._passages.keys())

class SquareCell(Cell):
    """a simple square cell"""

    def initialize(self):
        """initialization

        USAGE

            SquareCell(x=COLUMN, y=ROW, nodes=NODES, walls=WALLS)

        KEY ARGUMENTS

            x - the column number (or abscissa for southwest corner)
            y - the row number (or ordinate for southwest corner)
        """
        self.x = self._kwargs['x']
        self.y = self._kwargs['y']
        self.index = (self.y, self.x)   # row, column

    def __str__(self):
        """primarily for testing"""
        return 'Cell(' + str(self.y) + ',' + str(self.x) + ')'

# end of cell.py
