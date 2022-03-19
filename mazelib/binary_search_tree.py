"""binary_search_tree.py - implementation of a binary tree algorithm
    using search techniques
Copyright 2022 by Eric Conrad

DESCRIPTION

    The algorithm implemented here uses searching techniques (like
    depth-first search to attempt to construct a binary spanning
    tree on an arbitrary grid.  It may sometimes fail (even on a
    rectangular grid) as it may sometimes paint itself into a
    proverbial corner.

BACKGROUND

    There are connected grids which have no binary spanning trees.
    Perhaps the simplest example is the grid in Figure 1 below:


                    +---+
                    | a |           Figure 1
                +---+---+---+       Grid G with no binary
                | b | x | d |       spanning tree
                +---+---+---+
                    | c |
                    +---+

    To see that no binary spanning tree is possible, note the cell
    marked with an 'x'.  It has four neighboring cells, and each of
    its neighbors has exactly one neighbor, namely the cell marked
    'x'.  Consider an arbitrary spanning tree T of grid G.  It must
    contain all five cells, and it must be connected.  So it must
    contain the four passages {a,x}, {b,x}, {c,x}, and {d,x}.  But
    those are, in fact all the available passages in grid G.  While
    these edges do form a tree and a spanning tree of grid G, they
    fail to form a binary tree as cells in a binary tree maze cannot
    have more than three passages, namely at most one to a parent and
    at most two to children.

    Any rectangular grid does have a binary spanning tree.  Perhaps
    the simplest way to construct one is to carve long corridors along
    each row and carve one long corridor along the first column.  In
    Figure 2, we have the result of this exceptionally lazy algorithm
    on a 3x5 rectangular grid:

              +---+---+---+---+---+
              | 5   B   C   D   E |    Figure 2
              +   +---+---+---+---+    Every rectangular grid has
              | 2   4   8   9   A |    a binary spanning tree
              +   +---+---+---+---+ 
              | r   1   3   6   7 |
              +---+---+---+---+---+

    In Figure 3, we show that that spanning tree in Figure 2 is
    indeed a binary tree by displaying it in the customary inverted
    tree format:

                          r             Figure 3
                         / \            The binary spanning tree of
                        1   2           Figure 2
                       /   / \
                      3   4   5
                      |   |   |
                      6   8   B
                      |   |   |
                      7   9   C
                          A   |
                              D
                              |
                              E

    It is easy to check that each node except 'r' in the rooted binary
    tree of Figure 3 has exactly one 1 parent and each node has at most
    two children.  The passages in the maze of Figure 2 are the edges in
    the rooted binary tree of Figure 3, so the maze is a binary spanning
    tree.

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
from maze_support import Stack, Queue, Unqueue

class DFSBinaryTree(object):
    """DFSBinaryTree - implementation of a binary tree passage
        carver using depth-first search

    EXAMPLE

        +---+---+---+---+---+---+---+---+---+---+
        |                               |       |
        +   +---+   +   +---+---+---+   +   +   +
        |       |   |   |       |   |   |   |   |
        +---+   +   +---+   +   +   +   +   +   +  The root cell is
        |       |   |       |   |   |       |   |  marked with an 'X'
        +   +---+   +   +---+   +   +---+---+   +
        |       |   |     X |   |           |   |
        +---+   +   +---+---+   +   +---+---+   +
        |       |   |           |               |
        +   +---+   +   +---+---+   +---+---+---+
        |       |       |                       |
        +---+---+---+---+---+---+---+---+---+---+
    Maze characteristic:
           number of nodes:         v = 60
           number of edges:         e = 59
      number of components:         k = 1
          Euler characteristic: v - e - k = 0
    """

    @classmethod
    def on(cls, maze, root=None, mark_root=False):
        """attempt to carve a binary tree on an grid

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell

            mark_root - if true, the first character of the
                representation is used to mark the cell
        """
        grid = maze.grid
        if not root:
            root = choice(grid.cells)
        if mark_root:
            root.text = repr(mark_root)[1]

        stack = Stack()
        stack.enter(None, root)
        visited = set([])

        while not stack.isEmpty:
            parent, cell = stack.serve()
            if cell in visited:
                continue        # already adopted

            if parent:
                    # cannot adopt 3 children (binary tree requirement)
                n = len(parent.passages)
                if n > 2:       # limit = 1 parent + 2 children
                    continue
                if parent == root and n > 1:
                    continue
                parent.link(cell)     # adoption is complete

            visited.add(cell)

                # now the cell applies to the adoption agency
                # some possibilities are found, but no guarantees
            neighbors = cell.neighbors
            shuffle(neighbors)
            for nbr in neighbors:
                stack.enter(cell, nbr)

        return maze

class BFSBinaryTree(object):
    """BFSBinaryTree - implementation of a binary tree passage
        carver using breadth-first search

    EXAMPLE

        +---+---+---+---+---+---+---+---+---+---+
        |                           |           |
        +---+   +   +   +   +   +   +   +---+---+
        |       |   |   |   |   | X             |
        +   +   +   +   +   +   +---+---+   +---+
        |   |   |   |   |   |           |       |
        +   +   +   +   +   +   +---+---+   +   +
        |   |   |   |   |   |   |           |   |
        +   +   +   +   +   +   +---+   +   +   +
        |   |   |   |   |   |   |       |   |   |
        +   +   +   +   +   +   +---+   +   +   +
        |   |   |   |   |   |   |       |   |   |
        +---+---+---+---+---+---+---+---+---+---+
        Maze characteristic:
               number of nodes:         v = 60
               number of edges:         e = 59
          number of components:         k = 1
          Euler characteristic: v - e - k = 0
    """

    @classmethod
    def on(cls, maze, root=None, mark_root=False):
        """attempt to carve a binary tree on an grid

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell

            mark_root - if true, the first character of the
                representation is used to mark the cell
        """
        grid = maze.grid
        if not root:
            root = choice(grid.cells)
        if mark_root:
            root.text = repr(mark_root)[1]

        queue = Queue()       # <-- this is the only real change
        queue.enter(None, root)
        visited = set([])

        while not queue.isEmpty:
            parent, cell = queue.serve()
            if cell in visited:
                continue        # already adopted

            if parent:
                    # cannot adopt 3 children (binary tree requirement)
                n = len(parent.passages)
                if n > 2:       # limit = 1 parent + 2 children
                    continue
                if parent == root and n > 1:
                    continue
                parent.link(cell)     # adoption is complete

            visited.add(cell)

                # now the cell applies to the adoption agency
                # some possibilities are found, but no guarantees
            neighbors = cell.neighbors
            shuffle(neighbors)
            for nbr in neighbors:
                queue.enter(cell, nbr)

        return maze

class BinarySearchTree(object):
    """BinarySearchTree - implementation of a binary tree passage
        carver using generalized search

    EXAMPLE 1

            binary spanning tree using random-first search

        The maze_support.Unqueue class was used.

        +---+---+---+---+---+---+---+---+---+---+
        |       |   |       |   |   |   |       |
        +---+   +   +   +---+   +   +   +   +---+
        |   |       |   |       |   |           |
        +   +---+   +   +   +---+   +   +---+---+
        |       |       |           |           |
        +   +   +   +---+   +---+---+---+   +---+
        |   |           |   |                   |
        +   +   +---+---+   +---+   +   +---+---+
        |   |                       |           |
        +---+   +   +   +---+---+   +---+   +---+
        |       |   | X         |       |       |
        +---+---+---+---+---+---+---+---+---+---+
        Maze characteristic:
               number of nodes:         v = 60
               number of edges:         e = 59
          number of components:         k = 1
          Euler characteristic: v - e - k = 0

    EXAMPLE 2

            binary spanning tree using a heap

        The edges were randomly weighted and the starting cell
        is incident to the edge of minimum weight, so apart from
        the limitation on the number of children, this is
        essentially Prim's minimum-weight spanning tree algorithm.

        (Open question: Is the resulting binary spanning tree
        necessarily a minimum-weight binary spanning tree?)

        +---+---+---+---+---+---+---+---+---+---+
        |                       |           |   |
        +---+   +   +---+---+---+   +---+   +   +
        |       |   |           |   |           |
        +---+   +   +   +   +---+---+   +---+   +
        |   |   |       |   |           |       |
        +   +   +---+---+   +---+---+   +   +---+
        |       |       |   |           |       |
        +   +   +   +   +   +---+   +   +---+---+
        |   |   | X |               |           |
        +---+   +   +---+---+---+---+---+   +---+
        |       |           |                   |
        +---+---+---+---+---+---+---+---+---+---+
        Maze characteristic:
               number of nodes:         v = 60
               number of edges:         e = 59
          number of components:         k = 1
          Euler characteristic: v - e - k = 0
    """

    @classmethod
    def on(cls, maze, root=None, mark_root=False, queue=None,
           priority=None):
        """attempt to carve a binary tree on an grid

        REQUIRED ARGUMENTS

            maze - a Maze object with an underlying grid initialized as
                a passage carver

        KEYWORD ARGUMENTS

            root - a starting cell

            mark_root - if true, the first character of the
                representation is used to mark the cell

            queue - a generized queue object
                The queue object must be duck-type compatible with
                class Unqueue.

            priority - a priority function (for use with heaps)
                The priority function takes the form:
                    priority(maze, cell1, cell2)
        """
        grid = maze.grid
        if not root:
            root = choice(grid.cells)
        if mark_root:
            root.text = repr(mark_root)[1]

        if queue == None:
            queue = Unqueue()

        if not priority:
            priority = lambda maze, cell1, cell2: random()

        queue.enter(None, root, priority=0)
        visited = set([])

        while not queue.isEmpty:
            parent, cell = queue.serve()
            if cell in visited:
                continue        # already adopted

            if parent:
                    # cannot adopt 3 children (binary tree requirement)
                n = len(parent.passages)
                if n > 2:       # limit = 1 parent + 2 children
                    continue
                if parent == root and n > 1:
                    continue
                parent.link(cell)     # adoption is complete

            visited.add(cell)

                # now the cell applies to the adoption agency
                # some possibilities are found, but no guarantees
            neighbors = cell.neighbors
            shuffle(neighbors)
            for nbr in neighbors:
                queue.enter(cell, nbr,
                            priority=priority(maze, cell, nbr))

        return maze

# end of binary_tree.py
