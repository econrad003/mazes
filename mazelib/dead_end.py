"""dead_end.py - dead end tools
Copyright 2022 by Eric Conrad

IMPLEMENTS

    algorithm DeadEnds - for counting and listing
    algorithm DeadEndRemoval - for turning dead ends into cycles
        or into isolated cells

DESCRIPTION

    A dead end in an undirected maze is a cell with exactly one
    passage to another cell.  In graph theoretical language, a dead
    end in an undirected graph is a vertex of degree 1.

    This module provides algorithms for tallying dead ends and for
    eliminating them by turning them into parts of cycles.

REMARKS

    For a directed maze or graph, it gets a bit more complicated.

EXAMPLE

    1) dead ends on a uniformly random maze

       19 dead ends are marked with an 'X'.

        +---+---+---+---+---+---+---+---+---+---+
        |           |     X |             X | X |
        +   +   +   +   +---+   +---+---+---+   +
        | X | X |   |   | X |     X |           |
        +---+---+   +   +   +   +---+   +   +---+
        |     X |               | X | X |     X |
        +   +---+---+---+---+   +   +---+   +---+
        |               | X     |             X |
        +---+---+---+   +---+   +   +---+---+---+
        |                           | X | X | X |
        +   +---+---+   +   +   +---+   +   +   +
        |     X | X     | X |                   |
        +---+---+---+---+---+---+---+---+---+---+

    2) added passages to all dead ends

       Note that all former dead ends are cells of degree
       at least two.

        +---+---+---+---+---+---+---+---+---+---+
        |           |     X |             X   X |
        +   +   +   +   +   +   +---+---+   +   +
        | X | X |   |   | X |     X |           |
        +   +   +   +   +   +   +   +   +   +---+
        |     X |               | X | X |     X |
        +   +---+---+---+   +   +   +   +   +   +
        |               | X     |             X |
        +---+---+---+   +---+   +   +   +---+---+
        |                           | X   X   X |
        +   +---+---+   +   +   +---+   +   +   +
        |     X   X     | X                     |
        +---+---+---+---+---+---+---+---+---+---+

    3) added passages to dead ends, probability p=0.5

       The four dead ends that remain are starred.

        +---+---+---+---+---+---+---+---+---+---+
        |           |     * |             X   X |
        +   +   +   +   +---+   +---+---+---+   +
        | X   X |   |   | X       * |           |
        +---+---+   +   +   +   +---+   +   +---+
        |     * |                 X | X |     X |
        +   +---+---+---+---+   +   +   +   +   +
        |               | *     |             X |
        +---+---+---+   +---+   +   +---+---+---+
        |                             X | X   X |
        +   +---+---+   +   +   +---+   +   +   +
        |     X   X     | X                     |
        +---+---+---+---+---+---+---+---+---+---+

    4) N/S passages to dead ends, probability p=0.5

       Here ten dead ends remain.  The removal operation
       added a northward passage (if possible, or
       a southward passage otherwise,) to the other nine
       dead ends.

        +---+---+---+---+---+---+---+---+---+---+
        |           |     * |             X | X |
        +   +   +   +   +---+   +   +---+   +   +
        | * | X |   |   | * |     X |           |
        +---+   +   +   +   +   +---+   +   +---+
        |     X |               | * | X |     X |
        +   +---+---+---+---+   +   +   +   +   +
        |               | *     |             X |
        +---+---+---+   +---+   +   +   +---+---+
        |                           | X | * | * |
        +   +---+---+   +   +   +---+   +   +   +
        |     * | *     | * |                   |
        +---+---+---+---+---+---+---+---+---+---+

    5) roundabout passages to dead ends, probability p=0.5

       Here, with probability p=0.5, two adjacent dead
       ends were linked.  This has a tendency to create
       roundabout features in the maze.

        +---+---+---+---+---+---+---+---+---+---+
        |           |     X |             X   X |
        +   +   +   +   +   +   +---+---+---+   +
        | * | X |   |   | X |     X |           |
        +---+   +   +   +   +   +   +   +   +---+
        |     X |               | X | * |     * |
        +   +---+---+---+---+   +   +---+   +---+
        |               | *     |             X |
        +---+---+---+   +---+   +   +---+---+   +
        |                           | X   X | X |
        +   +---+---+   +   +   +---+   +   +   +
        |     X   X     | * |                   |
        +---+---+---+---+---+---+---+---+---+---+

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
from random import random, randrange, choice

class DeadEnds(object):
    """DeadEnds - dead ends bookkeeping for undirected mazes"""

    @classmethod
    def on(cls, maze):
        """return a list of dead ends in an undirected maze"""
        dead_ends = []
        for cell in maze.grid.each_cell():
            if len(cell.passages) == 1:
                dead_ends.append(cell)
        return dead_ends

    @classmethod
    def count(cls, maze):
        """the number of dead ends in an undirected maze"""
        return len(cls.on(maze))

class DeadEndRemoval(object):
    """for turning dead ends into cycles or isolates"""

    @classmethod
    def clip(cls, maze, p=1.0):
        """turn dead ends into isolated cells with probability p"""
        dead_ends = DeadEnds.on(maze)
        for cell in dead_ends:
            if p>=1 or random()<=p:
                for nbr in cell.passages:     # there is exactly one
                    cell.unlink(nbr)
        return maze

    @classmethod
    def on(cls, maze, p=1.0, method=None, **kwargs):
        """turn dead ends into cycles

            This is a simple filter that adds a list of dead-end cells
            to the argument list.

        REQUIRED ARGUMENTS

            maze - a Maze instance

        KEYWORD ARGUMENTS

            p - probability of carving a passage. If p >= 1, requested
                passages will always be carved.  If p < 0, no passages
                will be carved.  (If p = 0, then it is _very unlikely_
                that a passage will be carved.)

            method - a dead-end removal method.  These have the general
                form f(maze, cells, p=p, **kwargs) where cells is a list
                of cells of out-degree 0.  Currently supplied are:

                    DeadEndRemoval.add_passage
                        for each dead end, with probability p, add one
                        passage with target chosen at random.
 
                    DeadEndRemoval.directed_passage
                        for each dead end, where possible, with
                        probability p, add one passage in one of the
                        preferred target directions, chosen first-in
                        first-out.

                    DeadEndRemoval.roundabout
                        for each dead end, where possible, with
                        probability p, add one passage to a target
                        dead end cell, chosen at random.

            directions - a list of preferred carving directions for
                the DeadEndRemoval.directed_passage method.
        """
        maze.circuits = 0           # the number of passages carved
        if not method:
            method = cls.add_passage
        dead_ends = DeadEnds.on(maze)
        method(maze, dead_ends, p=p, **kwargs)
        return maze

    @staticmethod
    def add_passage(maze, cells, p=1.0, **kwargs):
        """rule - link dead ends with random neighbors"""
        for cell in cells:
            if len(cell.passages) > 1:
                continue          # no longer a dead end
            neighbors = []
            for nbr in cell.neighbors:
                if cell.isLinkedTo(nbr):
                    continue      # already linked
                neighbors.append(nbr)
            if not neighbors:
                continue          # no cell to link with

                # link to another cell with probability p
            if p>=1 or random()<=p:
                maze.circuits += 1
                nbr = choice(neighbors)
                cell.link(nbr)

    @staticmethod
    def directed_passage(maze, cells, p=1.0, directions=[], **kwargs):
        """rule - link dead ends with priority directions"""
        maze.circuits = 0
        if not directions:
            print("DeadEndRemoval.directed: Please supply directions")
            return maze

        for cell in cells:
            if len(cell.passages) > 1:
                continue          # no longer a dead end
            nbr = None
            for direction in directions:
                if not cell[direction]:
                    continue      # can't go thataway
                if cell.isLinkedTo(cell[direction]):
                    continue      # already linked
                nbr = cell[direction]
                break             # aha! found!
            if not nbr:
                continue          # no cell to link with

                # link to preferred cell with probability p
            if p>=1 or random()<=p:
                maze.circuits += 1
                cell.link(nbr)

    @staticmethod
    def roundabout(maze, cells, p=1.0, **kwargs):
        """rule - link dead ends with dead ends"""
        dead_ends = set(cells)
        maze.circuits = 0
        for cell in cells:
            if cell not in dead_ends:
                continue          # already visited
            neighbors = []
            for nbr in cell.neighbors:
                if cell.isLinkedTo(nbr):
                    continue      # already linked
                if nbr not in dead_ends:
                    continue      # not a dead end
                neighbors.append(nbr)
            if not neighbors:
                continue          # no dead ends to link with

                # link to another dead end with probability p
            if p>=1 or random()<=p:
                maze.circuits += 1
                nbr = choice(neighbors)
                cell.link(nbr)
                dead_ends.discard(cell)
                dead_ends.discard(nbr)

# end of dead_end.py
