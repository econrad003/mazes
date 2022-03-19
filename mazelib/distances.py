"""distances.py - find distances and shortest paths
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class Distances
    algorithm BellmanFord

EXAMPLES

    Both mazes were produced using Wilson's uniform random
    spanning tree algorithm.  They are easy mainly because they
    are small.  Some larger examples may be found in the images
    folder.

        distance from source S to target T: d = 14
        shortest path marked
        +---+---+---+---+---+---+---+---+---+---+
        |                       |       |   | T |
        +   +   +   +---+---+---+   +---+   +   +
        |   |   |       |           |       | * |
        +---+   +---+---+   +---+---+   +---+   +
        | *   *   *   *   *   *   *   *   *   * |
        +   +---+---+---+   +---+---+   +---+---+
        | * |       |           |               |
        +   +   +---+   +---+---+---+---+   +   +
        | * |   |       |   |   |   |   |   |   |
        +   +   +   +   +   +   +   +   +   +   +
        | S |       |   |                   |   |
        +---+---+---+---+---+---+---+---+---+---+

        distance from source S to target T: d = 18
        shortest path marked
        +---+---+---+---+---+---+---+---+---+---+
        |       |   |   |   |               | T |
        +   +   +   +   +   +   +---+---+---+   +
        |   |             *   *   *   *   * | * |
        +   +---+---+---+   +---+   +---+   +   +
        |   |     *   *   * |       |     * | * |
        +---+---+   +---+---+---+---+---+   +   +
        | *   *   * |           |   |     *   * |
        +   +---+   +   +---+   +   +---+---+   +
        | * |   |           |               |   |
        +   +   +   +   +   +---+   +   +---+   +
        | S |       |   |       |   |   |       |
        +---+---+---+---+---+---+---+---+---+---+

    Since the mazes are perfect (i.e. they are spanning trees,)
    the shortest path in both cases is unique.

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

    [2] "Dijkstra's algorithm".  in Wikipedia, 14 Mar. 2022.
        Web. Accessed 15 Mar. 2022.
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

    [3] "Bellman–Ford algorithm." in Wikipedia, 23 Feb. 2022.
        Web. 15 Mar. 2022.
        https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
 
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

class Distances(object):
    """distance information"""

    def __init__(self, maze, source, **kwargs):
        """constructor"""
        self._kwargs = kwargs
        self.maze = maze
        self.grid = maze.grid
        self._distances = {}
        self._predecessor = {}
        self._flagged = {}
        if not source:
            source = choice(grid.cells)
        self._source = source
        self[source] = 0
        self.errors = False

    @property
    def source(self):
        """the source cell"""
        return self._source

    def __getitem__(self, cell):
        """operator [] overload"""
        return self._distances.get(cell, float('inf'))

    def __setitem__(self, cell, dist):
        """operator []= overload"""
        self._distances[cell] = dist
        return dist

    def predecessor(self, cell):
        """a cell's predecessor in some shortest path from source"""
        return self._predecessor.get(cell, None)

    def set_predecessor(self, cell, prev):
        """set a cell's predecessor"""
        self._predecessor[cell] = prev
        return prev

    def flagged(self, cell):
        """is the cell flagged?"""
        return self._flagged.get(cell)

    def set_flags(self, cell, value):
        """flag the cell"""
        self._flagged[cell] = value

class BellmanFord(object):
    """the Bellman-Ford shortest path algorithm"""

    @classmethod
    def on(cls, maze, source=None, weighted=False):
        """a dispatcher for Bellman-Ford"""
        status = Distances(maze, source)
        return cls.weightedOn(status) if weighted \
            else cls.unweightedOn(status)

    @classmethod
    def unweightedOn(cls, status):
        """each arc has weight 1 - we are counting steps

        The algorithm reminds me of a children's game.  One person
        (the source) starts by choosing a partner from a group of
        people.  The couple splits, and finds partners from those
        standing out. Eventually no one is left standing out.

        If the maze is connected and has more than one cell, the
        source cell will have at least one linked neighbor, so
        there will be at least one cell which is exactly one step
        away from the source. If there are at least three cells,
        then the maze will have at least three cells (including the
        source) which are at most two steps from the source.  If v
        is the number of cells and the maze is connected, then all
        cells will be at most v-1 steps from the source cell.
        """
        grid = status.grid
        v = len(grid.cells)             # the number of vertices
        for _ in range(v-1):
            for cell in grid.each_cell():
                d = status[cell]
                if d == float('inf'):   # not yet visited
                    continue
                for nbr in cell.passages:
                    if d + 1 < status[nbr]:
                        status[nbr] = d + 1
                        status.set_predecessor(nbr, cell)
        return status

    @classmethod
    def weightedOn(cls, status):
        """each arc is weighted

        Here we have a complication.  If the weight of some arc is
        negative and that arc is in some cycle, then we will have
        some cells for which weighted distance is undefined.  Since
        most mazes are undirected, it would follow that a single
        negative weight would imply that distance is undefined at
        every cell in an undirected maze.
        """
        grid = status.grid
        v = len(grid.cells)             # the number of vertices
        for _ in range(v-1):
            for cell in grid.each_cell():
                d = status[cell]
                if d == float('inf'):   # not yet visited
                    continue
                for nbr in cell.passages:
                    w = cell.weight(nbr)
                    if d + w < status[nbr]:
                        status[nbr] = d + w
                        status.predecessor(nbr, cell)

            # check for a neigative-weight cycle
        for cell in grid.each_cell():
            d = status[cell]
            for nbr in cell.passages:
                w = cell.weight(nbr)
                if d + w < status[nbr]:
                    status.set_flag[nbr] = 'undefined distance'
                    status.errors = True

        if status.errors:
            print('WARNING: There is a negative-weight cycle')
            print('WARNING: Distance is undefined')
                # we protect against misuse of the distance function
                # but the predecessor function can still be misused
            self._save_distances = self._distances.copy()
            self._distances = {}

        return status

# end of distances.py
