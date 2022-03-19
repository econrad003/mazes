"""maze.py - implementation of the Maze class
Copyright 2022 by Eric Conrad

DESCRIPTION

    The grid maintains topology and homology of the maze, that is,
    the vertices, edges and faces which are embedded on a plane, a
    a torus, or some other manifold.

NOTE

    The Maze class is a stub.  Fancier classes my be derived from
    this class.

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

from random import choice

class Maze(object):
    """Maze - implementation of a maze base class"""

        # initialization

    def __init__(self, grid, *args, **kwargs):
        """constructor

        REQUIRED ARGUMENTS

            grid - a grid object

        OPTIONAL ARGUMENTS

            Reserved for subclasses

        KEYWORD ARGUMENTS

            Reserved for subclasses
        """
        self._grid = grid
        self._args = args
        self._kwargs = kwargs
        self.sketcher = None      # sketch interface

        self.initialize()
        self.configure()

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    @property
    def grid(self):
        """return the grid object"""
        return self._grid

    def __str__(self):
        """string form"""
        return str(self.grid)

    def clone(self):
        """clone a maze"""
        grid = self.grid.clone()
        MazeClass = self.__class__
        args = self._args
        kwargs = self._kwargs
        return MazeClass(grid, *args, **kwargs)

    @property
    def components(self):
        """returns the set of components"""
        bag = {}          # principal cell : component of node
        cells = {}        # cell : principal cell

            # housekeeping
            #   The initial assumption is that the maze is discrete,
            #   that is, each cell is in a component by itself.
        for cell in self.grid.each_cell():
            bag[cell] = set([cell])
            cells[cell] = cell

            # main loop
            #   We search to find the components
        stack = list(self.grid.cells)
        while stack:
            cell = stack.pop()
            label = cells[cell]
            for nbr in cell.passages:
                owner = cells[nbr]
                if owner == label:
                    continue
                for item in bag[owner]:
                    bag[label].add(item)
                    cells[item] = label
                del bag[owner]

            # housecleaning
            #   Just return the components
        return list(bag.values())

        # Euler characteristic

    @property
    def v(self):
        """number of nodes"""
        return len(self.grid._cells)

    @property
    def e(self):
        """number of edges"""
        n = 0
        for cell in grid.each_cell():
            passages = set(cell.passages)
            n += len(passages)
            if cell in passages:
                n += 1        # loops are counted twice

            #     Nota bene!  Note well!
            # -----------------------------------------------------
            # All edges were counted twice, once at each endpoint.
            # (Loops were counted with multiplicity).
            #
            # Arcs (arc = directed edge), if any, were counted just
            # once at the source.
            #
            # If n is even (and it will be if there are no arcs),
            # then we return type int.
            #
            # If there are an odd number of arcs, then we return
            # type float.  If the number of arcs is even, we
            # nonetheless return type int. If there are arcs in the
            # maze, then the result isn't very useful.  But it is
            # what it is!
            #
        n = n // 2 if n % 2 else n / 2    # return int if possible
        return n

    @property
    def f(self):
        """number of faces - undefined"""
        cls = self.__class__
        gridcls = self.grid.__class__
        print('---------------------------------------------------')
        print(f'INFO: Property {cls.__name__}.f is undefined.')
        print(f'INFO: Did you mean {gridcls.__name__}.f?')
        print('---------------------------------------------------')
        raise ValueError(f'{cls.__name__} does not admit faces')

    @property
    def k(self):
        """number of grid components"""
        return len(self.components)

    @property
    def Euler_chi(self):
        """Euler characteristic"""
        return self.v - self.e - self.k

    def sketch(self, filename=None, show=True):
        """filter for sketching"""
        grid = self.grid
        grid.sketch(self.sketcher, filename, show)

# end of maze.py
