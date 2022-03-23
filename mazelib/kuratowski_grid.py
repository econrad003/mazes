"""kuratowski_grid.py - implementation of Kuratowski graph grids
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class PartiteGrid
    class CompleteGrid
    subclass BipartiteGrid

DESCRIPTION

    The Kuratowski graphs are a collection of families of graphs that
    satisfy certain completeness properties.  Many proofs of graph
    properties depend on finding minors(*) of graphs which are
    specific Kuratowski graphs (**).

    One of the important theorems of graph theory says:

        A graph is planar (i.e. has a planar embedding) if and only
        if it has no minor which is isomorphic to either K(5) or K(3,3).

COMPLETE GRAPHS K(n)

    The easiest family of Kuratowski graphs to describe are the
    complete graphs.  If n is a non-negative integer, K(n) is the
    the graph whose vertices are the positive integers from 1 through
    n, and whose edges are all 2-sets of its vertices.  For example:

        K(0) - the empty graph

        K(1) - a single isolated vertex         1

        K(2) - a line segment                   1---2

        K(3) - a triangle                       1---2
                                                 \ /
                                                  3

        K(4)     1---2            vertices: 1, 2, 3, 4
                 |\ /|            edges: {1,2}, {1,3}, {1,4},
                 | 4 |                {2,3}, {2,4}, {3,4}
                 |/  |
                 3---+

    It is easy to see that, given a set of m colors, there are no
    vertex-colorings of K(n) if m<n; n! vertex-colorings if m=n,
    and m(m-1)(m-2)...(m-n+1) vertex-colorings if n>m.  (In a
    vertex-coloring, two adjacent vertices have different colors.
    Mixing colors, by the way, is not admissible.)

COMPLETE BIPARTITE GRAPHS

    The complete bipartite graphs K(m,n) are obtained by taking as
    vertices the first m positive integers of one color (say red) and
    the first n positive integers of a second color (say green), and
    assigning edges between each red vertex and each green vertex.

        K(3,3)        vertices: 1R, 2R, 3R, 1G, 2G, 3G
                      edges:
                          {1R, 1G}, {1R, 2G}, {1R, 3G},
                          {2R, 1G}, {2R, 2G}, {2R, 3G},
                          {3R, 1G}, {3R, 2G}, {3R, 3G}

        Note that K(2) = K(1,1).

COMPLETE TRIPARTITE GRAPHS

    Going up one step, are the complete tripartite graphs K(m,n,p).
    Here we have three sets of vertices, say m red vertices, n green
    vertices, and p blue vertices.each red vertex is adjacent to every
    green and every blue vertex, each green vertex to every red and
    every blue one, and each blue to every red and every green.  No
    red is adjacent to a red, no green to a green, and no blue to a
    blue.

    The triangle graph K(3) is tripartite: K(3) = K(1,1,1).

    A square with one diagonal is tripartite:

        K(1,1,2)      B1--G1
                       | /|
                       |/ |
                      R1--B2

NOTES

    *   A minor of a graph is a smaller graph obtained by deleting edges
        and isolated vertices, or by contracting edges.  (A subgraph
        is a special kind of minor which can be obtained by deleting
        edges and isolated vertices.)

    **  To be precise and pedantic, we should speak of isomorphism
        classes of graphs.  The Kuratowski graphs are actually
        isomorphism classes of graphs.

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

    [2] most textbooks for an college course which introduces graph
        theory will talk about complete graphs and complete bipartite
        graphs, and about their connection to planar embeddings.

    [3] "Complete graph". Wikipedia, 16 February 2022. Web, accessed
        21 March 2022.
            URL: https://en.wikipedia.org/wiki/Complete_graph

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

class PartiteGrid(Grid):
    """PartiteGrid - Kuratowski complete partite grid base class

    The non-keyword arguments must be positive integers.  At least two
    are required.
    """

    @staticmethod
    def get_indices(args):
        """find the indices"""
        assert len(args) >= 2
        indices = []
        for i in range(len(args)):      # rows
            j = args[i]
            if not isinstance(j, int):
                raise TypeError(f'{j} is not an integer')
            if j < 1:
                raise ValueError(f'{j} is not positive')
            for k in range(j):      # columns
                indices.append((i,k))
        return indices

    def configure(self):
        """configuration"""
            # create the vertices
        assert len(self._args) >= 2
        indices = self.get_indices(list(self._args))
        for index in indices:
            cell = Cell(index)
            cell.index = index
            self[index] = cell

            # create the grid edges
        for cell1 in self.each_cell():
            i1, _ = cell1.index
            for cell2 in self.each_cell():
                i2, _ = cell2.index
                if i1 != i2:      # not in same row, so neighbors
                    cell1[cell2.index] = cell2     # grid topology
                    if self._kwargs.get(self.WALLBUILDER):
                        cell1.linkto(cell2)

        # sketching will be implemented for the bipartite subclass...

class CompleteGrid(Grid):
    """the Kuratowski complete graphs K(n) on n vertices"""

    def __init__(self, n, *args, **kwargs):
        """constructor"""
        self._n = n
        if not isinstance(n, int):
            raise TypeError(f'K(n)=K({n}) - n must be an integer')
        if n < 0:
            raise ValueError(f'K(n)=K({n}) - n must be non-negative')
        super().__init__(n, *args, **kwargs)

    @property
    def n(self):
        """The value of n"""
        return self._n

    def configure(self):
        """configuration"""
            # create the vertices
        n = self.n
        for i in range(n):
            cell = Cell(i)
            self[i] = cell
            cell.index = i

            # create the grid edges
        for cell1 in self.each_cell():
            i1 = cell1.index
            for cell2 in self.each_cell():
                i2 = cell2.index
                if i1 == i2:
                    continue          # no loops
                cell1[i2] = cell2     # grid topology
                if self._kwargs.get(self.WALLBUILDER):
                    cell1.linkto(cell2)

    def sketch_setup(self):
        """sketch parameter setup

        DESCRIPTION

            Cells are small circles placed on a circle.  The edges are
            chords that connect two small circles. If the number of
            vertices is large and the maze is highly connected, the
            sketch will be a mess.
        """
        CELLRADIUS = 20          # pixel radius of a cell
        assert CELLRADIUS > 5
        if not self._kwargs.get('cell_radius'):
            self._kwargs['cell_radius'] = CELLRADIUS

        SKETCHRADIUS = 120       # pixel radius of the large circle
        assert SKETCHRADIUS > 4*CELLRADIUS
        if not self._kwargs.get('sketch_radius'):
            self._kwargs['sketch_radius'] = SKETCHRADIUS

        EDGEWIDTH = pi / 18      # 10 degrees of arc
        assert EDGEWIDTH > 0 and EDGEWIDTH < pi/6
        if not self._kwargs.get('edge_width'):
            self._kwargs['edge_width'] = EDGEWIDTH

        MARGIN = 50              # reserved part of window
        assert MARGIN > 1
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN

        MINWIDTH = 400
        if not self._kwargs.get('min_width'):
            self._kwargs['min_width'] = MINWIDTH

        MINHEIGHT = 300
        if not self._kwargs.get('min_height'):
            self._kwargs['min_height'] = MINHEIGHT

    def sketch_cell(self, sketcher, cell):
        """sketch a cell of the maze"""
        cradius = self._kwargs['cell_radius']
        sradius = self._kwargs['sketch_radius']
        xorigin, yorigin = self._kwargs['sketch_origin']
        index = cell.index
        theta = 2*pi*index / self.n
        xcenter = sradius * cos(theta) + xorigin
        ycenter = sradius * sin(theta) + yorigin
        center = (xcenter, ycenter)
        fill = cell.color if cell.color else "white"
        sketcher.draw_circle(center, cradius, fill=fill)

    def sketch_edge(self, sketcher, cell1, cell2):
        """sketch a cell of the maze"""
        cradius = self._kwargs['cell_radius']
        sradius = self._kwargs['sketch_radius']
        ewidth = self._kwargs['edge_width']
        xorigin, yorigin = self._kwargs['sketch_origin']

        i = cell1.index
        j = cell2.index
        n = self.n
        assert j < i

            # center of cell i
        alpha = 2*pi*i/n
        a, b = cos(alpha), sin(alpha)
        xi0 = xorigin + a * sradius
        yi0 = yorigin + b * sradius

            # center of cell j
        beta = 2*pi*j/n
        a, b = cos(beta), sin(beta)
        xj0 = xorigin + a * sradius
        yj0 = yorigin + b * sradius

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
        sradius = self._kwargs['sketch_radius']
        ewidth = self._kwargs['edge_width']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']
        minwidth = self._kwargs['min_width']
        minheight = self._kwargs['min_height']

        self.sketch_width = 2 * (sradius + cradius + hmargin)
        if self.sketch_width < minwidth:
            self.sketch_width = minwidth
        self.sketch_height = 2 * (sradius + cradius + vmargin)
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
            cell1 = self[i]
            if not cell1:
                continue            # cell was deleted
            for j in range(i):
                cell1 = self[i]
                cell2 = self[j]
                if not cell2:
                    continue        # cell was deleted
                if cell1.isLinkedTo(cell2) or cell2.isLinkedTo(cell1):
                    self.sketch_edge(sketcher, cell1, cell2)

        self.sketch_epilogue(sketcher)
        sketcher.close(filename=filename, show=show)

class BipartiteGrid(PartiteGrid):
    """the Kuratowski bipartite grids K(m,n)"""

    def __init__(self, m, n, *args, **kwargs):
        """constructor"""
        self._m = m
        self._n = n
        self.warnings = {}

        if not isinstance(m, int):
            raise TypeError(f'm={m} - m must be an integer')
        if m < 0:
            raise ValueError(f'm={m} - m must be non-negative')

        if not isinstance(n, int):
            raise TypeError(f'n={n} - n must be an integer')
        if m < 0:
            raise ValueError(f'n={n} - n must be non-negative')

        super().__init__(m, n, optargs=args, **kwargs)

    @property
    def m(self):
        """number of cells in top row"""
        return self._m

    @property
    def n(self):
        """number of cells in bottom row"""
        return self._n

    def sketch_setup(self):
        """sketch parameter setup

        DESCRIPTION

            Cells are small circles placed on a circle.  The edges are
            chords that connect two small circles. If the number of
            vertices is large and the maze is highly connected, the
            sketch will be a mess.
        """
        CELLRADIUS = 20          # pixel radius of a cell
        assert CELLRADIUS > 5
        if not self._kwargs.get('cell_radius'):
            self._kwargs['cell_radius'] = CELLRADIUS

        EDGEWIDTH = pi / 18      # 10 degrees of arc
        assert EDGEWIDTH > 0 and EDGEWIDTH < pi/6
        if not self._kwargs.get('edge_width'):
            self._kwargs['edge_width'] = EDGEWIDTH

        MARGIN = 50              # reserved part of window
        assert MARGIN > 1
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN

        MINWIDTH = 400
        if not self._kwargs.get('min_width'):
            self._kwargs['min_width'] = MINWIDTH

        MINHEIGHT = 300
        if not self._kwargs.get('min_height'):
            self._kwargs['min_height'] = MINHEIGHT

    def sketch_cell(self, sketcher, cell):
        """sketch a cell of the maze"""
        cradius = self._kwargs['cell_radius']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']
        width = self._kwargs['min_width']
        cellswide = max(self.m, self.n)
        if width <= 2*cellswide*cradius:
            if not warnings.get(1):
                print('WARNING: insufficient sketch width for cells')
                warnings[1] = True
        width -= 2*cradius
        height = self._kwargs['min_height']
        if height <= 4*cradius:
            if not warnings.get(2):
                print('WARNING: insufficient sketch height for cells')
                warnings[2] = True
        height -= 2*cradius

        i, j = cell.index
        if i==0:    # top row has m cells from first class
            k = self.m
            ycenter = height - cradius
        else:   # bottom row has n cells from second class
            k = self.n
            ycenter = cradius + vmargin
        xcenter = j*(width-2*cradius)/k + cradius + hmargin
        # print(cell.index, k, (xcenter, ycenter))

        center = (xcenter, ycenter)
        fill = cell.color if cell.color else "white"
        sketcher.draw_circle(center, cradius, fill=fill)
        cell.sketch_center = center       # save for edge processing

    def sketch_edge(self, sketcher, cell1, cell2):
        """sketch a cell of the maze"""
        cradius = self._kwargs['cell_radius']
        ewidth = self._kwargs['edge_width']

        i = cell1.index
        j = cell2.index

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
        ewidth = self._kwargs['edge_width']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']
        minwidth = self._kwargs['min_width']
        minheight = self._kwargs['min_height']

        sketcher.open(width=minwidth, height=minheight)
        self.sketch_prologue(sketcher)

        for cell in self.each_cell():
            self.sketch_cell(sketcher, cell)

        for i in range(self.m):
            cell1 = self[(0,i)]
            if not cell1:
                continue            # cell was deleted
            for j in range(self.n):
                cell2 = self[(1,j)]
                if not cell2:
                    continue        # cell was deleted
                if cell1.isLinkedTo(cell2) or cell2.isLinkedTo(cell1):
                    self.sketch_edge(sketcher, cell1, cell2)

        self.sketch_epilogue(sketcher)
        sketcher.close(filename=filename, show=show)

# end of kuratowski_grid.py
