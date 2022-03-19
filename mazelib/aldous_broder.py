"""aldous_broder.py - an unbiased spanning tree algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    The Aldous-Broder algorithm for creating an unbiased spanning
    tree on a connected grid starts with a random walk of the grid.
    The plain flavor of the algorithm records the first entrance
    to a cell.  The French vanilla flavor records the last exit.
    Both versions are passage carvers.

    If the grid is disconnected, the algorithm will fail by not
    halting.  With a bad random sequence, the algorithm may also
    fail to halt on a connected grid -- but this sort of failure
    is extremely rare.  The plain version of the algorithm collects
    cells into a subtree, quickly at first, and more slowly as the
    subtree grows in size.  The French vanilla version produces the
    entire tree only on completion of the random walk.

    The degree to which the resulting spanning tree maze is actually
    unbiased depends, of course, on the quality of the pseudorandom
    uniform deviates (or 'random numbers') used to produce the random
    walk.

BUGS

    There are some artificial conditions which can cause failures.

        1) The grid has a directed arc into a cell with no
           neighbors.  In this case, the algorithm aborts.

        2) The grid has a directed arc into a cell which is its
           own neighbor (loop) and has no other neighbors.  In
           neighbors.  In this case, the algorithm goes into an
           infinite loop.

    These are artificial since a grid is not supposed to contain
    loops or directed arcs.

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

class AldousBroder(object):
    """AldousBroder - implementation of the Aldous-Broder unbiased
        spanning tree algorithm
    """

    @classmethod
    def on(cls, maze, method, *args, **kwargs):
        """carve an unbiased spanning tree on a connected grid

        This is a filter.

        REQUIRED ARGUMENTS

            maze - a Maze object on a grid initialized as a passage
                carver

            method - the algorithm to use

                AldousBroder.plain    - first entrance, no bells
                AldousBroder.vanilla  - last exit, subtly different
                AldousBroder.blueberry- first entrance, but fancy
        """
        method(maze, *args, **kwargs)
        return maze

    @staticmethod
    def plain(maze, *args, **kwargs):
        """plain Aldous-Broder first entrance

        REQUIRED ARGUMENT

            maze

        KEYWORD ARGUMENTS

            start - an optional starting cell

        All other arguments are ignored.
        
        SIDE EFFECTS

            The maze is carved and the first-entrance lookup table
            is stored in the maze.

        EXAMPLE

                plain (first-entrance) Aldous-Broder
                    on a toroidal grid
                C                                   D
            A +---+---+---+---+---+---+   +---+---+---+ A
                  |               |   |   |       |    
              +---+---+   +   +   +   +   +   +---+   +
                      |   |   |                   |    
              +---+   +---+---+   +   +---+   +---+   +
              |           |       |       |       |   |
              +   +   +---+   +---+---+---+   +---+   +
              |   |   |           |       |   |       |
              +   +---+---+   +   +---+   +   +   +---+
              |       |       |   |                   |
              +---+---+   +---+   +---+---+   +   +---+
                              |   |       |   |   |    
            B +---+---+---+---+---+---+   +---+---+---+ B
                C                                   D
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!
        """
        first = kwargs.get('start', None)
        maze.first_entrance = \
            AldousBroder.simple_random_walk(maze.grid, start=first)
        for cell in maze.first_entrance:
            nbr = maze.first_entrance[cell]
            if nbr:
                cell.link(nbr)

    @staticmethod
    def vanilla(maze, *args, **kwargs):
        """vanilla Aldous-Broder last exit

        REQUIRED ARGUMENT

            maze

        KEYWORD ARGUMENTS

            start - an optional starting cell

        All other arguments are ignored.
        
        SIDE EFFECTS

            The maze is carved and the last-exit lookup table
            is stored in the maze.

        EXAMPLE

                    vanilla (last-exit) Aldous-Broder
                        on a toroidal grid
                C                                   D
            A +   +   +---+   +---+---+---+---+   +---+ A
              |   |   |       |       |   |           |
              +---+   +---+   +---+   +   +   +   +---+
              |   |   |           |       |   |       |
              +   +   +   +---+   +---+   +---+---+---+
                  |   |       |   |           |        
              +   +---+   +---+   +---+---+   +---+---+
              |   |       |   |   |               |   |
              +   +---+---+   +---+---+   +   +   +   +
                  |                   |   |   |        
              +   +---+---+   +   +---+   +---+---+   +
              |           |   |               |       |
            B +   +   +---+   +---+---+---+---+   +---+ B
                C                                   D
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!
        """
        first = kwargs.get('start', None)
        maze.last_exit = \
            AldousBroder.simple_random_walk2(maze.grid, start=first)
        for cell in maze.last_exit:
            nbr = maze.last_exit[cell]
            if nbr:
                cell.link(nbr)

    @staticmethod
    def blueberry(maze, *args, **kwargs):
        """first-entrance Aldous-Broder with breakpoints

        This method has two major purposes:
            1) step through the first-entrance algorithm to
               enable animations
            2) as a hook for a hybrid Aldous-Broder/Wilson
               algorithm

        REMARKS ON EXAMPLE

            In the example below using a 6x10 toroidal grid, we
            broke up the run into three phases, with the first
            two phases processing about half of the unvisited cells.

            Phase 1 visited 31 cells in 49 iterations, creating
            30 edges at a cost of about 1.6 iterations per edge.

            Phase 2 visited 16 cells in 110 iterations, creating
            16 more edges at a cost of about 6.9 iterations per
            edge.

            Phase 3 visited the remaining 14 cells in 215
            iterations, creating the last 14 edges at a cost of
            about 15.4 iterations per edge.

            In general, the random walk finds cells fast at first,
            but loses momentum as the number of unvisited cells
            gets small.

        EXAMPLE

                  blueberry (first-entrance) Aldous-Broder
                        on a toroidal grid

                        Phase 1
                      49 iterations
                      29 unvisited
                C                                   D
            A +---+---+---+---+---+   +   +---+---+---+ A
              |   |   |   |   |   |   |   |   |   |   |
              +---+---+---+---+---+   +---+---+---+---+
              |   |   |   |   |   |   |   |   |   |   |
              +---+---+---+---+---+   +---+---+---+---+
              |       |   |   |   |   |   |           |
              +---+   +---+---+---+   +---+---+   +   +
                  |   |                           |    
              +   +   +   +---+---+---+   +---+---+   +
              |   |       |   |   |   |   |       |   |
              +---+---+---+---+---+---+---+   +---+---+
              |   |   |   |                   |   |   |
            B +---+---+---+---+---+   +   +---+---+---+ B
                C                                   D
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 30
                      number of components:         k = 30
                      Euler characteristic: v - e - k = 0

                        Phase 2
                      110 iterations
                      13 unvisited
                C                                   D
            A +---+---+   +---+---+   +   +   +---+---+ A
              |   |   |       |   |   |   |   |   |   |
              +---+---+---+   +---+   +---+---+---+---+
              |   |   |   |   |               |   |   |
              +---+---+---+   +---+   +   +---+---+---+
              |       |   |   |   |   |   |           |
              +---+   +---+---+   +   +---+---+   +   +
                  |   |                           |    
              +   +   +   +---+---+   +   +---+---+   +
              |   |       |   |       |   |       |   |
              +   +---+---+---+---+---+---+   +   +---+
                  |   |                       |   |    
            B +---+---+   +---+---+   +   +   +---+---+ B
                        C                                   D
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 46
                      number of components:         k = 14
                      Euler characteristic: v - e - k = 0

                        Phase 3 - finish run...
                      215 iterations
                      0 unvisited
                      successful completion
                C                                   D
            A +   +   +   +---+---+   +   +   +---+---+ A
                  |   |       |   |   |   |   |        
              +---+   +---+   +   +   +---+---+   +   +
              |       |   |   |               |   |   |
              +---+---+   +   +---+   +   +---+---+---+
              |       |       |   |   |   |           |
              +---+   +---+---+   +   +---+---+   +   +
                  |   |                           |    
              +   +   +   +---+---+   +   +---+---+   +
              |   |       |           |   |       |   |
              +   +---+---+---+---+---+---+   +   +---+
                  |                           |   |    
            B +   +   +   +---+---+   +   +   +---+---+ B
                C                                   D
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!
        """
        grid = maze.grid
        debug = kwargs.get('debug')
        if kwargs.get('init'):
            maze.unvisited = set(grid.cells)
            maze.curr = kwargs.get('start', None)
            maze.blueberry = 'incomplete'
            if not maze.curr:
                maze.curr = choice(grid.cells)
            maze.unvisited.discard(maze.curr)
            if debug:
                print('AldousBroder.blueberry init')

            # breakpoints
        max_its = kwargs.get('max_its', float('inf'))
        max_its = max(1, max_its)
        min_cells = kwargs.get('min_cells', -1)
        min_cells = min(min_cells, 0.8 * len(maze.unvisited))

        n = 0         # number of iterations
        while maze.unvisited:
            n += 1

            nbr = choice(maze.curr.neighbors)
            if nbr in maze.unvisited:
                maze.curr.link(nbr)
                maze.unvisited.discard(nbr)
            maze.curr = nbr

                # breakpoint?
            if n >= max_its or len(maze.unvisited)<min_cells:
                if debug:
                    print(f'  {n} iterations')
                    print(f'  {len(maze.unvisited)} unvisited')
                return maze

        if debug:
            print(f'  {n} iterations')
            print(f'  {len(maze.unvisited)} unvisited')
            print('  successful completion')
        maze.blueberry = 'complete'
        return maze

    @staticmethod
    def simple_random_walk(grid, start=None):
        """perform a random walk of a grid, recording the first entrance

        REQUIRED ARGUMENTS

            grid - a connected grid (member of class Grid).  The walk will
                fail to halt if the grid is not connected.  The walk will
                abort if the starting cell is an isolated cell.

        KEYWORD ARGUMENTS

            start - an optional starting cell

        WALK TERMINATION

            The walk terminates when all cells have been visited.  Although
            this rarely happend, the walk may fail to terminate even though
            the grid is connected.

        RETURNS

            A directory mapping a cell to its first predecessor.
        """
        if not start:
            start = choice(grid.cells)

        first_entrance = {}
        unvisited = set(grid.cells)
        cell = start
        first_entrance[cell] = None
        unvisited.discard(cell)

        while unvisited:
            nbr = choice(cell.neighbors)
            unvisited.discard(nbr)
            if not nbr in first_entrance:
                first_entrance[nbr] = cell
            cell = nbr

        return first_entrance

    @staticmethod
    def simple_random_walk2(grid, start=None):
        """perform a random walk of a grid, recording the last exit

        REQUIRED ARGUMENTS

            grid - a connected grid (member of class Grid).  The walk will
                fail to halt if the grid is not connected.  The walk will
                abort if the starting cell is an isolated cell.

        KEYWORD ARGUMENTS

            start - an optional starting cell

        WALK TERMINATION

            The walk terminates when all cells have been visited.  Although
            this rarely happens, the walk may fail to terminate even though
            the grid is connected.)

        RETURNS

            A directory mapping a cell to its last successor.
        """
        if not start:
            start = choice(grid.cells)

        last_exit = {}
        unvisited = set(grid.cells)
        cell = start
        unvisited.discard(cell)

        while unvisited:
            nbr = choice(cell.neighbors)
            unvisited.discard(nbr)
            last_exit[cell] = nbr
            cell = nbr

        last_exit[cell] = None

        return last_exit

# end of aldous_broder.py
