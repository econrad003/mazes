"""coloring.py - map coloring algorithms
Copyright 2022 by Eric Conrad

IMPLEMENTS

    algorithm GreedyColoring - a simple greedy coloring algorithm
    algorithm WelshPowell - a fancier greedy coloring algorithm
    algorithm TreeColor - a map coloring algorithm for trees and forests

    procedure applyText
    procedure applyPaint

    function validColoring

USAGE

    The coloring selection algorithms have the following basic usages:

        ARGUMENTS

            maze - a maze to color.

        KEYWORD ARGUMENTS

            start - an optional starting cell.

        RETURNS

            colormap - a directory of cells and their color numbers.

            count - the number of distinct colors. (The colors will
                range from 0 through one less than the count.)

    The color application functions have the following usage:

        ARGUMENTS

            colormap - the directory of cells and color numbers returned
                from a color selection method.

            colors - a list of colors to be used.

        EXCEPTIONS

            IndexError is raised if the list of colors does not have
            enough members to accommodate the colormap.

DESCRIPTION

    A map coloring of a maze is an assignment of colors to the cells
    of the maze in which any pair of cells which are joined by a
    passage are assigned distinct colors.

REMARKS

    A tree is 2-colorable:
        Taking at an arbitrary cell as the root, paint a cell with color
        0 if the depth is even; otherwise paint the cell with color 1.

    A perfect maze is 2-colorable:
        Taking the cells as vertices and the passages as edges, a
        perfect maze is just a spanning tree of its grid.  As a
        perfect maze is a tree, it follows that it is 2-colorable.

    A maze with a planar embedding is 4-colorable.  This is the famous
    4-color map theorem, proven by Wolfgang Haken and Kenneth Ira Appel
    in 1976. The same result holds on the surface of a
    sphere, a polyhedron, or a cylinder, as there are projections
    from the plane onto each of these surfaces.

    A maze with an embedding on a torus is 7-colorable

    If a graph (or maze) has a loop, that is a vertex (resp: cell)
    which is adjacent to itself (resp: connected to itself by a
    passage), then no coloring is valid.

BUGS

    The minimum coloring problem is hard. For example, determining
    whether a graph is 3-colorable is NP-complete.  Thus one should not
    expect any of these algorithms to return a minimal colormap. How well
    they perform in practice will depend on the maze and its underlying
    grid.

    The methods herein might not work consistenty for mazes with loops.
    (NB: Loops are circuits of length 1.  Circuits of length > 1 are not
    loops.)

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

    [2] "Heawood conjecture". Wikipedia, 17 October 2021. Web accessed
        19 March 2022.

          URL: https://en.wikipedia.org/wiki/Heawood_conjecture

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

from random import choice, shuffle, random
from maze_support import Stack, Heap

class GreedyColoring(object):
    """GreedyColoring - a greedy algorithm for map coloring

    DESCRIPTION

        At each step simply choose the lowest permissible color.

    BUGS

        1) A minimal coloring is not guaranteed.

        2) If there are one-way passages in the maze, the result might
           not be a valid coloring. Neighbors which are joined by a
           one-way passage might be assigned the same color.
    """

    @classmethod
    def on(cls, maze, start=None, queuing=None, **kwargs):
        """a greedy coloring method

        ARGUMENTS

            maze - a Maze instance

        KEYWORD ARGUMENTS

            start - an optional starting cell.

            queuing - a queue data structure such as Stack, Queue or
                Unqueue imported from maze_support.

        By default, if queuing is not specified, the algorithm is
        depth-first search as a stack is used.
        """
        grid = maze.grid
        queue = queuing if queuing else Stack()
        unvisited = set(grid.cells)
        if start:
            queue.enter(start)
        colormap = {}
        maxcolor = -1

        while unvisited:
                # retrieve an unvisited cell
            cell = choice(list(unvisited)) if queue.isEmpty \
                else queue.serve()[0]
            if not cell in unvisited:
                continue
            unvisited.discard(cell)

                # examine the neighborhood
            colors = set([])              # neigboring colors
            passages = cell.passages
            shuffle(passages)

            for nbr in passages:
                if nbr in unvisited:
                    queue.enter(cell)     # not yet painted
                else:
                    colors.add(colormap[nbr])

                # paint the cell with the first available color
            color = 0
            while color in colors:
                color += 1
            colormap[cell] = color
            maxcolor = max(maxcolor, color)

        return colormap, maxcolor+1

class WelshPowell(object):
    """GreedyColoring - a greedy algorithm for map coloring

    DESCRIPTION

        Here we first sort the cells in descending order by degree or
        valence.

        In each pass, we first assign a color to an uncolored cell
        of highest degree.  Proceeding through the list of uncolored,
        we assign the same color to cells not adjacent to a cell of
        the assigned color.

    BUGS

        1) A minimal coloring is not guaranteed.

        2) If there are one-way passages in the maze, the result might
           not be a valid coloring. Neighbors which are joined by a
           one-way passage might be assigned the same color.
    """
    @classmethod
    def on(cls, maze, **kwargs):
        """a more sophisticated greedy coloring method

        ARGUMENTS

            maze - a Maze instance

        KEYWORD ARGUMENTS

            ignored.
        """
        grid = maze.grid
        queue = Heap()
        unvisited = set(grid.cells)
        colormap = {}
        maxcolor = -1

        while unvisited:
                # put the unvisited cells in the heap
                #   We insure that the heap is unstable.
            for cell in unvisited:
                priority = -len(cell.passages)  # high degree, low pr
                priority += random() / 2        # unstable queue
                    # - valence <= priority <= 1/2 - valence
                queue.enter(cell, priority=priority)

                # remove a cell from the heap.  This will be a
                # cell of highest degree.
            first = queue.serve()[0]    # extract the cell
            maxcolor += 1               # an usused color
            colormap[first] = maxcolor  # this color is now used!
            unvisited.discard(first)

                # now we clear the rest of the heap
                # coloring if possible
            while not queue.isEmpty:
                cell = queue.serve()[0]
                ok_to_color = True
                for nbr in cell.passages:
                    color = colormap.get(nbr)
                    if color == maxcolor:
                        ok_to_color = False
                        break
                if ok_to_color:
                    colormap[cell] = maxcolor
                    unvisited.discard(cell)

        return colormap, maxcolor+1

class TreeColor(object):
    """start by assuming we have a tree or a forest..."""

    def on(maze, start=None, **kwargs):
        """will color a tree or forest in two colors"""
        from distances import BellmanFord

        grid = maze.grid
        unvisited = set(grid.cells)
        v = len(unvisited)
        distances = {}

            # first phase - get distances
        k = 0
        while unvisited:
            k += 1
            if not start:
                start = choice(list(unvisited))
            status = BellmanFord.on(maze, source=start)
            start = None

                # We access a hidden method to avoid traversing
                # the entire grid
            for cell in status._distances:
                distances[cell] = status[cell]
                unvisited.discard(cell)
        print(f'TreeColor: phase 1 complete - {k} components mapped')

            # second phase
        e = 0
        maxcolor = -1
        colormap = {}
        for cell in distances:
            color = distances[cell] % 2   # first guess
            colors = set([])
            for nbr in cell.passages:
                e += 1
                colors.add(colormap.get(nbr))
            if color in colors:     # conflict!
                color = 2           # we need a third color
                while color in colors:
                    color += 1      # maybe we still more colors
            colormap[cell] = color
            maxcolor = max(maxcolor, color)

        e = e // 2 if e % 2 == 0 else e / 2
        print(f'TreeColor: phase 2 complete - {v} vertices, {e} edges')

        return colormap, maxcolor+1

    # color application procedures

def applyText(colormap, colors):
    """set the cell's text based on the colormap"""
    for cell in colormap:
        cell.text = colors[colormap[cell]]

def applyPaint(colormap, colors):
    """set the cell's color based on the colormap"""
    for cell in colormap:
        cell.color = colors[colormap[cell]]

def validColoring(colormap):
    """determine whether a colormap is a valid coloring

    We assume here that every cell in the maze is in the colormap.
    """
    for cell in colormap:
        for nbr in cell.passages:
            if colormap[cell] == colormap[nbr]:
                return False
    return True

# end of coloring.py
