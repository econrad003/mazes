"""hunt_kill.py - the hunt and spanning tree algorithm
Copyright 2022 by Eric Conrad

DESCRIPTION

    The Aldous-Broder algorithm for creating a uniform or unbiased
    spanning is easy to code, but has some performance drawbacks.
    Perhaps the key drawback is that the algorithm spends a lot of
    unproductive time passing through cells that (in the first
    entrance form of the algorithm) have already been visited or
    (in the last exit form) will be visited again.

    In the kill phase, the hunt and kill algorithm restricts itself
    to a random walk which steps only on unvisited cells.  (Imagine
    a door closing behind you as you step into the unknown.)  But
    eventually the walk will reach a cell with no unvisited neighbors.
    At this point, the algorithm goes into a hunt phase.

    The frontier is the set of unvisited cells with a visited
    neighbor.  In the hunt phase, the algorithm searches for a
    frontier cell.  Finding one, it links the cell to its visited
    neighbor and resumes the kill.

IMPLEMENTATION

    The kill phase is straightforward.  It is the hunt phase where
    some choices need to be made.

    (1) Scan the visited cells in some order to find one with an
        unvisited neighbor; or

    (2) As cells are added to the visited region, keep track of
        frontier cells in some sort of queue, and find an unvisited
        cell with a visited neighbor in this queue.


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

from random import randrange, choice
from maze_support import Unqueue

class HuntAndKill(object):
    """HundAndKill - hunt and kill algorithm implementation"""

    class State(object):
        """state information for huntnd kill"""

        def __init__(self, maze, start=None, debug=False):
            """constructor"""
            self.grid = grid = maze.grid
            self.frontier = Unqueue()
            self.debug = debug

            self.unvisited = set(grid.cells)
            self.curr = start if start else choice(grid.cells)
            self.unvisited.discard(self.curr)

            self.visited = set([self.curr])

    @classmethod
    def on(cls, maze, start=None, use_frontier=True, debug=False,
           no_shuffle=False):
        """hunt and kill algorithm

        REQUIRED ARGUMENTS

            maze - a Maze object on a grid initialized as a passage
                carver

        KEYWORD ARGUMENTS

            start - a starting cell

            use_frontier - if true, the frontier heap will be used
                for hunting, otherwise the unvisited cells will be
                shuffled and scanned.

            no_shuffle - if true, 'use_frontier' is ignored and the
                unvisited cells will be scanned without shuffling

            debug - if true, display pass information

        EXAMPLE 1

                      hunt and kill
                       using heap

            (log)
            kill phase: 108 candidate cells, 30 added to tree,
                39 added to heap.
            hunt phase: 1 cells removed from heap
            kill phase: 57 candidate cells, 15 added to tree,
                10 added to heap.
            hunt phase: 1 cells removed from heap
            kill phase: 3 candidate cells, 0 added to tree,
                0 added to heap.
            hunt phase: 1 cells removed from heap
            kill phase: 6 candidate cells, 1 added to tree,
                0 added to heap.
            hunt phase: 2 cells removed from heap
            kill phase: 15 candidate cells, 4 added to tree,
                1 added to heap.
            hunt phase: 1 cells removed from heap
            kill phase: 15 candidate cells, 4 added to tree,
                0 added to heap.
            hunt phase complete:  44 cells removed from heap

            +---+---+---+---+---+---+---+---+---+---+
            |       |   |           |               |
            +   +   +   +   +   +   +   +---+---+   +
            |   |       |   |   |       |   |       |
            +   +---+   +   +   +   +---+   +   +---+
            |   |       |   |   |       |       |   |
            +---+   +---+   +   +---+   +---+---+   +
            |       |       |   |       |       |   |
            +   +---+---+---+   +   +---+   +   +   +
            |   |           |   |           |       |
            +   +   +   +   +   +---+---+---+---+   +
            |       |   |       |                   |
            +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        EXAMPLE 2


            
                    hunt and kill
                  random pick scan

            (log)
            kill phase: 103 candidate cells, 28 added to tree.
            hunt phase: 11 cells scanned
            kill phase: 35 candidate cells, 9 added to tree.
            hunt phase: 4 cells scanned
            kill phase: 19 candidate cells, 5 added to tree.
            hunt phase: 4 cells scanned
            kill phase: 28 candidate cells, 7 added to tree.
            hunt phase: 3 cells scanned
            kill phase: 19 candidate cells, 5 added to tree.
            hunt phase: 1 cells scanned

            +---+---+---+---+---+---+---+---+---+---+
            |           |                   |       |
            +   +---+   +---+---+---+   +   +   +   +
            |   |       |               |       |   |
            +---+   +---+   +---+---+---+---+---+---+
            |       |       |   |           |       |
            +   +---+   +   +   +   +---+   +   +   +
            |           |           |       |   |   |
            +---+---+---+---+---+---+   +   +---+   +
            |       |                   |       |   |
            +   +---+   +   +---+---+---+---+   +   +
            |           |                   |       |
            +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        EXAMPLE 3

                    hunt and kill
                   scan as ordered

            (log)
            kill phase: 133 candidate cells, 37 added to tree.
            hunt phase: 17 cells scanned
            kill phase: 53 candidate cells, 13 added to tree.
            hunt phase: 4 cells scanned
            kill phase: 19 candidate cells, 7 added to tree.
            hunt phase complete: 0 cells scanned

            +---+---+---+---+---+---+---+---+---+---+
            |               |                       |
            +   +   +---+---+   +---+---+---+---+   +
            |   |   |           |               |   |
            +   +   +   +---+   +   +---+---+   +   +
            |   |   |       |   |   |       |   |   |
            +   +   +---+   +   +---+   +   +   +   +
            |   |   |       |   |       |       |   |
            +   +   +   +---+   +   +---+---+---+   +
            |   |       |       |   |           |   |
            +   +---+---+   +---+   +   +---+---+   +
            |           |           |               |
            +---+---+---+---+---+---+---+---+---+---+
                    Maze characteristic:
                           number of nodes:         v = 60
                           number of edges:         e = 59
                      number of components:         k = 1
                      Euler characteristic: v - e - k = 0
                    A perfect maze!

        NOTES ON THE EXAMPLES

            The maze in example 3 shows a bias for straight passages.
            This is explained by the failure to randomize the scanning
            in the hunt phase.  The Python set implementation preserves
            the left-to-right, top-to-bottom ordering of the grid.

            The hunt phase in examples 1 and 2 both break the stability.
            In example 1, use of the first-in random-out queue serves
            to shuffle the hunt.  In example 2, the unvisited cells
            are themselves drawn in random order.
        """
        state = cls.State(maze, start=start, debug=debug)
        curr = state.curr
        if no_shuffle:
            while state.unvisited and curr:
                cls.kill_no_frontier(state)
                curr = cls.hunt_no_shuffle(state)
        elif use_frontier:
            while state.unvisited and curr:
                cls.kill_with_frontier(state)
                curr = cls.hunt_with_frontier(state)
        else:
            while state.unvisited and curr:
                cls.kill_no_frontier(state)
                curr = cls.hunt_no_frontier(state)

        if state.unvisited:
            print('WARNING: the grid is not connected!')
        return maze

    @staticmethod
    def kill_with_frontier(state):
        """kill phase of hunt and kill"""
        visited = 0
        fcount = 0
        nbrcount = 0

        while state.unvisited:
            neighbors = set(state.curr.neighbors)
            for nbr in list(neighbors):
                nbrcount += 1               # for log
                if not nbr in state.unvisited:
                    neighbors.discard(nbr)
            neighbors = list(neighbors)     # unvisited neighbors
            if not neighbors:
                break         # painted into corner

                # visit an unvisited neighbor
            index = randrange(len(neighbors))
            nbr = neighbors.pop(index)
            state.unvisited.discard(nbr)
            visited += 1                    # for log
            state.curr.link(nbr)
            state.curr, prev = nbr, state.curr

                # extend the frontier
            for nbr in neighbors:
                state.frontier.enter(prev, nbr)
                fcount += 1                 # for log

        if state.debug:
            print(f'kill phase: {nbrcount} candidate cells,' + \
                f' {visited} added to tree, {fcount} added to heap.')

    @staticmethod
    def hunt_with_frontier(state):
        """hunt phase of hunt and kill"""
        fcount = 0                      # for log
        
        while not state.frontier.isEmpty:
            prev, curr = state.frontier.serve()
            fcount += 1                 # for log
            if curr in state.unvisited:
                prev.link(curr)
                state.unvisited.discard(curr)
                state.curr = curr
                if state.debug:
                    print('hunt phase:' + \
                        f' {fcount} cells removed from heap')
                return curr

        if state.debug:
            print('hunt phase complete:' + \
                f'  {fcount} cells removed from heap')
        return None

    @staticmethod
    def kill_no_frontier(state):
        """kill phase of hunt and kill"""
        visited = 0
        nbrcount = 0

        while state.unvisited:
            neighbors = set(state.curr.neighbors)
            for nbr in list(neighbors):
                nbrcount += 1               # for log
                if not nbr in state.unvisited:
                    neighbors.discard(nbr)
            neighbors = list(neighbors)     # unvisited neighbors
            if not neighbors:
                break         # painted into corner

                # visit an unvisited neighbor
            index = randrange(len(neighbors))
            nbr = neighbors.pop(index)
            state.unvisited.discard(nbr)
            visited += 1                    # for log
            state.curr.link(nbr)
            state.curr, prev = nbr, state.curr

        if state.debug:
            print(f'kill phase: {nbrcount} candidate cells,' + \
                f' {visited} added to tree.')

    @staticmethod
    def hunt_no_frontier(state):
        """hunt phase of hunt and kill"""
        count = 0                       # for log

        candidates = list(state.unvisited)        # unshuffled!
        while candidates:
            index = randrange(len(candidates))    # random pick
            cell = candidates.pop(index)
            for nbr in cell.neighbors:
                count += 1
                if nbr not in state.unvisited:
                    if state.debug:
                        print(f'hunt phase: {count} cells scanned')
                    cell.link(nbr)
                    state.unvisited.discard(cell)
                    state.curr = cell
                    return cell
                    
        if state.debug:
            print(f'hunt phase complete: {count} cells scanned')
        return None

    @staticmethod
    def hunt_no_shuffle(state):
        """hunt phase of hunt and kill"""
        count = 0                       # for log

        candidates = list(state.unvisited)        # unshuffled!
        for cell in candidates:
            for nbr in cell.neighbors:
                count += 1
                if nbr not in state.unvisited:
                    if state.debug:
                        print(f'hunt phase: {count} cells scanned')
                    cell.link(nbr)
                    state.unvisited.discard(cell)
                    state.curr = cell
                    return cell
                    
        if state.debug:
            print(f'hunt phase complete: {count} cells scanned')
        return None

# end of hunt_kill.py
