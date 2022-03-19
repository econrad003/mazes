"""grid8.py - higher order connectivity on rectangular grids
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class Rectangular8Grid - an 8-connected or 'octagonal' rectangular
        grid
    class Rectangular6Grid - a 6-connected or 'hexagonal' rectangular
        grid

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

from math import cos, sin, pi
from random import random
from cell import SquareCell
from grid import RectangularGrid

class Rectangular8Grid(RectangularGrid):
    """RectangularGrid - implementation of the basic 8-connected
        rectangular grid
    """
    NORTHEAST = 'northeast'
    NORTHWEST = 'northwest'
    SOUTHEAST = 'southeast'
    SOUTHWEST = 'southwest'

    class Node8(RectangularGrid.Node):
        """nodal point marker, used by the grid and by maze drawing
            routines

        For the 8-connected rectangular grid, each corner of a square
        cell has two nodal points.  For example, the southwest corner
        of one cell joins p with the northeast corner of another cell
        like this:

                    +---x---x---+
                    |           |        LEGEND
                    x           x    + corner of square
                    |   cell 2  |    x node
            +---x---x---+       x
            |       | e |       |
            x       +---x---x---+
            |  cell 1   |
            x           x
            |           |
            +---x---x---+

        Note that the corner vertices are not nodes in the 8-connected
        grid as cells (faces) must meet along edges.  The edges here
        may be viewed either as the overlap (little square e in the
        illustration) or the diagonal connecting the shared nodes.

        Since cells are indexed by their southwest corner, we index the
        two nodes nearest a southwest corner, virtually extending the
        grid north and east one cell each way to get indices for the
        nodes along the north and east boundary walls.


                        |
                  0,0,0 +
                        |
                  0,0,1 x
                        |       0,0,3
                        +---x---x---
                      0,0   0,0,2

        The actual job of plotting this mess has some complications as
        corner edges may cross, requiring overpasses and underpasses.
        """

        def __init__(self, x, y, which):
            """constructor"""
            self.x = x
            self.y = y
            self.which = which

    def initialize(self):
        """create the directories of available nodes and faces"""
        rows, cols = self.rows, self.cols
        for i in range(rows):         # ordinates or y values
            for j in range(cols):   # abscissae or x-values
                    # southwest corner of cell
                x, y = self.transform(j, i)
                self._nodes[(x, y, 0)] = self.Node8(x, y, 0)
                self._nodes[(x, y, 1)] = self.Node8(x, y, 1)
                self._nodes[(x, y, 2)] = self.Node8(x, y, 2)
                self._nodes[(x, y, 3)] = self.Node8(x, y, 3)
        for j in range(cols):   # abscissae or x-values
                # populate the north wall
            x, y = self.transform(j, rows)
            self._nodes[(x, y, 2)] = self.Node8(x, y, 2)
            self._nodes[(x, y, 3)] = self.Node8(x, y, 3)
        for i in range(rows):         # ordinates or y values
                # populate the east wall
            x, y = self.transform(cols, i)
            self._nodes[(x, y, 0)] = self.Node8(x, y, 0)
            self._nodes[(x, y, 1)] = self.Node8(x, y, 1)

            # faces or cells
        for i in range(rows):         # ordinates or y values
            for j in range(cols):     # abscissae or x-values
                xvalue, yvalue = self.transform(j, i)
                cell = SquareCell(x=xvalue, y=yvalue)
                self[(i, j)] = cell

    def configure_walls(self):
        """build the cell boundaries"""
        rows, cols = self.rows, self.cols
        for i in range(rows):         # ordinates or y values
            for j in range(cols):     # abscissae or x-values
                index = (i, j)
                cell = self[index]
                x1, y1 = self.transform(j, i)   # sw corner
                x2, y2 = self.transform(j+1, i) # se corner
                x3, y3 = self.transform(j, i+1) # nw corner
                    # node coordinates
                ene = (x2, y2, 0)
                nne = (x3, y3, 3)
                nnw = (x3, y3, 2)
                wnw = (x1, y1, 0)
                wsw = (x1, y1, 1)
                ssw = (x1, y1, 2)
                sse = (x1, y1, 3)
                ese = (x2, y2, 1)
                    # corner nodes
                ene = self._nodes[ene]
                nne = self._nodes[nne]
                nnw = self._nodes[nnw]
                wnw = self._nodes[wnw]
                wsw = self._nodes[wsw]
                ssw = self._nodes[ssw]
                sse = self._nodes[sse]
                ese = self._nodes[ese]
                    # record the nodes in the cell
                cell.set_node(ene)
                cell.set_node(nne)
                cell.set_node(nnw)
                cell.set_node(wnw)
                cell.set_node(wsw)
                cell.set_node(ssw)
                cell.set_node(sse)
                cell.set_node(ese)
                    # assuming this is not a cylinder with just 1 column
                    # or a torus with with either 1 row or 1 column, we
                    # should have 8 nodes.
                if not self._kwargs.get('suppress_node_check', False):
                    assert len(cell.nodes) == 8

                    # build the walls as needed
                southWall = self._build_wall(ssw, sse)
                eastWall = self._build_wall(ese, ene)
                northWall = self._build_wall(nne, nnw)
                westWall = self._build_wall(wnw, wsw)
                southeastWall = self._build_wall(sse, ese)
                northeastWall = self._build_wall(ene, nne)
                northwestWall = self._build_wall(nnw, wnw)
                southwestWall = self._build_wall(wsw, ssw)
                    # record the walls in the cell
                cell.set_wall(self.SOUTH, southWall)
                cell.set_wall(self.EAST, eastWall)
                cell.set_wall(self.NORTH, northWall)
                cell.set_wall(self.WEST, westWall)
                cell.set_wall(self.SOUTHWEST, southwestWall)
                cell.set_wall(self.SOUTHEAST, southeastWall)
                cell.set_wall(self.NORTHEAST, northeastWall)
                cell.set_wall(self.NORTHWEST, northwestWall)
                if not self._kwargs.get('suppress_node_check', False):
                    assert len(cell.walls) == 8
                    counts = {}
                    for wall in cell.walls.values():
                        node1, node2 = list(wall.nodes)
                        counts[node1] = counts.get(node1, 0) + 1
                        counts[node2] = counts.get(node2, 0) + 1
                    assert len(counts) == 8
                    for count in counts.values():
                        assert count == 2

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
                southwest = tuple(reversed(self.transform(j-1, i-1)))
                southeast = tuple(reversed(self.transform(j+1, i-1)))
                northeast = tuple(reversed(self.transform(j+1, i+1)))
                northwest = tuple(reversed(self.transform(j-1, i+1)))
                    # neighboring faces
                    # -----------------
                    # here we use fact that both Cell.__setitem__ and
                    # Grid.__getitem__ handle the value None in a
                    # reasonable way...
                cell[self.SOUTH] = self[south]
                cell[self.EAST] = self[east]
                cell[self.NORTH] = self[north]
                cell[self.WEST] = self[west]
                cell[self.SOUTHWEST] = self[southwest]
                cell[self.SOUTHEAST] = self[southeast]
                cell[self.NORTHEAST] = self[northeast]
                cell[self.NORTHWEST] = self[northwest]

    def configure_passages(self):
        """carve passages through all internal walls"""
        for cell in self.each_cell():
                # note that linkTo does not link with None
            cell.linkto(cell[self.SOUTH])
            cell.linkto(cell[self.EAST])
            cell.linkto(cell[self.NORTH])
            cell.linkto(cell[self.WEST])
            cell.linkto(cell[self.SOUTHWEST])
            cell.linkto(cell[self.SOUTHEAST])
            cell.linkto(cell[self.NORTHEAST])
            cell.linkto(cell[self.NORTHWEST])
        return s

    def __str__(self):
        """for now, not implemented"""
        return '8-connected rectangular maze - not implemented'

    def sketch_setup(self):
        """sketch parameter setup"""
        ROADWIDTHTHETA = pi/15
        assert ROADWIDTHTHETA > 0 and ROADWIDTHTHETA < pi/8
        if not self._kwargs.get('road_theta'):
            self._kwargs['road_theta'] = ROADWIDTHTHETA
        super().sketch_setup()

        ROADEPSILON = 0.05
        assert ROADEPSILON >= 0
        if not self._kwargs.get('road_epsilon'):
            self._kwargs['road_epsilon'] = ROADEPSILON

        super().sketch_setup()

    def sketch_cell(self, sketcher, cell, location, dim, inset):
        """sketch a single cell"""
        x0, y0 = location             # southwest corner
        cwidth, cheight = dim
        color = cell.color if cell.color else "white"
#
#        if cell.isLinkedTo(cell[self.NORTHEAST]):
#            color = "red"
#            if cell.isLinkedTo(cell[self.NORTHWEST]):
#                color = "purple"
#        elif cell.isLinkedTo(cell[self.NORTHWEST]):
#            color = "blue"
#
#        if cell.isLinkedTo(cell[self.EAST]):
#            color = "cyan"
#            if cell.isLinkedTo(cell[self.WEST]):
#                color = "magenta"
#        elif cell.isLinkedTo(cell[self.WEST]):
#            color = "brown"
#
            # cell bounding box diagonal
        nw_x = x0 + inset * cwidth
        nw_y = y0 + (1 - inset) * cheight
        se_x = x0 + (1 - inset) * cwidth
        se_y = y0 + inset * cheight
        diagonal = ((nw_x, nw_y), (se_x, se_y))

        sketcher.draw_ellipse(diagonal, fill=color, outline="black")

        # for passage sketching, see the epilogue.

    def sketch_epilogue(self, sketcher):
        """epilogue to sketching"""

            # sketch N/S passages
        self.sketch_passages_north(sketcher)
        self.sketch_passages_east(sketcher)
        self.sketch_diagonal_passages(sketcher)

    def sketch_passages_north(self, sketcher):
        """sketch the north/south passages"""
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        inset = self._kwargs['inset']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self[(i, j)]
                nbr = cell[self.NORTH]
                if not nbr:
                    continue              # no north neighbor
                if not cell.isLinkedTo(nbr):
                    if not nbr.isLinkedTo(cell):
                        continue          # no N/S passage
                    # cell centers
                y1, x1 = cell.index
                x1, y1 = x1 + 0.5, y1 + 0.5
                u1, v1 = x1 * cwidth + hmargin, y1 * cheight + vmargin
                y2, x2 = nbr.index
                x2, y2 = x2 + 0.5, y2 + 0.5
                u2, v2 = x2 * cwidth + hmargin, y2 * cheight + vmargin
                self.sketch_passage_north(sketcher, cell, (u1, v1), \
                    nbr, (u2, v2), (cwidth, cheight), inset)

    def sketch_passage_north(self, sketcher, scell, sloc, ncell, nloc,
                              dim, inset):
        """sketch a north/south passage

        BUGS
            One-way passages need to be implemented.
        """
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']
        epsilon = self._kwargs['road_epsilon']

        theta1 = pi/2 - theta/2
        theta2 = pi/2 + theta/2
        a = (0.5 - inset) * cwidth      # semi-axis for horizontal
        a *= 1 - epsilon
        b = (0.5 - inset) * cheight     # semi-axis for vertical
        b *= 1 - epsilon

        x0, y0 = sloc                   # the south cell center
        x1, y1 = x0 + a*cos(theta2), y0 + b*sin(theta2)
        x2, y2 = x0 + a*cos(theta1), y1

        x0, y0 = nloc                   # the north cell center
        x3, y3 = x2, y0 - b*sin(theta2)
        x4, y4 = x1, y3

        polygon = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        fill = "white"
        sketcher.draw_polygon(polygon, fill)

    def sketch_passages_east(self, sketcher):
        """sketch the east/west passages"""
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        inset = self._kwargs['inset']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self[(i, j)]
                nbr = cell[self.EAST]
                if not nbr:
                    continue              # no east neighbor
                if not cell.isLinkedTo(nbr):
                    if not nbr.isLinkedTo(cell):
                        continue          # no E/W passage
                    # cell centers
                y1, x1 = cell.index
                x1, y1 = x1 + 0.5, y1 + 0.5
                u1, v1 = x1 * cwidth + hmargin, y1 * cheight + vmargin
                y2, x2 = nbr.index
                x2, y2 = x2 + 0.5, y2 + 0.5
                u2, v2 = x2 * cwidth + hmargin, y2 * cheight + vmargin
                self.sketch_passage_east(sketcher, cell, (u1, v1), \
                    nbr, (u2, v2), (cwidth, cheight), inset)

    def sketch_passage_east(self, sketcher, wcell, wloc, ecell, eloc,
                              dim, inset):
        """sketch a north/south passage

        BUGS
            One-way passages need to be implemented.
        """
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']/2
        epsilon = self._kwargs['road_epsilon']

        a = (0.5 - inset) * cwidth      # semi-axis for horizontal
        a *= 1 - epsilon
        b = (0.5 - inset) * cheight     # semi-axis for vertical
        b *= 1 - epsilon

        x0, y0 = wloc                   # the west cell center
        x1, y1 = x0 + a*cos(theta), y0 - b*sin(theta)
        x2, y2 = x1, y0 + b*sin(theta)

        x0, y0 = eloc                   # the east cell center
        x3, y3 = x0 - a*cos(theta), y2
        x4, y4 = x3, y1

        polygon = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        fill = "white"
        sketcher.draw_polygon(polygon, fill)

    def sketch_diagonal_passages(self, sketcher):
        """sketch the diagonal passages"""
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        inset = self._kwargs['inset']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

        locator = self.locate_diagonals()
        for cell in locator:
            nbr1 = cell[self.EAST]
            nbr2 = cell[self.NORTH]
            nbr3 = cell[self.NORTHEAST]
            ptype = locator[cell]

            if ptype % 2 == 1:      # NE/SW passage
                y1, x1 = cell.index
                x1, y1 = x1 + 0.5, y1 + 0.5
                u1, v1 = x1 * cwidth + hmargin, y1 * cheight + vmargin
                y2, x2 = nbr3.index
                x2, y2 = x2 + 0.5, y2 + 0.5
                u2, v2 = x2 * cwidth + hmargin, y2 * cheight + vmargin
                self.sketch_passage_northeast(sketcher, cell, \
                    (u1, v1), nbr3, (u2, v2), (cwidth, cheight), inset)

            if ptype // 2 == 1:     # NW/SE passage
                y1, x1 = nbr1.index
                x1, y1 = x1 + 0.5, y1 + 0.5
                u1, v1 = x1 * cwidth + hmargin, y1 * cheight + vmargin
                y2, x2 = nbr2.index
                x2, y2 = x2 + 0.5, y2 + 0.5
                u2, v2 = x2 * cwidth + hmargin, y2 * cheight + vmargin
                self.sketch_passage_northwest(sketcher, nbr1, \
                    (u1, v1), nbr2, (u2, v2), (cwidth, cheight), inset)

            if ptype == 3:          # need overpass
                if(random() <= 0.5):      # heads
                    y1, x1 = cell.index
                    x1, y1 = x1 + 0.5, y1 + 0.5
                    u1 = x1 * cwidth + hmargin
                    v1 = y1 * cheight + vmargin
                    y2, x2 = nbr3.index
                    x2, y2 = x2 + 0.5, y2 + 0.5
                    u2 = x2 * cwidth + hmargin
                    v2 = y2 * cheight + vmargin
                    self.sketch_northeast_overpass(sketcher, cell, \
                        (u1, v1), nbr3, (u2, v2), (cwidth, cheight), \
                        inset)
                else:
                    y1, x1 = nbr1.index
                    x1, y1 = x1 + 0.5, y1 + 0.5
                    u1 = x1 * cwidth + hmargin
                    v1 = y1 * cheight + vmargin
                    y2, x2 = nbr2.index
                    x2, y2 = x2 + 0.5, y2 + 0.5
                    u2 = x2 * cwidth + hmargin
                    v2 = y2 * cheight + vmargin
                    self.sketch_northwest_overpass(sketcher, nbr1, \
                        (u1, v1), nbr2, (u2, v2), (cwidth, cheight), \
                        inset)
            
    def locate_diagonals(self):
        locator = {}
        for i in range(self.rows):
            for j in range(self.cols):
                    # a small square of cells
                cell = self[(i, j)]
                nbr1 = cell[self.EAST]
                nbr2 = cell[self.NORTH]
                nbr3 = cell[self.NORTHEAST]
                    # is there a NE/SW diagonal passage?
                if nbr3:
                    if cell.isLinkedTo(nbr3) or nbr3.isLinkedTo(cell):
                        locator[cell] = 1
                    # is there a NW/SE diagonal passage?
                    #     possible values of locator:
                    #         1 - NE/SW passage only
                    #         2 - NW/SE passage only
                    #         3 - both
                if nbr1 and nbr2:
                    if nbr1.isLinkedTo(nbr2) or nbr2.isLinkedTo(nbr1):
                        locator[cell] = locator.get(cell, 0) + 2

        return locator

    def sketch_passage_northeast(self, sketcher, wcell, wloc, ecell,
                                 eloc, dim, inset):
        """sketch a north/south passage

        BUGS
            One-way passages need to be implemented.
        """
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']
        theta1 = pi/4 - theta/2
        theta2 = pi/4 + theta/2
        theta3 = 5*pi/4 - theta/2
        theta4 = 5*pi/4 + theta/2
        epsilon = self._kwargs['road_epsilon']

        a = (0.5 - inset) * cwidth      # semi-axis for horizontal
        a *= 1 - epsilon
        b = (0.5 - inset) * cheight     # semi-axis for vertical
        b *= 1 - epsilon

        x0, y0 = wloc                   # the southwest cell center
        x1 = x0 + a*cos(theta1)
        y1 = y0 + b*sin(theta1)
        x2 = x0 + a*cos(theta2)
        y2 = y0 + b*sin(theta2)

        x0, y0 = eloc                   # the northeast cell center
        x3 = x0 + a*cos(theta3)
        y3 = y0 + b*sin(theta3)
        x4 = x0 + a*cos(theta4)
        y4 = y0 + b*sin(theta4)

        polygon = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        fill = "white"
        sketcher.draw_polygon(polygon, fill)

    def sketch_passage_northwest(self, sketcher, wcell, wloc, ecell,
                                 eloc, dim, inset):
        """sketch a north/south passage

        BUGS
            One-way passages need to be implemented.
        """
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']
        theta1 = 3*pi/4 - theta/2
        theta2 = 3*pi/4 + theta/2
        theta3 = - pi/4 - theta/2
        theta4 = - pi/4 + theta/2
        epsilon = self._kwargs['road_epsilon']

        a = (0.5 - inset) * cwidth      # semi-axis for horizontal
        a *= 1 - epsilon
        b = (0.5 - inset) * cheight     # semi-axis for vertical
        b *= 1 - epsilon

        x0, y0 = wloc                   # the southeast cell center
        x1 = x0 + a*cos(theta1)
        y1 = y0 + b*sin(theta1)
        x2 = x0 + a*cos(theta2)
        y2 = y0 + b*sin(theta2)

        x0, y0 = eloc                   # the northwest cell center
        x3 = x0 + a*cos(theta3)
        y3 = y0 + b*sin(theta3)
        x4 = x0 + a*cos(theta4)
        y4 = y0 + b*sin(theta4)

        polygon = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        fill = "white"
        sketcher.draw_polygon(polygon, fill)

    def sketch_northeast_overpass(self, sketcher, wcell, wloc, ecell,
                                  eloc, dim, inset):
        """sketch a northeast overpass"""
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']
        theta1 = pi/4 - theta/2
        theta2 = pi/4 + theta/2
        theta3 = 5*pi/4 - theta/2
        theta4 = 5*pi/4 + theta/2

        a = 0.5 * cwidth                # semi-axis for horizontal
        b = 0.5 * cheight               # semi-axis for vertical

        x0, y0 = wloc                   # the southwest cell center
        x1 = x0 + a*cos(theta1)
        y1 = y0 + b*sin(theta1)
        x2 = x0 + a*cos(theta2)
        y2 = y0 + b*sin(theta2)

        x0, y0 = eloc                   # the northeast cell center
        x3 = x0 + a*cos(theta3)
        y3 = y0 + b*sin(theta3)
        x4 = x0 + a*cos(theta4)
        y4 = y0 + b*sin(theta4)

        sketcher.draw_line_segment((x2,y2), (x3,y3), thickness=2)
        sketcher.draw_line_segment((x1,y1), (x4,y4), thickness=2)

    def sketch_northwest_overpass(self, sketcher, wcell, wloc, ecell,
                                 eloc, dim, inset):
        """sketch a north/south passage

        BUGS
            One-way passages need to be implemented.
        """
        cwidth, cheight = dim
        theta = self._kwargs['road_theta']
        theta1 = 3*pi/4 - theta/2
        theta2 = 3*pi/4 + theta/2
        theta3 = - pi/4 - theta/2
        theta4 = - pi/4 + theta/2

        a = 0.5 * cwidth                # semi-axis for horizontal
        b = 0.5 * cheight               # semi-axis for vertical

        x0, y0 = wloc                   # the southeast cell center
        x1 = x0 + a*cos(theta1)
        y1 = y0 + b*sin(theta1)
        x2 = x0 + a*cos(theta2)
        y2 = y0 + b*sin(theta2)

        x0, y0 = eloc                   # the northwest cell center
        x3 = x0 + a*cos(theta3)
        y3 = y0 + b*sin(theta3)
        x4 = x0 + a*cos(theta4)
        y4 = y0 + b*sin(theta4)

        sketcher.draw_line_segment((x2,y2), (x3,y3), thickness=2)
        sketcher.draw_line_segment((x1,y1), (x4,y4), thickness=2)

class Rectangular6Grid(Rectangular8Grid):
    """Rectangular6Grid - implementation of the basic 6-connected
        rectangular grid

    The 4-connected and 8-connected grids have some undesirable
    topological properties.  The 6-connected grid eliminated some
    of these problems.

          +---+---+---+---+
          |   |   |   |   |       Figure 1 - one or two components...
          +---+---+---+---+         how many holes?
          |   | X |   |   |
          +---+---+---+---+
          |   |   | X |   |
          +---+---+---+---+
          |   |   |   |   |
          +---+---+---+---+

    Figure 1 illustrates one of the most basic problems.  Here we
    have a 4x4 rectangular array of square cells, with foreground
    cells marked 'X' and background cells unmarked.

    If we use the cells are 4-connected (EAST, NORTH, WEST, SOUTH),
    then the foreground image has two components, but the
    background image has just one hole.

    If we use the cells are 8-connected (EAST, NORTHEAST, NORTH, etc.),
    then the foreground image has just one component, but the
    background image has two holes.

          +---+---+---+---+
          | B | B | B | B |       Figure 2 - one or two holes...
          +---+---+---+---+         how many components?
          | B |   | B | B |
          +---+---+---+---+
          | B | B |   | B |
          +---+---+---+---+
          | B | B | B | B |
          +---+---+---+---+

    In a 6-connected grid, we use N/S/E/W connections as in both
    4-connected and 8-connected, and add either NE/SW or NW/SE
    connections.  As with the 4-connected grid, the grid is embedded
    in the plane, that is, no overpasses or underpasses are required.
    Apart from initialization, we can use everything we have written
    for the 8-connected grid.
    """
    def configure_neighborhood(self):
        """identify the cell's neighbors"""
        self.diagonal = -1 \
            if self._kwargs.get('configure_diagonal', 1) < 0 \
            else 1
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
                southwest = tuple(reversed(self.transform(j-1, i-1)))
                southeast = tuple(reversed(self.transform(j+1, i-1)))
                northeast = tuple(reversed(self.transform(j+1, i+1)))
                northwest = tuple(reversed(self.transform(j-1, i+1)))
                    # neighboring faces
                    # -----------------
                    # here we use fact that both Cell.__setitem__ and
                    # Grid.__getitem__ handle the value None in a
                    # reasonable way...
                cell[self.SOUTH] = self[south]
                cell[self.EAST] = self[east]
                cell[self.NORTH] = self[north]
                cell[self.WEST] = self[west]
                if self.diagonal >= 0:
                    cell[self.NORTHEAST] = self[northeast]
                    cell[self.SOUTHWEST] = self[southwest]
                else:
                    cell[self.SOUTHEAST] = self[southeast]
                    cell[self.NORTHWEST] = self[northwest]

# end of grid8.py
