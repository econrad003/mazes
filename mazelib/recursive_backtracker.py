"""recursive_backtracker.py - depth-first search and related algorithms
    using search techniques
Copyright 2022 by Eric Conrad

DESCRIPTION

    The algorithm implemented here uses searching techniques (like
    depth-first search to construct a spanning tree on an arbitrary
    grid. Assuming that there is sufficient space for queuing
    operations and that the queuing operations are well-posed, the
    algorithm will succeed in finding a solution whenever the grid
    is connected.

    Maze lovers seem to have taken to the term `recursive backtracker'
    to describe depth-first search. (For example, see reference [1].)
    Under suitable changes of parameters, the algorithm can be used
    for breadth-first search, Prim's minimum-weight spanning tree,
    and other exotica.

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

from random import shuffle, choice, random
from maze_support import Stack, Queue, Unqueue, Heap

class SpanningSearchTree(object):
    """SpanningSearchTree - spanning tree using search
    """

    @classmethod
    def on(cls, maze, root=None, mark_root='', QueueClass=None,
           priority=None, shuffle_hood=True):
        """carve a spanning tree on an grid

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell. If none is ptovided, then a cell
                will be chosen at random.  (default: None)

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

            queuing - a queuing _class_ which is duck-type compatible
                with Stack, Queue or Heap in maze_support.  If queuing
                is None (the default), then maze_support.Stack will
                be used.

            priority - a priority function taking a maze and two cells
                as its arguments.  (default: None)

            shuffle_hood - if false, a cell's neighborhood will not be
                shuffled. (default: True)

        REMARKS

            If the default values are used for the keyword argument,
            then the algorithm is depth-first search.  Shuffling the
            neighborhood before stacking the neighbors produces a
            more interesting maze.
        """
        grid = maze.grid
        if not root:
            root = choice(grid.cells)
        if mark_root:
            root.text = repr(mark_root)[1]

        queue = QueueClass() if QueueClass else Stack()
        if not priority:
            priority = lambda maze, cell1, cell2: 1
        queue.enter(None, root, priority=0)
        visited = set([])

        while not queue.isEmpty:
            parent, cell = queue.serve()
            if cell in visited:
                continue        # already adopted

            if parent:
                parent.link(cell)     # adoption is complete
            visited.add(cell)

                # now the cell applies to the adoption agency
                # some possibilities are found, but no guarantees
            neighbors = cell.neighbors
            if shuffle_hood:
                shuffle(neighbors)
            for nbr in neighbors:
                queue.enter(cell, nbr,
                            priority=priority(maze, cell, nbr))

        return maze

class DFSSpanningTree(object):
    """DFSSpanningTree - spanning tree using depth-first search
                        (filter)

    This is the algorithm described in [1] as 'recursive backtracker'.
    The author notes that it is the same algorithm as the graph search
    algorithm generally known as 'depth-first search' or 'DFS'.
    """

    @classmethod
    def on(cls, maze, root=None, mark_root='', shuffle_hood=True):
        """carve a depth-first spanning search tree on an grid

        This is just a simple filter.

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell. If none is ptovided, then a cell
                will be chosen at random.  (default: None)

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

            shuffle_hood - if false, a cell's neighborhood will not be
                shuffled. (default: True)

        EXAMPLES

            In both examples, the starting cell is labelled 'r'.
            The first example uses shuffling.  The second example
            does not.

            DFS spanning tree on a rectangular grid
            +---+---+---+---+---+---+---+---+---+---+
            |                                       |
            +   +   +---+---+---+---+---+---+---+   +
            |   |   |         r |               |   |
            +   +   +   +---+---+---+---+   +---+   +
            |   |   |                   |   |       |
            +   +---+---+---+---+---+   +   +   +---+
            |           |           |   |           |
            +   +   +---+   +   +---+   +---+---+   +
            |   |           |       |       |   |   |
            +   +---+---+---+---+   +---+   +   +   +
            |                   |           |       |
            +---+---+---+---+---+---+---+---+---+---+
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

            DFS spanning tree (no shuffling)
            +---+---+---+---+---+---+---+---+---+---+
            |                                       |
            +   +---+---+---+---+---+---+---+---+   +
            |   |                                   |
            +   +   +---+---+---+---+---+---+---+---+
            |   |                                   |
            +   +---+---+---+---+---+---+---+---+   +
            |   |                                   |
            +   +   +---+---+---+---+---+---+---+---+
            |   |                                   |
            +   +---+---+---+---+---+---+---+---+   +
            | r |                                   |
            +---+---+---+---+---+---+---+---+---+---+
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

        BIAS

            Long twisting passages are characteristic of depth-first
            search.
        """
        return SpanningSearchTree.on(maze, root=root,
                                     mark_root=mark_root,
                                     QueueClass=Stack,
                                     priority=None,
                                     shuffle_hood=shuffle_hood)

class BFSSpanningTree(object):
    """BFSSpanningTree - spanning tree using breadth-first search
                        (filter)
    """

    @classmethod
    def on(cls, maze, root=None, mark_root='', shuffle_hood=True):
        """carve a breadth-first spanning search tree on an grid

        This is just a simple filter.

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - an optional starting cell.

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

            shuffle_hood - if false, don't shuffle the neighborhoods.

        EXAMPLES

            In both examples, the starting cell is labelled 'r'.
            The first example uses shuffling.  The second example
            does not.

                      BFS spanning tree on a rectangular grid
                +---+---+---+---+---+---+---+---+---+---+
                |                                       |
                +---+---+---+---+---+---+---+   +---+---+
                |                             r         |
                +---+---+---+---+---+---+---+   +---+---+
                |                                       |
                +---+---+---+---+---+---+---+   +---+---+
                |                                       |
                +---+---+---+---+---+---+   +   +---+---+
                |                           |           |
                +---+---+---+---+---+---+   +   +---+---+
                |                           |           |
                +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

                    BFS spanning tree (no shuffling)
                +---+---+---+---+---+---+---+---+---+---+
                |   |   |   |   |   |   |   |   |   |   |
                +   +   +   +   +   +   +   +   +   +   +
                | r                                     |
                +   +---+---+---+---+---+---+---+---+---+
                |                                       |
                +   +---+---+---+---+---+---+---+---+---+
                |                                       |
                +   +---+---+---+---+---+---+---+---+---+
                |                                       |
                +   +---+---+---+---+---+---+---+---+---+
                |                                       |
                +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        BIAS

            Breadth-first search favors passages the branch very early,
            much like a spider web.
        """
        return SpanningSearchTree.on(maze, root=root,
                                     mark_root=mark_root,
                                     QueueClass=Queue,
                                     priority=None,
                                     shuffle_hood=shuffle_hood)

class RFSSpanningTree(object):
    """RFSSpanningTree - spanning tree using random-first search
                        (filter)

    EXAMPLE

                  random-first search (RFS) spanning tree
            +---+---+---+---+---+---+---+---+---+---+
            |   |   |               |           |   |
            +   +   +---+---+   +---+---+   +---+   +
            |   |   |   |       |           |       |
            +   +   +   +---+   +---+   +   +---+   +
            |   |       |           |   |   |       |
            +   +---+   +---+   +---+---+   +---+   +
            |                                 r     |
            +   +---+---+   +   +   +---+   +   +---+
            |   |           |   |   |       |       |
            +---+---+   +   +---+---+---+   +---+   +
            |           |   |                   |   |
            +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

    The choice of a random queued cell in the frontier will
    tend to produce more even branching than breath-first search
    (using the first queued item) or depth first search (using
    the last queued item).
    """

    @classmethod
    def on(cls, maze, root=None, mark_root=''):
        """carve a random-first spanning search tree on an grid

        This is just a simple filter.

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell. If none is ptovided, then a cell
                will be chosen at random.  (default: None)

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

        NOTE

            Shuffling of neighborhoods is unnecessary and thus not
            supported.
        """
        return SpanningSearchTree.on(maze, root=root,
                                     mark_root=mark_root,
                                     QueueClass=Unqueue,
                                     priority=None,
                                     shuffle_hood=False)

class Prim(object):
    """Prim - Prim's minimum-weight spanning tree algorithm
                        (filter)

    EXAMPLE

                Prim's minimum weight spanning tree
        +---+---+---+---+---+---+---+---+---+---+
        |       |       |   |                   |
        +   +---+   +---+   +---+   +   +---+---+
        |       | r         |       |           |
        +   +---+   +---+---+---+   +---+---+---+
        |   |   |   |   |   |   |           |   |
        +   +   +   +   +   +   +   +   +   +   +
        |       |               |   |   |   |   |
        +   +---+---+   +---+   +   +   +---+   +
        |                   |       |           |
        +---+---+   +   +   +---+   +   +---+   +
        |           |   |       |   |       |   |
        +---+---+---+---+---+---+---+---+---+---+
                Maze characteristic:
                   number of nodes:         v = 60
                   number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!
                Weight of maze: 83.2232387300603
                Weight per edge: 1.4105633683061067

    Edge weights in the simulation were uniformly distributed
    in the interval [1, 2].  The starting cell 'r' was incident
    to a least-weight edge.
    """

    @classmethod
    def on(cls, maze, root=None, mark_root='', priority={}):
        """carve a minimum-weight spanning tree on an grid

        This is a filter.

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - an optional starting cell.

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

            priority - a dictionary of priorities.  The keys are
                undirected edges (frozenset([cell1, cell2])). The
                values are positive real numbers.

        SIDE EFFECTS

            The Maze object will have a copy of the priority dictionary
            and the maximum priority (with minimum 1) that was given as
            input.
        """

        def prf(maze, cell1, cell2):
            """a priority function"""
            key = frozenset([cell1, cell2])
            if not key in maze.priority:
                maze.priority[key] = maze.max_priority + random()
            return maze.priority[key]

            # housekeeping
        max_priority = 1
        for pr in priority.values():
            if pr > max_priority:
                max_priority = pr

        maze.priority = priority.copy()
        maze.max_priority = max_priority
        
        return SpanningSearchTree.on(maze, root=root,
                                     mark_root=mark_root,
                                     QueueClass=Heap,
                                     priority=prf,
                                     shuffle_hood=False)

class FalsePrim(object):
    """FalsePrim - a spanning tree algorithm using vertex weights
                        (filter)
    """

    @classmethod
    def on(cls, maze, root=None, mark_root='', priority={}):
        """carve a best-first spanning search tree on an grid

        This is a filter.

        In [1], this algorithm is called "vertex-Prim".

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - an optional starting cell.

            mark_root - if true, the first character of the
                representation is used to mark the starting cell.

            priority - a dictionary of priorities.  The keys are
                vertices (cell). The values are positive real numbers.

        REMARK

            The vertex-weight of the result is simply the sum of the
            weights of the vertices.  The sum over the cells of the
            weights of the vertices is constant, independent of
            the choice of spanning tree. 

            To get a better sense of what the vertex weights mean, one
            must multiply the weight times the degree of the cell and
            sum over the cells.  (This greedy algorithm does not
            necessarily minimize this sum.)  Since edges are counted
            twice, we would typically divide by 2.

            A second interpretation is to take a sum over the edges of
            the lower weight endpoint.  Here the idea is to associate
            each wall of the grid with two antiparallel directed arcs,
            each weighted with the weight of the target endpoint.
            (There is no guarantee that the lower-weighted arc will be
            the one chosen to guide the carving of the passage, so,
            again, this second sum is not necessarily minimized.)

        AMBIGUITY

            The algorithm can lead to more than one solution even
            when the vertex weights are unique.

            To see this consider the triangle graph on 3 vertices,
            labelled and weighted 1, 2 and 3:

                1 --- 2     Step 1: choose the least weight vertex.
                 \   /           (Choose vertex 1)
                   3        Step 2: take an available edge from a
                                 visited vertex to the least weight
                                 frontier vertex.
                                (Choose edge 1--2 to vertex 2)
                Step 3: repeat step 2
                   (Choose either edge 1--3 or 2--3 to vertex 3)

            So depending on priority queue implementation, the spanning
            tree is either:                     or:

                1---2                           1---2
                 \                                 /
                  3                               3

            If we look at the two sums proposed above, we have:

                      (weight x degree) / 2, summed over vertices
                (2x1 + 2 + 3)/2 = 3.5     (1+ 2x2 + 3)/2 = 4

                          lower weight, summed over edges
                1 + 1 = 2                       1 + 2 = 3

            A third spanning tree is possible for this configuration,
            but it is rejected by the algorithm.  Just for comparison,
            and perhaps also inspiration:

                1   2   weight-degree:  (2x3 + 1 + 2)/2 = 4.5
                 \ /    lower weight:   1 + 2 = 3
                  3

        EXAMPLE

                False Prim spanning tree (using cell weights)
            +---+---+---+---+---+---+---+---+---+---+
            |   |       |     r                     |
            +   +---+   +---+   +   +   +   +   +---+
            |   |   |       |   |   |   |   |   |   |
            +   +   +   +---+---+---+   +---+---+   +
            |               |   |           |       |
            +---+---+   +---+   +---+   +---+---+   +
            |   |   |   |   |               |   |   |
            +   +   +   +   +---+   +   +---+   +   +
            |                       |               |
            +---+   +   +   +   +   +   +   +   +   +
            |       |   |   |   |   |   |   |   |   |
            +---+---+---+---+---+---+---+---+---+---+
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!
                Weight of maze: 84.37440600466697
                Weight per cell: 1.4062401000777827
                Alternate weight: 75.20127338171999
                Weight per edge: 1.2745978539274574

            The first weight is half of the sum taken over the cells of
            the product of the cell's degree times the weight of the
            cell.  We divide by two to take into account the fact that
            each edge is counted twice in the sum.

            The lower weight is the sum taken over the edges of the
            weight of the edge's lower-weight endpoint.  (This will
            necessarily be less than or equal to -- and almost always
            less than the first weight.  The exception is that equality
            will hold if and only if each cell is of equal weight.)

            It is unlikely that either quantitity will be minimized
            by the algorithm.

        SIDE EFFECTS

            The Maze object will have a copy of the priority dictionary
            and the maximum priority (minimum: 1) that was given in the
            input.
        """

        def prf(maze, cell1, cell2):
            """a priority function"""
            if not cell2 in maze.priority:
                maze.priority[cell2] = maze.max_priority + random()
            return maze.priority[cell2]

            # housekeeping
        min_priority = float('inf')
        max_priority = 1
        lowcell = None
        for cell, pr in priority.items():
            if pr > max_priority:
                max_priority = pr
            if pr < min_priority:
                min_priority = pr
                lowcell = cell

        if not root:
            root = lowcell      # incident to least-weight edge

        maze.priority = priority.copy()
        maze.max_priority = max_priority
        
        return SpanningSearchTree.on(maze, root=root,
                                     mark_root=mark_root,
                                     QueueClass=Heap,
                                     priority=prf,
                                     shuffle_hood=False)

# end of recursive_backtracker.py
