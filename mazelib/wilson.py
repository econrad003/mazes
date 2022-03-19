"""wilson.py - an unbiased spanning tree algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    Wilson's algorithm for creating an unbiased spanning tree on a
    connected grid takes with a circuit-erased random walk starting
    at a random unvisited cell (the desert) and ending at a visited
    cell (somewhere civilized). The path taken (_i.e._ the trail
    minus any circuits) is then added to the emerging spanning tree.

    As with Aldous-Broder, there is no guarantee that the algorithm
    will terminate, but infinite loops are rare.

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

class Wilson(object):
    """Wilson - implementation of Wilson's unbiased spanning tree
        algorithm
    """

    @classmethod
    def on(cls, maze, debug=False):
        """carve an unbiased spanning tree on a connected grid

        REQUIRED ARGUMENTS

            maze - a Maze object on a grid initialized as a passage
                carver

        KEYWORD ARGUMENTS

            debug - if true, display progress information

        EXAMPLE

                    Wilson's algorithm on a Moebius strip grid

            Progress information:
                 1) 59 unvisited cells, 180 steps, path length 15
                 2) 45 unvisited cells, 7 steps, path length 6
                 3) 40 unvisited cells, 48 steps, path length 5
                 4) 36 unvisited cells, 7 steps, path length 4
                 5) 33 unvisited cells, 1 steps, path length 2
                 6) 32 unvisited cells, 11 steps, path length 8
                 7) 25 unvisited cells, 4 steps, path length 5
                 8) 21 unvisited cells, 2 steps, path length 3
                 9) 19 unvisited cells, 1 steps, path length 2
                10) 18 unvisited cells, 1 steps, path length 2
                11) 17 unvisited cells, 1 steps, path length 2
                12) 16 unvisited cells, 3 steps, path length 2
                13) 15 unvisited cells, 1 steps, path length 2
                14) 14 unvisited cells, 5 steps, path length 2
                15) 13 unvisited cells, 1 steps, path length 2
                16) 12 unvisited cells, 1 steps, path length 2
                17) 11 unvisited cells, 1 steps, path length 2
                18) 10 unvisited cells, 4 steps, path length 3
                19) 8 unvisited cells, 1 steps, path length 2
                20) 7 unvisited cells, 1 steps, path length 2
                21) 6 unvisited cells, 1 steps, path length 2
                22) 5 unvisited cells, 1 steps, path length 2
                23) 4 unvisited cells, 1 steps, path length 2
                24) 3 unvisited cells, 1 steps, path length 2
                25) 2 unvisited cells, 1 steps, path length 2
                26) 1 unvisited cells, 1 steps, path length 2

            Resulting maze:

            G +---+---+---+---+---+---+---+---+---+---+ A
                  |       |   |               |   |   |
            F +---+---+   +   +---+   +   +---+   +   + B
              |   |               |   |           |   |
            E +   +---+   +---+---+   +---+---+---+   + C
                  |           |           |            
            D +   +---+---+   +   +---+---+   +---+---+ D
                  |           |       |   |       |    
            C +   +   +   +   +   +---+   +---+   +   + E
              |       |   |   |       |           |   |
            B +   +---+---+   +   +---+---+   +---+   + F
              |       |       |               |        
            A +---+---+---+---+---+---+---+---+---+---+ G
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        NOTES ON EXAMPLE

            With each pass, the emerging spanning tree became a
            bit larger.  In general, the earlier passes extended
            the tree by more than later passes, but took more
            wasted steps in doing so.  In the first pass, 166 of
            the 180 steps (92%) ended in a circuit.  The second
            pass did much better, with only 2 of 7 steps (29%)
            wasted.  (Sometimes a person just happens to get
            teleported reasonably close and also happens to walk
            in a good direction.)  In the third pass, luck failed
            despite more visited cells to stumble onto -- 44 of
            of 48 steps (92%) ended in a circuit.

            But as the desert regions became smaller and more
            isolated from each other, luck became less of a
            factor.  In passes 15 through 26 (the final pass),
            there were no wasted steps in finding the already
            visited region.  In all but one of these passes
            (the exception: pass 18), the teleported explorer
            returned home in a single step.

        COMPARISON WITH ALDOUS-BRODER

            Aldous-Broder tends to pick up unvisited cells rapidly
            at first to add them to the maze.  As the unvisited
            regions become smaller and more scattered, fruitless
            wandering in the visited region becomes more common
            and progress slows considerably.

            With Wilson's algorithm, the situation is reversed.
            Progress is slow at first, but as the unvisited regions
            become smaller and more scattered, Wilson's algorithm
            becomes faster.

            Wilson's algorithm has one additional advantage over
            Aldous-Broder.  Each pass always adds at least one
            new unvisited cell to the maze -- in the code, we
            call that cell the oasis.  This advantage comes free
            of cost.
        """
        unvisited = set(maze.grid.cells)
        start = choice(maze.grid.cells)
        unvisited.discard(start)          # start of civilizarion

        while unvisited:
            path = cls.circuit_erased_walk(unvisited, debug=debug)
            for i in range(len(path) - 1):
                curr, step = path[i:i+2]
                curr.link(step)           # follow the path
                unvisited.discard(step)   # expand civilization

    @staticmethod
    def circuit_erased_walk(unvisited, debug=False):
        """one pass of Wilson's algorithm, read only

            "That's one small step for (a) man, one giant leap
            for mankind." -- Neil Armstrong, July 20, 1969
        """
        trail = {}
            # teleport to desert oasis
        oasis = choice(list(unvisited))
        trail[oasis] = None

        n = 0
        curr = oasis
        while curr in unvisited:          # still in the desert
            n += 1                        # step count
            step = choice(curr.neighbors)
            if step not in trail:         # someplace new
                trail[step] = curr
            curr = step                   # continue from here

            # find a path to the oasis
        path = []
        while curr:
            path.append(curr)
            curr = trail[curr]

        if debug:
            print(f'{len(unvisited)} unvisited cells,',
                  f'{n} steps,', f'path length {len(path)}')

        return path

# end of wilson.py
