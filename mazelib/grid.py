"""grid.py - implementation of the Grid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class Grid
    class RectangularGrid

DESCRIPTION

    The grid maintains topology and homology of the maze, that is,
    the vertices, edges and faces which are embedded on a plane, a
    a torus, or some other manifold.

    The Grid class that is implemented here is basically a stub.
    Derived from this is the RectangularGrid class, also provided
    in this module.

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

MODIFICATIONS

    28 March 2022 - EC - added edge colors to grid
"""

from math import floor
from cell import Cell, SquareCell

class Grid(object):
    """Grid - implementation of a grid base class"""

    WALLBUILDER = 'wall_builder'
    DEFAULT_COLOR = 'white'

        # initialization

    def __init__(self, *args, **kwargs):
        """constructor

        OPTIONAL ARGUMENTS

            Reserved for subclasses

        KEYWORD ARGUMENTS

            wall_builder - configure the grid as a wall builder instead
                of a passage carver if this is true

        DATA ITEMS

            _nodes - dictionary of facial corners - set by the grid
            _walls - dictionary of facial edges - set by the grid
                          {node1, node2} : [cell1, cell2]
            _neighbors - dictionary of neighbors - set by the grid
                          direction : cell
            _passages - dictionary of passages - maintained by various
                algorithms
                          cell : weight
        """
        self._nodes = {}
        self._walls = {}
        self._cells = {}
        self._trace = []
        self._edge_colors = {}

        self._args = args
        self._kwargs = kwargs

        self.initialize()
        self.configure()

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    @property
    def nodes(self):
        """return a list of nodes"""
        return list(self._nodes.values())

    @property
    def walls(self):
        """return a list of facial walls (edges)"""
        return list(self._walls.values())

    @property
    def cells(self):
        """return a list of cells"""
        return list(self._cells.values())

    @property
    def indices(self):
        """return a list of indices"""
        return list(self._cells.keys())

    def __getitem__(self, index):
        """return the cell with a given index (operator [])"""
        return self._cells.get(index)

    def __setitem__(self, index, cell):
        """associate a cell with an index (operator []=)"""
        if cell:
            self._cells[index] = cell
        elif index in self._cells:
            del self._cells[index]
        return cell

    def each_index(self):
        """generator for all the cell indices"""
        indices = self.indices
        for index in indices:
            yield index

    def each_cell(self):
        """generator for all the cells"""
        indices = self.indices
        for index in indices:
            yield self[index]

    def set_edge_color(self, cell1, cell2, color):
        """set the color to be used for an edge"""
        edge = frozenset([cell1, cell2])
        self._edge_colors[edge] = color

    def edge_color(self, cell1, cell2):
        """set the color to be used for an edge"""
        edge = frozenset([cell1, cell2])
        color = self._edge_colors.get(edge)
        return color if color else self.DEFAULT_COLOR

    def clone(self, warning=True):
        """make a copy of the grid

        NOTE

            Derived classes that alter the grid layout after
            construction will need to overload this method!

        BUGS

            We assume here that the vertices, edges, and faces of the
            grid are established at the time the grid is constructed.
            The maze structure may have changed, that is, passages may
            have been carved or closed off.
        """
        print('WARNING: Clone uses only the maze DNA.')
        print('WARNING: Nodes/edges/faces are as fixed at time of',
              'construction.')
        print('INFO: Passages will be carved or removed as needed.')
        GridClass = self.__class__
        args = self._args
        kwargs = self._kwargs

            # call the constructor
        other = GridClass(*args, **kwargs)

        for index in self.indices:
            cell1 = self[index]
            cell2 = other[index]
            if not cell2:
                raise ValueError('A cell is missing.')
            cell2.text = cell1.text
            cell2.color = cell1.color
            for direction in cell1.directions:
                    # we do not need to check whether
                    # links exist in the copy -- the linking
                    # and unlinking methods take care of this
                    # in a transparent fashion.
                nbr1 = cell1[direction]
                nbr2 = cell2[direction]
                if cell1.isLinkedTo(nbr1):
                    wgt = cell1.weight(nbr1)
                    cell2.linkto(nbr2, weight=wgt)
                else:
                    cell2.unlinkto(cell2)
        return other

    @property
    def components(self):
        """returns the set of grid components

        The grid components are each sets of nodes or grid vertices.

        Use Maze.components to find the connectivity for faces (cells). 
        """
        bag = {}          # principal node : component of node
        nodes = {}        # node : principal node

            # housekeeping
            #   The initial assumption is that the grid is discrete,
            #   that is, each node is in a component by itself.
        for node in self.nodes:
            bag[node] = set([node])
            nodes[node] = node

            # main loop
            #   We search to find the components
        for edge in self._walls.keys():
            if len(edge) != 2:
                continue        # edge is a loop
            node1, node2 = list(edge)

            label1, label2 = nodes[node1], nodes[node2]
            if label1 == label2:
                continue        # same component

            component2 = bag[label2]    # merge into component 1
            for node in component2:
                bag[label1].add(node)
                nodes[node] = label1

            del bag[label2]

            # housecleaning
            #   Just return the components
        return list(bag.values())

        # Euler characteristic

    @property
    def v(self):
        """number of nodes"""
        return len(self._nodes)

    @property
    def e(self):
        """number of edges"""
        return len(self._walls)

    @property
    def f(self):
        """number of faces"""
        return len(self._cells)

    @property
    def k(self):
        """number of grid components"""
        return len(self.components)

    @property
    def Euler_chi(self):
        """Euler characteristic"""
        return self.v - self.e + self.f - self.k

    def sketch(self, sketcher, filename=None, show=True):
        """filter for sketching"""
        raise NotImplementedError("Not implemented")

class RectangularGrid(Grid):
    """RectangularGrid - implementation of the basic 4-connected
        rectangular grid
    """

    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'

    class Node(object):
        """nodal point marker, used by the grid and by maze drawing
        routines"""

        def __init__(self, x, y):
            """constructor"""
            self.x = x
            self.y = y

    class Wall(object):
        """facial edge marker, used by the grid and by maze drawing
        routines"""

        def __init__(self, node1, node2):
            """constructor"""
            self.nodes = [node1, node2]

    def __init__(self, rows, cols, *args, **kwargs):
        """constructor

        REQUIRED ARGUMENTS

            rows, cols - the number of rows and of columns in the
                face array
        """
        self.rows = rows
        self.cols = cols

            # we pass the arguments to the base class
        super().__init__(rows, cols, *args, **kwargs)

    def initialize(self):
        """create the directories of available nodes and faces"""
        rows, cols = self.rows, self.cols
            # vertices or nodes
        for i in range(rows+1):       # ordinates or y values
            for j in range(cols+1):   # abscissae or x-values
                x, y = point = self.transform(j, i)
                self._nodes[point] = self.Node(x, y)

            # faces or cells
        for i in range(rows):         # ordinates or y values
            for j in range(cols):     # abscissae or x-values
                xvalue, yvalue = self.transform(j, i)
                cell = SquareCell(x=xvalue, y=yvalue)
                self[(i, j)] = cell

    def configure(self):
        """finish building the cells"""
        self.configure_walls()
        self.configure_neighborhood()
        if self._kwargs.get(self.WALLBUILDER):
            self.configure_passages()

    def configure_walls(self):
        """build the cell boundaries"""
        rows, cols = self.rows, self.cols
        for i in range(rows):         # ordinates or y values
            for j in range(cols):     # abscissae or x-values
                index = (i, j)
                cell = self[index]
                    # corner coordinates
                sw = self.transform(j, i)
                se = self.transform(j+1, i)
                ne = self.transform(j+1, i+1)
                nw = self.transform(j, i+1)
                    # corner nodes
                sw = self._nodes[sw]
                se = self._nodes[se]
                ne = self._nodes[ne]
                nw = self._nodes[nw]
                    # record the nodes in the cell
                cell.set_node(sw)
                cell.set_node(se)
                cell.set_node(ne)
                cell.set_node(nw)
                    # build the walls as needed
                southWall = self._build_wall(sw, se)
                eastWall = self._build_wall(se, ne)
                northWall = self._build_wall(ne, nw)
                westWall = self._build_wall(nw, sw)
                    # record the walls in the cell
                cell.set_wall(self.SOUTH, southWall)
                cell.set_wall(self.EAST, eastWall)
                cell.set_wall(self.NORTH, northWall)
                cell.set_wall(self.WEST, westWall)

    def configure_neighborhood(self):
        """identify the cell's neighbors"""
        rows, cols = self.rows, self.cols
        for i in range(rows):         # ordinates or y values
            for j in range(cols):     # abscissae or x-values
                index = (i, j)
                cell = self[index]
                    # neighboring face coordinates
                south = tuple(reversed(self.transform(j, i-1)))
                east = tuple(reversed(self.transform(j+1, i)))
                north = tuple(reversed(self.transform(j, i+1)))
                west = tuple(reversed(self.transform(j-1, i)))
                    # neighboring faces
                    # -----------------
                    # here we use fact that both Cell.__setitem__ and
                    # Grid.__getitem__ handle the value None in a
                    # reasonable way...
                cell[self.SOUTH] = self[south]
                cell[self.EAST] = self[east]
                cell[self.NORTH] = self[north]
                cell[self.WEST] = self[west]

    def configure_passages(self):
        """carve passages through all internal walls"""
        for cell in self.each_cell():
                # note that linkTo does not link with None
            cell.linkto(cell[self.SOUTH])
            cell.linkto(cell[self.EAST])
            cell.linkto(cell[self.NORTH])
            cell.linkto(cell[self.WEST])

    def _build_wall(self, node1, node2):
        """erect the facial walls

        the walls are undirected with respect to the nodes, so
        we must take care.
        """
        index = frozenset([node1, node2])
        if index in self._walls:
            return self._walls[index]
        wall = self.Wall(node1, node2)
        self._walls[index] = wall
        return wall

    def transform(self, x, y):
        """coordinate transformation

        For a rectangular grid, coordinates are not transformed.  This
        is a stub for derived classes (for example ToroidalGrid).

        If integers are input, integers should be output.  The modulus
        operation (%) preserves integer input, but the divide opration
        (/) does not.
        """
        return (x, y)

    def __getitem__(self, index):
        """fetch the indicated cell"""
        return self._cells.get(index)

    def __setitem__(self, index, cell):
        """associate a cell will an index, or dissociate it"""
        if cell:
            self._cells[index] = cell
        elif index in self._cells:
            del self._cells[index]
        return cell

    def _make_wall(self, i, cells, direction=None,
                   nodes=['+', '+', '+'],
                   walls=['   ', ' v ', ' ^ ', '---']):
        """helper for __str__ and unicode

        DESCRIPTION

            This helper method draws a horizontal wall.

        REQUIRED ARGUMENTS

            i - the row number

            cells - a list of cells in the row, ordered in column
                order from first to last

        KEYWORD ARGUMENTS

            direction - the direction to follow (default: 'north')

            corners - the characters used for the leftmost, middle
                and rightmost nodal points

            walls - the strings used for passages, entry passges,
                exit passages, and hard walls.
        """
        if not direction:
            direction = RectangularGrid.NORTH
        left, middle, right = nodes
        passage, entry, exit, wall = walls

        s = ''
        first = True
        for cell in cells:
            s += left if first else middle
            first = False
            nbr = cell[direction]
            if nbr:
                if cell.isLinkedTo(nbr):
                    if nbr.isLinkedTo(cell):
                        s += passage  # two-way passage
                    else:
                        s += exit     # exit-only passage
                else:
                    if nbr.isLinkedTo(cell):
                        s += entry    # entrance-only passage
                    else:
                        s += wall     # internal wall - no passage
            else:
                s += wall             # external wall
        s += right
        return s

    def _make_faces(self, i, cells, walls=[' ', '>', '<', '|']):
        """helper for __str__ and unicode

        DESCRIPTION

            This helper method draws a row of cellfaces and their
            vertical walls.

        REQUIRED ARGUMENTS

            i - the row number

            cells - a list of cells in the row, ordered in column
                order from first to last

        KEYWORD ARGUMENTS

            walls - the strings used for passages, entry passges,
                exit passages, and hard walls.
        """
        passage, entry, exit, wall = walls
        direction = RectangularGrid.WEST

        s = ''
        first = True
        for cell in cells:
            first = False
            nbr = cell[direction]
            if nbr:
                if cell.isLinkedTo(nbr):
                    if nbr.isLinkedTo(cell):
                        s += passage  # two-way passage
                    else:
                        s += exit     # exit-only passage
                else:
                    if nbr.isLinkedTo(cell):
                        s += entry    # entrance-only passage
                    else:
                        s += wall     # internal wall - no passage
            else:
                s += wall             # external wall
            s += ' ' + cell.text[0] + ' ' if cell.text else '   '

        cell = cells[-1]
        direction = RectangularGrid.EAST
        nbr = cell[direction]
        entry, exit = exit, entry
        if nbr:
            if cell.isLinkedTo(nbr):
                if nbr.isLinkedTo(cell):
                    s += passage  # two-way passage
                else:
                    s += exit     # exit-only passage
            else:
                if nbr.isLinkedTo(cell):
                    s += entry    # entrance-only passage
                else:
                    s += wall     # internal wall - no passage
        else:
            s += wall             # external wall
        return s

    def __str__(self):
        """string representation of the maze"""
            # assemble the string image, row by row
        s = ''
        for i in range(self.rows-1, -1, -1):
            row = self.row(i)
            s += self._make_wall(i, row) + '\n'
            s += self._make_faces(i, row) + '\n'
        row = self.row(0)
        s += self._make_wall(0, row, direction=self.SOUTH,
                             walls=['   ', ' ^ ', ' v ', '---'])

        return s

    def row(self, i, split=0, reverse=False):
        """the cells in the indicated row from west to east

        Returns a list of cells.

        The order of the cells can be modified using the 'split' and
        'reverse' keyword arguments.
        """
        cells = []
        for j in range(self.cols):
            cells.append(self[(i, j)])
        if split:
            cells = cells[split:] + cells[:split]
        if reverse:
            cells.reverse()
        return cells

    def column(self, j, split=0, reverse=False):
        """the cells in the indicated column from south to north

        Returns a list of cells.

        The order of the cells can be modified using the 'split' and
        'reverse' keyword arguments.
        """
        cells = []
        for i in range(self.rows):
            cells.append(self[(i, j)])
        if split:
            cells = cells[split:] + cells[:split]
        if reverse:
            cells.reverse()
        return cells

    def sketch_setup(self):
        """sketch parameter setup"""
        CELLSIZE = 50       # pixel dimensions of cell
        assert CELLSIZE > 10
        if not self._kwargs.get('cell_width'):
            self._kwargs['cell_width'] = CELLSIZE
        if not self._kwargs.get('cell_height'):
            self._kwargs['cell_height'] = CELLSIZE

        MARGIN = 5          # reserved part of window
        assert MARGIN > 1
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN

        INSET = 0.15        # corners of cells
        assert INSET > 0 and INSET < 0.36
        if not self._kwargs.get('inset'):
            self._kwargs['inset'] = INSET

    @property
    def sketch_width(self):
        return self.cols * self._kwargs['cell_width'] \
            + 2 * self._kwargs['hmargin']

    @property
    def sketch_height(self):
        return self.rows * self._kwargs['cell_height'] \
            + 2 * self._kwargs['vmargin']

    def sketch_cell(self, sketcher, cell, location, dim, inset):
        """sketch a single cell"""
        def doortype(cell, nbr):
            """door can be 0-wall, 1-exit or 2"""
            if not nbr:
                return 0      # external wall
            if nbr.isLinkedTo(cell):
                return 2      # entrance or 2-way
            if cell.isLinkedTo(nbr):
                return 1      # exit
            return 0          # internal wall

        x, y = location                 # SW corner of cell
        cwidth, cheight = dim           #
        hinset = floor(inset * cwidth)  # inset width
        vinset = floor(inset * cheight) # inset height

        east = doortype(cell, cell[self.EAST])
        north = doortype(cell, cell[self.NORTH])
        west = doortype(cell, cell[self.WEST])
        south = doortype(cell, cell[self.SOUTH])

        doors = []
        polygon = []

        x1, x2 = x+cwidth-hinset, x+cwidth
        y1, y2 = y+vinset, y+cheight-vinset
        if east:
            door = [(x1, y1), (x2, y1)]
            doors.append(door)
            door = [(x1, y2), (x2, y2)]
            doors.append(door)
            polygon += [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        else:
            door = [(x1, y1), (x1, y2)]
            doors.append(door)
            polygon += [(x1, y1), (x1, y2)]

        x1, x2 = x+cwidth-hinset, x+hinset
        y1, y2 = y+cheight-vinset, y+cheight
        if north:
            door = [(x1, y1), (x1, y2)]
            doors.append(door)
            door = [(x2, y2), (x2, y1)]
            doors.append(door)
            polygon += [(x1, y2), (x2, y2), (x2, y1)]
        else:
            door = [(x1, y1), (x2, y1)]
            doors.append(door)
            polygon += [(x2, y1)]

        x1, x2 = x+hinset, x
        y1, y2 = y+cheight-vinset, y+vinset
        if west:
            door = [(x1, y1), (x2, y1)]
            doors.append(door)
            door = [(x1, y2), (x2, y2)]
            doors.append(door)
            polygon += [(x2, y1), (x2, y2), (x1, y2)]
        else:
            door = [(x1, y1), (x1, y2)]
            doors.append(door)
            polygon += [(x1, y2)]

        x1, x2 = x+hinset, x+cwidth-hinset
        y1, y2 = y+vinset, y
        if south:
            door = [(x1, y1), (x1, y2)]
            doors.append(door)
            door = [(x2, y2), (x2, y1)]
            doors.append(door)
            polygon += [(x1, y2), (x2, y2)]
        else:
            door = [(x1, y1), (x2, y1)]
            doors.append(door)

        color = cell.color if cell.color else "white"
        sketcher.draw_polygon(polygon, color)
        sketcher.draw_line_segments(doors)

    def sketch(self, sketcher, filename=None, show=True):
        """filter for sketching"""
        self.sketch_setup()
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        inset = self._kwargs['inset']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

        sketcher.open(width=self.sketch_width,
                      height=self.sketch_height)

        self.sketch_prologue(sketcher)
        for cell in self.each_cell():
            y, x = cell.index
            u, v = x * cwidth + hmargin, y * cheight + vmargin
            self.sketch_cell(sketcher, cell, (u, v),
                             (cwidth, cheight), inset)
        self.sketch_epilogue(sketcher)

        sketcher.close(filename=filename, show=show)

    def sketch_prologue(self, sketcher):
        """prologue to sketching"""
        pass            # stub

    def sketch_epilogue(self, sketcher):
        """epilogue to sketching"""
        pass            # stub

# end of grid.py
