"""grid.py - implementation of the Grid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class PolarGrid - a circular grid
    class PolarCell - the general cell type for polar grids
    class PoleCell - a specialized cell type for polar grids

    algorithm Inwinder - for creating sidewinder and lazy binary tree
        mazes on polar grids
    algorithm Outwinder - for creating sidewinder and lazy binary tree
        mazes on polar grids (winds outward instead of inward)

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
"""

from math import sin, cos, pi, floor
from random import random, choice, randrange

from cell import SquareCell
from grid import RectangularGrid

class PolarCell(SquareCell):
    """cells in a polar grid"""

    def initialize(self):
        """initialization

        KEYWORD ARGUMENTS

            index - the row and column
            theta1, theta2 - the clockwise angle range
                (in revolutions)

        The defaults are for a pole cell.
        """
        self.index = self._kwargs.get('index', (0,0))  # row, column
        self.i, self.j = self.index
        self.theta1 = self._kwargs.get('theta1', 0)
        self.theta2 = self._kwargs.get('theta1', 1)
        self.polecell = isinstance(self, PoleCell)

class PoleCell(PolarCell):
    """cells in a polar grid"""
    pass

class PolarGrid(RectangularGrid):
    """PolarGrid - implementation of the basic circular grid"""

    INWARD = 'in'
    OUTWARD = 'out'
    CCW = 'ccw'     # counterclockwise / anticlockwise
    CW = 'cw'       # clockwise

    def __init__(self, rows, mincols, *args, **kwargs):
        """constructor

        REQUIRED ARGUMENTS

            rows - the number of concentric circles in the maze
            mincols - the number of cells at the pole

        KEYWORD ARGUMENTS

            cell_ratio - the ideal ratio of the cell's inner arc to its
               thickness (default: 1, minimum: 1)
        """
        assert rows >= 1
        assert mincols >= 1

        self.rows = rows
        self.mincols = mincols
        self.column_cells = [mincols]
        self.column_splits = []
        self.ratio = max(0.1, kwargs.get('cell_ratio', 1))

            # we pass the arguments to the parent class
        super().__init__(rows, mincols, *args, **kwargs)

    def initialize(self):
        """create the directories of available nodes and faces"""
        rows = self.rows
        lengths = self.column_cells
        splits = self.column_splits
        ratio = self.ratio

        for i in range(rows):
                # determine how to split going outward
            cols = lengths[i]           # number of columns in this row
            theta = 2*pi*i/cols         # length of outer wall
            split = 1 if cols>1 else 2  # force a pole cell to split
            if floor(theta) > ratio:
                nsplit = int(floor(theta/ratio))
                split = max(split, nsplit)
            splits.append(split)        # outward neighbors per cell
            lengths.append(cols*split)  # number of cells in next row

                # create the cells
            if cols > 1:
                for j in range(cols):
                        # a typlcal cell
                    theta1 = j / cols
                    theta2 = (j+1) / cols
                    cell = PolarCell(index=(i,j), theta1=theta1,
                                     theta2=theta2)
                    self[cell.index] = cell
                        # inward nodes
                    self._nodes[(i, j)] = self.Node(i, j)                   
            else:       # a single cell at the pole
                cell = PoleCell()
                self[cell.index] = cell

            # outward nodes for last row
        lengths.pop()
        splits[-1] = 1
        for j in range(lengths[-1]):
            self._nodes[(rows, j)] = self.Node(rows, j)

        self.column_cells = lengths
        self.column_splits = splits

    def configure(self):
        """finish building the cells"""
        self.configure_walls()
        self.configure_neighborhood()
        if self._kwargs.get(self.WALLBUILDER):
            self.configure_passages()

    def configure_walls(self):
        """build the cell boundaries"""
        rows = self.rows
        lengths = self.column_cells
        splits = self.column_splits
        
        for i in range(rows):
            cols = lengths[i]
            split = splits[i]
            for j in range(cols):
                index = (i,j)
                cell = self[index]
                    # inward wall
                if cols > 0:
                    sw = (i, j)
                    cell.set_node(sw)
                    se = (i, (j+1)%cols)
                    cell.set_node(se)
                    swall = self._build_wall(sw, se)
                    cell.set_wall(self.INWARD, swall)

                    nw = (i+1, split*j)
                    cell.set_node(nw)
                    wwall = self._build_wall(sw, nw)
                    cell.set_wall(self.CCW, swall)

                    ne = (i+1, (split*(j+1))%(split*cols))
                    cell.set_node(ne)
                    ewall = self._build_wall(se, ne)
                    cell.set_wall(self.CW, ewall)

                for k in range(split):
                    nw = (i+1, split*j+k)
                    cell.set_node(nw)
                    ne = (i+1, (split*j+k+1)%(split*cols))
                    cell.set_node(ne)
                    nwall = self._build_wall(sw, se)
                    cell.set_wall(self.OUTWARD + f'{k}', nwall)

    def configure_neighborhood(self):
        """identify the cell's neighbors"""
        rows = self.rows
        lengths = self.column_cells
        splits = self.column_splits

        for i in range(rows):         # ordinates or y values
            cols = lengths[i]
            split = splits[i]
            for j in range(cols):     # abscissae or x-values
                index = (i, j)
                cell = self[index]

                    # neighboring face coordinates (except inward)

                if not cell.polecell:
                    ccw = (i, (j-1)%cols)
                    cell[self.CCW] = self[ccw]
                    cw = (i, (j+1)%cols)
                    cell[self.CW] = self[cw]

                if i + 1 == rows:
                    continue          # no neighbors for outer row

                for k in range(split):
                    outward = (i+1, (split*j+k))
                    nbr = self[outward]
                    if nbr:
                        direction = self.OUTWARD + f'{k}'
                        cell[direction] = nbr
                        nbr[self.INWARD] = cell

    def configure_passages(self):
        """carve passages through all internal walls"""
        for cell in self.each_cell():
            for nbr in cell.passages:
                cell.linkto(nbr)

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

    def __str__(self):
        """string representation of the maze"""
        raise NotImplementedError('Not valid for polar grids')

    def row(self, i, split=0, reverse=False):
        """the cells in the indicated row from west to east

        Returns a list of cells.

        The order of the cells can be modified using the 'split' and
        'reverse' keyword arguments.
        """
        lengths = self.column_cells
        cols = lengths[i]
        cells = []
        for j in range(cols):
            cells.append(self[(i, j)])
        if split:
            cells = cells[split:] + cells[:split]
        if reverse:
            cells.reverse()
        return cells

    def column(self, j, split=0, reverse=False):
        """not valid for polar grids"""
        raise NotImplementedError('Not valid for polar grids')

    def sketch_setup(self):
        """sketch parameter setup"""
        MAZERADIUS = 200       # pixel dimensions of cell
        assert MAZERADIUS > 10
        if not self._kwargs.get('sketch_radius'):
            self._kwargs['sketch_radius'] = MAZERADIUS

        MARGIN = 5          # reserved part of window
        assert MARGIN > 1
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN

        INSET = 0.12        # corners of cells
        assert INSET > 0 and INSET < 0.36
        if not self._kwargs.get('inset'):
            self._kwargs['inset'] = INSET

        OUTLINE = "black"
        if not self._kwargs.get('outline'):
            self._kwargs['outline'] = OUTLINE
            if self._kwargs['outline'] == 'None':
                self._kwargs['outline'] = None

        EDGEWIDTH = 5
        if not self._kwargs.get('edge_width'):
            self._kwargs['edge_width'] = EDGEWIDTH

    @property
    def sketch_width(self):
        return 2 * (self._kwargs['sketch_radius'] + \
            2 * self._kwargs['hmargin'])

    @property
    def sketch_height(self):
        return 2 * (self._kwargs['sketch_radius'] + \
            2 * self._kwargs['vmargin'])

    def sketch_cell(self, sketcher, cell):
        """sketch a single cell"""
        sradius = self._kwargs['sketch_radius']
        inset = self._kwargs['inset']
        outline = self._kwargs['outline']

        x0, y0 = self.sketch_width/2, self.sketch_height/2  # center
        center = (x0,y0)

        i, j = cell.index
        rows = self.rows
        cols = self.column_cells[i]

        r1 = (i+1-inset)/rows           # outer radius
        r1 *= sradius

        color = cell.color if cell.color else "white"

        if cell.polecell:               # single cell at the pole
            sketcher.draw_circle(center, r1,
                                 outline=outline, fill=color)
        else:
            r2 = (i+inset)/rows             # inner radius
            r2 *= sradius
            theta1 = j / cols               # in revolutions
            theta2 = (j+1) / cols

                # get a reasonable inset
            dtheta = inset / cols
            ds = r2 * 2* pi* dtheta         # outer width of dtheta
            dr = inset * sradius / rows     # radial inset
            if dr < ds:
                dtheta = dr / (r2 * 2 * pi)

            theta1 += dtheta
            theta2 -= dtheta

            sketcher.draw_segment(center, r1, r2, theta1, theta2,
                                  fill=color, outline=outline)

    def sketch_inward_edge(self, sketcher, cell1, cell2,
                           color='white'):
        """sketch inward edges

        For the time being, we treat all edges are undirected.

        Note that a PoleCell has no inward edges, so cell1 is not an
        instance of PoleCell.
        """
        sradius = self._kwargs['sketch_radius']
        inset = self._kwargs['inset']
        outline = self._kwargs['outline']
        width = self._kwargs['edge_width']
        rows = self.rows

        x0, y0 = self.sketch_width/2, self.sketch_height/2  # center

        i1, j1 = cell1.index
        r1 = (i1+inset)/rows            # inner radius of cell1
        r1 *= sradius

        i2, j2 = cell2.index
        r2 = (i2+1-inset)/rows          # outer radius of cell2
        r2 *= sradius

        r1 += 1                         # cut through outlines
        r2 -= 1

        cols = self.column_cells[i1]
        theta = (2*j1+1) / (2*cols)     # central radial axis (rev)
        theta *= 2*pi                   # (radians)

            # clockwise coordinates!
        source = x0 + r1*cos(theta), y0 - r1*sin(theta)
        sink = x0 + r2*cos(theta), y0 - r2*sin(theta)

        sketcher.draw_line_segment(source, sink, fill=color,
                          thickness=width)

    def sketch_clockwise_edge(self, sketcher, cell1, cell2,
                              color="white"):
        """sketch inward edges

        For the time being, we treat all edges are undirected.
        """
        sradius = self._kwargs['sketch_radius']
        inset = self._kwargs['inset']
        outline = self._kwargs['outline']
        width = self._kwargs['edge_width']
        rows = self.rows

        x0, y0 = self.sketch_width/2, self.sketch_height/2  # center
        center = (x0,y0)

        i, j = cell1.index
        r1 = (i+1-inset)/rows           # outer radius of cell1 and cell2
        r1 *= sradius
        r2 = (i+inset)/rows             # inner radius of cell1 and cell2
        r2 *= sradius

        width = r1 - r2
        r1 -= width / 4
        r2 += width / 4

        cols = self.column_cells[i]
        theta = (j+1) / cols           # in revolutions

                # get a reasonable outset
        dtheta = (0.25 - inset/2) / cols
        theta1 = theta - dtheta
        theta2 = theta + dtheta

        sketcher.draw_segment(center, r1, r2, theta1, theta2,
                              fill=color, outline=None)

    def sketch_edge(self, sketcher, cell1, cell2):
        """sketch edges

        So that edges are not sketched twice, we sketch only clockwise
        and inward edges.

        For the time being, we treat all edges are undirected, so
        counterclockwise and outward arcs will be missed, and clockwise
        and inward arcs will be treated as edges.
        """
        color = self.edge_color(cell1, cell2)
        if cell1[self.INWARD] == cell2:
            self.sketch_inward_edge(sketcher, cell1, cell2,
                                    color=color)
            return

        if cell1[self.CW] == cell2:
            self.sketch_clockwise_edge(sketcher, cell1, cell2,
                color=color)
            return

    def sketch(self, sketcher, filename=None, show=True):
        """filter for sketching"""
        self.sketch_setup()
        sradius = self._kwargs['sketch_radius']
        inset = self._kwargs['inset']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']
        outline = self._kwargs['outline']

        sketcher.open(width=self.sketch_width,
                      height=self.sketch_height)

        self.sketch_prologue(sketcher)
        for cell in self.each_cell():
            self.sketch_cell(sketcher, cell)

        for cell1 in self.each_cell():
            for cell2 in self.each_cell():
                if cell1.isLinkedTo(cell2):
                    self.sketch_edge(sketcher, cell1, cell2)

        self.sketch_epilogue(sketcher)

        sketcher.close(filename=filename, show=show)

class InWinder(object):
    """a sidewinder passage carving algorithm for polar grids

    This algorithm can also be tailored to produce lazy binary trees.
    """

    class State(object):
        """state variables for Inwinder - a stub"""

        def __init__(self, **kwargs):
            """constructor

            KEYWORD ARGUMENTS

                Several of the row_choice methods provided below have
                an optional keyword argument for changing the behavior
                of the method.  Implemented keywords:

                    p - coin flip heads probability (default: 0.5)
                          used by median, first_last

                    gofirst - start going counterclockwise instead
                        of clockwise (default: false)
                          used by cocktail
            """
            self.kwargs = kwargs

    @classmethod
    def on(cls, maze, p=0.5, row_choice=None, state=None):
        """create an inwinder maze on a polar grid

        REQUIRED ARGUMENTS

            maze - a Maze instance on a PolarGrid instance.
                The grid should be initialized as a passage carver.

        KEYWORD ARGUMENTS

            p - the coin flip probability of heads.  When the coin flip
                is heads, a passage is carved clockwise.  When the coin
                flip is tails, the row choice method is called to select
                a cell in the current long passageway.
                    (default: fair coin p=0.5)

            row_choice - a method which chooses one from a list of at
                least one cell.  The method takes two arguments, namely
                a State-compatible object and a non-empty list of cells.
                    (default: None - use InWinder.random_choice)

                Provided below are the following row_choice methods:

                    InWinder.random_choice (like Sidewinder)
                    InWinder.first_choice (lazy inward/ccw binary tree)
                    InWinder.last_choice (lazy inward/cw binary tree)
                    InWinder.median_choice (an averaged Sidewinder)
                    InWinder.first_last_choice (lazy inward binary tree)
                    InWinder.cocktail_choice (lazy inward binary tree)

            state - a State-compatible object or None.  If one is
                provided, the instance variable state.grid will be set
                to the value maze.grid, and the instance variable
                state.initialized will be set to False.
                    (default: None - use the Inwinder.State class)

            q - a coinflip probability used by some of the run-choice
                methods

            gofirst - switches the alternation in the cocktail shaker
                method

        NOTES

            InWinder (or inward winder) is an adaptation of the
            sidewinder algorithm for polar grids.  Just as lazy binary
            tree algorithms             are special cases of the
            sidewinder algorithm obtained by always choosing one of the
            two endpoints of a run as the rising point, so also we have
            lazy binary tree algorithms for the polar grid.

            InWinder has the same implementation problems that occur
            when adapting the sidewinder algorithm to a cylindrical
            grid. Just as we must insure that there is an end of row in
            the cylinder, so we must also insure that there is an end of
            each latitudinal row in the polar grid.  Just as runs in the
            cylindical grid can proceed periodically along the east/west
            rows, so do runs in the polar grid proceed periodically
            along the latitudinal (or counterclockwise/clockwise) rows
            of the polar grid. (Rows in the cylindrical and polar grids
            form circuits, whereas those in the 4-connected rectangular
            grid form chains.)

            Just as sidewinder produces a long corridor (or chain) along
            the top or the bottom row of the cylindrical grid, the
            inward winder does likewise for cells that are incident to
            the pole.  If there is a single cell atop the pole, the long
            chain is degenerate, reduced to a single cell.  Those of us
            inclined to Greek mythology may imagine the hero Theseus,
            supplied by King Minos's daughter Ariadne with a sword and
            a large sphere of yarn, working his way down to the center
            of the maze, slaying the dreaded mutant Minotaur, and
            returning to meet Ariadne at the entrance by following a
            trail of yarn.  But maids, lest ye fall in love with the
            dashing hero, please note that, on returning to Athens,
            after all passion was spent, Theseus abandoned Ariadne on
            a deserted island.  If my memory is correct, he ended up
            marrying a traitorous Amazon queen who helped defend Athens
            against an invasion by her compatriots.  As for Ariadne, she
            supposedly pined away and died -- but was instead probably
            enslaved by island sprites and forced into a life of
            household drudgery.

            It is also possible to create an outward winder, but, with
            a long single chain in the outermost latitudinal row, the
            results will not be as interesting.

        SOLVING AN INWARD WINDING MAZE

            The easiest wsy to solve the maze is to work your way
            inward from an outside cell.  The specialized algorithm
            consists of one pass per latitudinal row, as follows:

                Take the unique inward exit for the latitudinal run.
                To find it, proceed clocwise toward the clockwise wall;
                if it isn't in that direction, proceed counterclockwise
                until you find it.

            To use the above algorithm to solve a problem involving
            arbitrary start and end cells, proceed from each of the
            terminals to the pole.  The two paths will have a first
            intersection cell.  Follow the path from start to the first
            intersection.  Then trace backwards along the path from
            finish.
        """
            # housekeeping
        grid = maze.grid

        if not state:
            state = cls.State()
        state.grid = grid             
        state.initialized = False

        if not row_choice:
            row_choice = cls.random_choice

            # main

        rows = grid.rows
        lengths = grid.column_cells
        for i in range(rows):
            cols = lengths[i]
            curr = first = grid[(i, randrange(cols))]
            firsthit = True
            run = []
            while curr and (curr != first or firsthit):
                firsthit = False      # we make sure first is used
                prev = curr
                curr = curr[PolarGrid.CW]
                can_go_inward = bool(prev[PolarGrid.INWARD])
                can_go_forward = curr and curr != first

                if can_go_inward:
                    run.append(prev)
                can_go_inward = bool(run)

                if can_go_forward:
                    if can_go_inward:
                        if random() <= p:       # heads
                                # go forward
                            prev.link(curr)
                        else:                   # tails
                                # close out run and go inward
                            cell = row_choice(state, run)
                            cell.link(cell[PolarGrid.INWARD])
                            run = []
                else:                           # last in row
                    if can_go_inward:
                            # close out run and go inward
                        cell = row_choice(state, run)
                        cell.link(cell[PolarGrid.INWARD])
                        run = []

            # housecleaning
        return maze

    @staticmethod
    def random_choice(_, cells):
        """choose from a list of cells to carve inward

        stateless - the state parameter is ignored
        """
        return choice(cells)

    @staticmethod
    def first_choice(_, cells):
        """choose from a list of cells to carve inward

        stateless - the state parameter is ignored
        """
        return cells[0]

    @staticmethod
    def last_choice(_, cells):
        """choose from a list of cells to carve inward

        stateless - the state parameter is ignored
        """
        return cells[-1]

    @staticmethod
    def median_choice(state, cells):
        """choose from a list of cells to carve inward

        The state is used when the number cells is even.  In this
        case a coin is flipped - heads takes the higher candidate.
        """
        if not state.initialized:
                # default is a fair coin
            state.q = kwargs.get('q', 0.5)
            state.initialized = True

        median = len(cells) // 2
        if len(cells) % 2 == 1:     # odd number of cells (easy case)
            return cells[median]

        if random() <= state.q:     # heads
            return cells[median]
        return cells[median-1]      # tails

    @staticmethod
    def first_last_choice(state, cells):
        """choose from a list of cells to carve inward

        The state is used.  A coin is flipped - heads takes the 
        first cell and tails takes the last.
        """
        if not state.initialized:
                # default is a fair coin
            state.q = kwargs.get('q', 0.5)
            state.initialized = True

        if random() <= state.p:     # heads
            return cells[0]
        return cells[-1]            # tails

    @staticmethod
    def cocktail_choice(state, cells):
        """choose from a list of cells to carve inward

        The state is used.  The method alternates between the first cell
        and the last.
        """
        if not state.initialized:
                # default is a fair coin
            state.gofirst = kwargs.get('gofirst', False)
            state.initialized = True

        if state.gofirst:
            state.gofirst = False
            return cells[0]

        state.gofirst = True           
        return cells[-1]

class OutWinder(InWinder):
    """create an inwinder maze on a polar grid

    It winds outward instead of inward.  As a result, the outermost row
    is a single chain with just one wall.
    """

    @classmethod
    def on(cls, maze, p=0.5, row_choice=None, state=None):
        """create an outwinder maze on a polar grid

        The arguments are as for InWinder.on with one addition...

        REQUIRED ARGUMENTS

            maze - a Maze instance on a PolarGrid instance.
                The grid should be initialized as a passage carver.

        KEYWORD ARGUMENTS

            p - the coin flip probability of heads.  When the coin flip
                is heads, a passage is carved clockwise.  When the coin
                flip is tails, the row choice method is called to select
                a cell in the current long passageway.
                    (default: fair coin p=0.5)

            row_choice - a method which chooses one from a list of at
                least one cell.  The method takes two arguments, namely
                a State-compatible object and a non-empty list of cells.
                    (default: None - use OutWinder.random_choice)

                The provided methods are the same as for the inward
                winder:

                    OutWinder.random_choice (like Sidewinder)
                    OutWinder.first_choice (lazy outward/ccw binary
                        tree)
                    OutWinder.last_choice (lazy outward/cw binary tree)
                    OutWinder.median_choice (an averaged Sidewinder)
                    OutWinder.first_last_choice (lazy inward binary
                        tree)
                    OutWinder.cocktail_choice (lazy inward binary tree)

            exit_choice - a method which chooses one from a list of at
                least one cell.  The method takes two arguments, namely
                a State-compatible object and a non-empty list of cells.
                    (default: None - use OutWinder.random_choice)

            state - a State-compatible object or None.  If one is
                provided, the instance variable state.grid will be set
                to the value maze.grid, and the instance variable
                state.initialized will be set to False.
                    (default: None - use the Inwinder.State class)

            q - a coinflip probability used by some of the run-choice
                methods

            gofirst - switches the alternation in the cocktail shaker
                method

        NOTES

            Because there might be more than one outward exit, the
            method is slightly more complex than InWinder.on.

            The maze is easiest to solve starting at a cell incident to
            or atop the pole and ending at the outermost latitudinal
            row.  In other words, it is easier for the Minotaur to
            eacape from the maze than it is for Theseus to descend and
            locate the Minotaur.  On the other hand, if Theseus slays
            the Minotaur at the center of the maze, he has no need for
            Ariadne's ball of yarn.
        """
            # housekeeping
        outward = PolarGrid.OUTWARD
        outlen = len(PolarGrid.OUTWARD)
        grid = maze.grid

        if not state:
            state = cls.State()
        state.grid = grid             
        state.initialized = False

        if not row_choice:
            row_choice = cls.random_choice
        if not exit_choice:
            exit_choice = cls.random_choice

            # main

        rows = grid.rows
        lengths = grid.column_cells
        for i in range(rows):
            cols = lengths[i]
            curr = first = grid[(i, randrange(cols))]
            firsthit = True
            run = []
            outward_exits = {}
            while curr and (curr != first or firsthit):
                firsthit = False      # we make sure first is used
                prev = curr
                curr = curr[PolarGrid.CW]

                outward_exits[prev] = []
                for direction in prev.directions:
                    if direction[:outlen] == outward:
                        if prev[direction]:
                            outward_exits[prev].append(prev[direction])
                can_go_outward = bool(outward_exits[prev])
                can_go_forward = curr and curr != first

                if can_go_outward:
                    run.append(prev)
                can_go_outward = bool(run)

                if can_go_forward:
                    if can_go_inward:
                        if random() <= p:       # heads
                                # go forward
                            prev.link(curr)
                        else:                   # tails
                                # close out run and go inward
                            cell = row_choice(state, run)
                            nbr = exit_choice(outward_exits[cell])
                            cell.link(nbr)
                            run = []
                            outward_exits = {}
                else:                           # last in row
                    if can_go_inward:
                            # close out run and go inward
                        cell = row_choice(state, run)
                        nbr = exit_choice(outward_exits[cell])
                        cell.link(nbr)
                        run = []
                        outward_exits = {}

            # housecleaning
        return maze
        
# end of polar_grid.py
