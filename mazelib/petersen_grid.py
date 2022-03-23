"""Petersen_grid.py - implementation of the PetersenGrid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class PetersenGrid

DESCRIPTION

    The Petersen graph is a graph consisting of 10 vertices an 15
    edges, with five of the vertices arranged to form a circuit
    connected in a large outer regular pentagon, the remaining five
    connected to form a smaller regular pentagram inside the outer
    five, and with an additional edge from a vertex on the pentagon
    to the nearest vertex in the pentagram.  Each of the ten
    vertices is incident to exactly three edges.

    A standard way to generalize this graph is to place a regular
    n-gon outside a regular n-gram (or n-pointed star) and connect
    each vertex of the outside figure to the nearest vertex of the
    inside figure.

    There is more than one way to form a regular n-gram.  These ways
    amount to connecting each vertex to the k-th vertex in a
    counterclockwise direction.  (For the usual pentagram, k=2 or 3.)
    If k is 1 or n-1, the result is a regular n-gon.  If n and k
    are relatively the n-gram is a circuit, otherwise the n-gram
    breaks up into several independent circuit.  For example, if
    n=6 and k=2, the result is a hexagram (or "star of David") which
    consists of two equilateral triangles.  When n=2k, the figure
    is degenerate with two parallel edges incident to each vertex.

    The non-degenerate graphs are denoted G(n,k) with k at least 1
    and strictly less than n/2.  We can handle other values of k
    as follows:

          value of k    signifies         reduction
          ------------- ----------------- ---------------------------
          negative      clockwise         G(n,k) = G(n,k+n)
          zero          loops             G(n,0) is degenerate
          one           inner n-gon       G(n,1)
          1 < k < n/2   inner n-gram      G(n,k)
          k = n/2       parallel edges    G(n,n/2) is degenerate
          n/2 < k < n   clockwise         G(n,k) = G(n, n-k)
          k > n-1       periodic          G(n,k) = G(n, k-n)

    The Petersen graph is G(n,2).  It has no planar embedding.

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

    [2] "Petersen graph". Wikipedia, 29 November 2021. Web, accessed
        23 March 2022.
            URL: https://en.wikipedia.org/wiki/Petersen_graph

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

from math import pi, sin, cos, asin, acos, atan, sqrt
from cell import Cell
from grid import Grid

class PetersenGrid(Grid):
    """PetersenGrid - Petersen grid base class"""

    def __init__(self, n, k, *args, **kwargs):
        """constructor"""
            # reduce and validate n and k
        if not isinstance(n, int):
            raise TypeError(f'n={n} must be an integer')
        if n < 3:   # loops and parallel edges are inadmissible
            raise ValueError(f'n={n} must be at least 3')

        if not isinstance(n, int):
            raise TypeError(f'k={k} must be an integer')
        k1 = k % n
        if k1 > n/2:
            k1 = n - k
        if k != k1:
            print('WARNING: Petersen G({n},{k}) reduced to G({n},{k1})')
            k = k1

        if k == 0:
            raise ValueError(f'k={k} - loops are inadmissible')
        if k + k == n:
            raise ValueError(f'k={k} - parallel edges are inadmissible')
        self._n = n
        self._k = k

        super().__init__(n, k, *args, **kwargs)

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k

    def configure(self):
        """configuration"""
        n = self.n
        k = self.k
        wallbuilder = self._kwargs.get(self.WALLBUILDER)

            # Step 1: n-gon
            # construct the outer circuit
        for j in range(n):
            index = (0, j)
            cell = Cell(index)
            cell.index = index
            self[index] = cell

        for j in range(n):
            index1 = (0, j)
            index2 = (0, (j+1)%n)
            self[index1][index2] = self[index2]
            self[index2][index1] = self[index1]
            if wallbuilder:
                self[index1].link(self[index2])

            # Step 2: n-gram
            # construct the inner circuit
        for j in range(n):
            index = (1, j)
            cell = Cell(index)
            cell.index = index
            self[index] = cell

        for j in range(n):
            index1 = (1, j)
            index2 = (1, (j+k)%n)
            self[index1][index2] = self[index2]
            self[index2][index1] = self[index1]
            if wallbuilder:
                self[index1].link(self[index2])

            # Step 3: connect the two circuits
        for j in range(n):
            index1 = (0, j)
            index2 = (1, j)
            self[index1][index2] = self[index2]
            self[index2][index1] = self[index1]
            if wallbuilder:
                self[index1].link(self[index2])

    def sketch_setup(self):
        """sketch parameter setup

        DESCRIPTION

            Cells are small circles placed on a circle.  The edges are
            chords that connect two small circles. If the number of
            vertices is large and the maze is highly connected, the
            sketch will be a mess.
        """
        OUTERRING = 120          # pixel radius of outer ring
        if not self._kwargs.get('outer_ring'):
            self._kwargs['outer_ring'] = OUTERRING

        INNERRING = 60           # pixel radius of inner ring
        if not self._kwargs.get('inner_ring'):
            self._kwargs['inner_ring'] = INNERRING
        assert self._kwargs['outer_ring'] > self._kwargs['inner_ring']

        CELLRADIUS = 20          # pixel radius of a cell
        if not self._kwargs.get('cell_radius'):
            self._kwargs['cell_radius'] = CELLRADIUS
        assert self._kwargs['inner_ring'] > self._kwargs['cell_radius']

        EDGEWIDTH = pi / 18      # 10 degrees of arc
        if not self._kwargs.get('edge_width'):
            self._kwargs['edge_width'] = EDGEWIDTH
        assert self._kwargs['edge_width'] > 0

        MARGIN = 50              # reserved part of window
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        assert self._kwargs['hmargin'] > 0
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN
        assert self._kwargs['vmargin'] > 0

        MINWIDTH = 400
        if not self._kwargs.get('min_width'):
            self._kwargs['min_width'] = MINWIDTH

        MINHEIGHT = 300
        if not self._kwargs.get('min_height'):
            self._kwargs['min_height'] = MINHEIGHT

    def sketch_cell(self, sketcher, cell):
        """sketch a cell of the maze"""
        i, j = cell.index
        sradius = self._kwargs['outer_ring'] if i==0 \
            else self._kwargs['inner_ring']
        cradius = self._kwargs['cell_radius']
        xorigin, yorigin = self._kwargs['sketch_origin']
        theta = 2*pi*j / self.n
        xcenter = sradius * cos(theta) + xorigin
        ycenter = sradius * sin(theta) + yorigin
        center = (xcenter, ycenter)
        fill = cell.color if cell.color else "white"
        sketcher.draw_circle(center, cradius, fill=fill)
        cell.sketch_center = center     # save the cell's center

    def sketch_edge(self, sketcher, cell1, cell2):
        """sketch a cell of the maze"""
        cradius = self._kwargs['cell_radius']
        ewidth = self._kwargs['edge_width']

        xi0, yi0 = cell1.sketch_center    # center of cell1
        xj0, yj0 = cell2.sketch_center    # center of cell2

            # length of line connecting the centers:
            #     d(P,Q) = sqrt(dx^2 + dy^2)
        ds = sqrt((xi0-xj0)**2 + (yi0-yj0)**2)

            # coordinates of the intersections with the cell
            # walls...
        xi1 = xi0 + (xj0-xi0) * cradius/ds
        yi1 = yi0 + (yj0-yi0) * cradius/ds
        xj1 = xj0 + (xi0-xj0) * cradius/ds
        yj1 = yj0 + (yi0-yj0) * cradius/ds

            # angle of incidence from cell i to cell j
        dx, dy = xi1-xi0, yi1-yi0
        if dy >= 0:
                # Quadrants I and II
            theta = acos(dx/cradius)
        elif dx >= 0:
                # Quadrant IV
            theta = asin(dy/cradius)
        else:
                # Quadrand III
            theta = pi + atan(dy/dx)

            # angle of incidence from cell j to cell i
        dx, dy = xj1-xj0, yj1-yj0
        if dy >= 0:
                # Quadrants I and II
            phi = acos(dx/cradius)
        elif dx >= 0:
                # Quadrant IV
            phi = asin(dy/cradius)
        else:
                # Quadrand III
            phi = pi + atan(dy/dx)

        epsilon = ewidth/2
        r = cradius - 1

        x1, y1 = r*cos(theta+epsilon), r*sin(theta+epsilon)
        x1, y1 = x1 + xi0, y1 + yi0
        x2, y2 = r*cos(theta-epsilon), r*sin(theta-epsilon)
        x2, y2 = x2 + xi0, y2 + yi0

        x3, y3 = r*cos(phi+epsilon), r*sin(phi+epsilon)
        x3, y3 = x3 + xj0, y3 + yj0
        x4, y4 = r*cos(phi-epsilon), r*sin(phi-epsilon)
        x4, y4 = x4 + xj0, y4 + yj0

        polygon = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        sketcher.draw_polygon(polygon, "white")

    def sketch_prologue(self, sketcher):
        """prologue to sketching"""
        pass            # stub

    def sketch_epilogue(self, sketcher):
        """epilogue to sketching"""
        pass            # stub

    def sketch(self, sketcher, filename=None, show=True):
        """filter for sketching"""
        self.sketch_setup()
        cradius = self._kwargs['cell_radius']
        oradius = self._kwargs['outer_ring']
        iradius = self._kwargs['inner_ring']
        ewidth = self._kwargs['edge_width']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']
        minwidth = self._kwargs['min_width']
        minheight = self._kwargs['min_height']

        self.sketch_width = 2 * (oradius + cradius + hmargin)
        if self.sketch_width < minwidth:
            self.sketch_width = minwidth
        self.sketch_height = 2 * (oradius + cradius + vmargin)
        if self.sketch_height < minheight:
            self.sketch_height = minheight
        self._kwargs['sketch_origin'] \
            = (self.sketch_width/2, self.sketch_height/2)

        sketcher.open(width=self.sketch_width,
                      height=self.sketch_height)
        self.sketch_prologue(sketcher)

        for cell in self.each_cell():
            self.sketch_cell(sketcher, cell)

        for i in range(self.n):
            index = (0, i)
            cell1 = self[index]
            if not cell1:
                continue            # cell was deleted
            for cell2 in cell1.neighbors:
                if cell1.isLinkedTo(cell2) or cell2.isLinkedTo(cell1):
                    self.sketch_edge(sketcher, cell1, cell2)

            index = (1, i)
            cell1 = self[index]
            if not cell1:
                continue            # cell was deleted
            for cell2 in cell1.neighbors:
                if cell2.index[0] == 0:
                    continue
                if cell1.isLinkedTo(cell2) or cell2.isLinkedTo(cell1):
                    self.sketch_edge(sketcher, cell1, cell2)



        self.sketch_epilogue(sketcher)
        sketcher.close(filename=filename, show=show)

# end of petersen_grid.py
