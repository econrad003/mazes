"""aldous_broder_wilson.py - an hybrid spanning tree passage carver
    based on the Aldous-Broder first-entrance algorithm and Wilson's
    algorithm
Copyright 2022 by Eric Conrad

IMPLEMENTS

    HybridABW - a hybrid using Aldous-Broder and Wilson

DESCRIPTION

    Here we use the advantages of Aldous-Broder and Wilson to create
    a faster algoithm to create relatively uniform spanning trees.

PRECONDITIONS

    The grid must not contain loops (a wall between a cell and itself)
    or directed walls.

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
from wilson import Wilson

class HybridABW(object):
    """HybridABW - start with Aldous-Broder and finish with Wilson"""

    @classmethod
    def on(cls, maze, start=None, density=0.5, debug=None):
        """hybrid Aldous-Broder/Wilson

        REQUIRED ARGUMENTS

            maze - a maze to be carved with its grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            start - an optional cell to start the random walk.

            density - when the portion of cells in the unvisited region
                drops below this this ratio, the algorithm switches from
                random walk (Aldous-Broder) to circuit-erased random
                walk (Wilson).

                    A density of 0 or less implies pure Aldous-Broder.

                    A density of 1 or more implies pure Wilson.

            debug - if true, the method will provide some progress
                reporting

        EXAMPLE 1

                    the hybrid ABW algorithm
                       on a cylindrical grid
            cutoff density: 50%

                            log
            HybridABW start random walk
              random walk 62 iterations
              29 unvisited
            HybridABW start circuit-erased random walks
              29 unvisited cells, 8 steps, path length 5
              25 unvisited cells, 2 steps, path length 3
              23 unvisited cells, 3 steps, path length 2
              22 unvisited cells, 3 steps, path length 4
              19 unvisited cells, 9 steps, path length 2
              18 unvisited cells, 1 steps, path length 2
              17 unvisited cells, 3 steps, path length 4
              14 unvisited cells, 3 steps, path length 2
              13 unvisited cells, 2 steps, path length 3
              11 unvisited cells, 1 steps, path length 2
              10 unvisited cells, 1 steps, path length 2
              9 unvisited cells, 5 steps, path length 2
              8 unvisited cells, 4 steps, path length 3
              6 unvisited cells, 1 steps, path length 2
              5 unvisited cells, 1 steps, path length 2
              4 unvisited cells, 1 steps, path length 2
              3 unvisited cells, 1 steps, path length 2
              2 unvisited cells, 1 steps, path length 2
              1 unvisited cells, 1 steps, path length 2

                            result
            A +---+---+---+---+---+---+---+---+---+---+ A
                  |   |       |                        
              +---+   +---+   +   +   +   +---+---+   +
                      |       |   |   |       |   |    
              +   +---+   +---+   +---+---+   +   +   +
              |   |   |                   |       |   |
              +---+   +   +---+---+---+---+   +   +   +
              |               |       |       |   |   |
              +---+---+   +---+---+   +   +   +   +---+
                              |           |   |   |    
              +---+   +   +---+   +---+   +   +   +   +
                  |   |   |       |       |   |   |    
            B +---+---+---+---+---+---+---+---+---+---+ B
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        EXAMPLE 2
    
                    The hybrid ABW algorithm
                      on a cylindrical grid

            cutoff density: 75%

                            log
            HybridABW start random walk
              random walk 45 iterations
              44 unvisited
            HybridABW start circuit-erased random walks
              44 unvisited cells, 16 steps, path length 7
              38 unvisited cells, 21 steps, path length 12
              27 unvisited cells, 1 steps, path length 2
              26 unvisited cells, 1 steps, path length 2
              25 unvisited cells, 1 steps, path length 2
              24 unvisited cells, 1 steps, path length 2
              23 unvisited cells, 4 steps, path length 3
              21 unvisited cells, 7 steps, path length 4
              18 unvisited cells, 1 steps, path length 2
              17 unvisited cells, 1 steps, path length 2
              16 unvisited cells, 2 steps, path length 3
              14 unvisited cells, 1 steps, path length 2
              13 unvisited cells, 1 steps, path length 2
              12 unvisited cells, 1 steps, path length 2
              11 unvisited cells, 1 steps, path length 2
              10 unvisited cells, 3 steps, path length 2
              9 unvisited cells, 1 steps, path length 2
              8 unvisited cells, 1 steps, path length 2
              7 unvisited cells, 1 steps, path length 2
              6 unvisited cells, 1 steps, path length 2
              5 unvisited cells, 1 steps, path length 2
              4 unvisited cells, 1 steps, path length 2
              3 unvisited cells, 1 steps, path length 2
              2 unvisited cells, 1 steps, path length 2
              1 unvisited cells, 1 steps, path length 2

                            result
            A +---+---+---+---+---+---+---+---+---+---+ A
              |               |       |   |           |
              +---+   +---+   +   +---+   +---+   +   +
                  |       |                   |   |    
              +   +   +---+---+---+   +---+---+---+   +
              |               |       |           |   |
              +---+   +---+---+   +   +   +   +---+---+
              |           |   |   |   |   |           |
              +---+   +   +   +---+   +   +   +---+---+
                  |   |   |   |           |            
              +   +   +   +   +---+   +   +---+   +   +
              |   |   |           |   |   |       |   |
            B +---+---+---+---+---+---+---+---+---+---+ B
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        NOTES ON THE EXAMPLES

            In example 1, the cutoff density was 0.5 or 50%.  62
            random walk steps reduced the unvisited region from
            59 of 60 cells to 44 cells.  So 30 of the 62 steps
            were productive (52% waste).  The circuit-erased
            random walks were generally very productive -- the
            most notable outlier was at 19 unvisited cells where
            a walk of 9 steps only produced a path of length 2,
            reducing the unvisited region by just 1 cell (waste:
            89%).  In 13 of the 19 circuit-erased walks, there
            was no waste at all.

            In example 2, the cutoff density was 0.75 or 75%.  45
            random walk steps reduced the unvisited region from
            59 of 60 cells to 44 cells.  So 15 of the 45 steps
            were productive (67% waste).  The first two
            circuit-erased random walks were notably inefficient:
                  44 unvisited cells, 16 steps, path length 7
                      16 steps to get 6 cells (waste: 63%)
                  38 unvisited cells, 21 steps, path length 12
                      21 steps to get 11 cells (waste: 48%)
            Twenty of the twenty-five circuit-erased walks had no
            waste at all.

            These results are not statistically significant and are
            provided solely for illustration purposes.  Actual
            results will vary from run to run, and will depend on
            both the number of cells in the grid and the connectivity
            of the grid.
        """
        grid = maze.grid

            # initialization

        unvisited = set(grid.cells)
        curr = start if start else choice(grid.cells)
        unvisited.discard(curr)
        if debug:
            print('HybridABW start random walk')

            # breakpoint
        min_cells = density * len(grid.cells)

            # Aldous-Broder first-entrance
        n = 0                   # number of passes
        while unvisited:
                # breakpoint?
            if len(unvisited) < min_cells:
                break           # switch to circuit erased walk

            n += 1
            nbr = choice(curr.neighbors)
            if nbr in unvisited:
                curr.link(nbr)
                unvisited.discard(nbr)
            curr = nbr

            # At this point, we are set up for circuit-erased
            # random walks
        if debug:
            print(f'  random walk {n} iterations')
            print(f'  {len(unvisited)} unvisited')
            print('HybridABW start circuit-erased random walks')

        while unvisited:
            path = Wilson.circuit_erased_walk(unvisited, debug=debug)
            while len(path) > 1:
                curr = path.pop(0)
                step = path[0]
                curr.link(step)           # follow the path
                unvisited.discard(step)   # expand civilization

        return maze

# end of aldous_broder_wilson.py
