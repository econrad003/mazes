"""cylinder_grid.py - implementation of the CylinderGrid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class CylinderGrid

    algorithm BinaryTree
    algorithm CocktailShaker
    algorithm Sidewinder

DESCRIPTION

    The cylindrical grid can be viewed as a rectangular strip of
    quadrille paper with a pair of opposite sides taped as in
    Figure 1.

              +---+---+---+---+---+
           A  | 1 |   |   |   | 4 | A'    Figure 1:
              +---+---+---+---+---+         a 3x5 cylindrical grid
           B  | 2 |   |   |   | 5 | B'
              +---+---+---+---+---+
           C  | 3 |   |   |   | 6 | C'
              +---+---+---+---+---+

    As a result of the taping of the two sides ABC and A'B'C', the
    nodes and edges along boundary ABC and those along boundary
    A'B'C' are identified and faces 1, 2 and 3 are respectively
    east of faces 4, 5 and 6.

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
from grid import RectangularGrid

class CylinderGrid(RectangularGrid):
    """CylinderGrid - a cylindrical grid class

    The identification of the left and right sides of the fundamental
    rectangle shows up in the Euler characteristic.  Starting with a
    6x10 rectangular grid with 60 cells or faces, there are:

        (6+1)x(10+1) = 77 nodes,

    of which the 7 in the last column are identified with the 7 in the
    first column, leaving v = 70 nodes.  The 6x10 rectangular grid has

        6(10+1) = 66 vertical edges, and
        (6+1)10 = 70 horizontal edges, of which
        6 vertical edges are paired with their mates at row's end,

    leaving e = 130 edges.

    The cylindrical grid is connected (k=1) and has the same f=60 faces
    as its rectangular counterpart.

                Grid characteristic for the 6x10 cylindrical grid:
                       number of nodes:             v = 70
                       number of edges:             e = 130
                       number of faces:             f = 60
                  number of components:             k = 1
                  Euler characteristic: v - e + f - k = -1

    More generally:
                Rectangular         Cylindrical       Toroidal
      v         (m+1)(n+1)          (m+1)n            mn
      e         m(n+1) + (m+1)n     mn + (m+1)n       2mn
      f         mn                  mn                mn
      k         1                   1                 1
      v-e+f-k   0                   -1                -1

    EXAMPLE

                recursive backtracker on a cylindrical grid
        A +---+---+---+---+---+---+---+---+---+---+ A
              |                   |       |        
          +   +---+---+---+   +   +---+   +   +---+
              |               |           |   | r  
          +---+   +---+---+---+---+   +---+   +---+
                  |               |   |       |    
          +---+   +---+---+   +   +   +   +---+   +
              |   |       |   |       |       |    
          +   +   +   +   +---+---+---+---+   +---+
          |   |       |                   |       |
          +   +---+---+---+---+---+---+   +---+   +
          |                           |           |
        B +---+---+---+---+---+---+---+---+---+---+ B
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    """

    def transform(self, x, y):
        """coordinate transformation

        For a rectangular grid, coordinates are not transformed.  This
        is a stub for derived classes (for example ToroidalGrid).

        If integers are input, integers should be output.  The modulus
        operation (%) preserves integer input, but the divide opration
        (/) does not.
        """
        return (x % self.cols, y)

    def __str__(self):
        """string representation of the maze"""
            # assemble the string image, row by row
        s = ''
        marker1 = 'A '
        marker2 = ' A\n'
        for i in range(self.rows-1, -1, -1):
            row = self.row(i)
            s += marker1 + self._make_wall(i, row) + marker2 
            marker1 = '  '
            marker2 = '\n'
            s += marker1 + self._make_faces(i, row) + marker2
        row = self.row(0)
        s += 'B '
        s += self._make_wall(0, row, direction=self.SOUTH,
                             walls=['   ', ' ^ ', ' v ', '---'])
        s += ' B'

        return s

    def sketch_setup(self):
        """sketch parameter setup"""
        MARGIN = 40          # reserved part of window
        assert MARGIN > 1
        if not self._kwargs.get('hmargin'):
            self._kwargs['hmargin'] = MARGIN
        super().sketch_setup()

    def sketch_epilogue(self, sketcher):
        """sketching epilogue"""
        super().sketch_epilogue(sketcher)
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

        x, y = hmargin // 2, cheight + vmargin // 2
        sketcher.draw_text((x, y), 'A', fontsize=14)
        x += cwidth * (self.cols + 1) + hmargin // 5
        sketcher.draw_text((x, y), 'A', fontsize=14)

        x, y = hmargin // 2, cheight * self.rows + vmargin // 2
        sketcher.draw_text((x, y), 'B', fontsize=14)
        x += cwidth * (self.cols + 1) + hmargin // 5
        sketcher.draw_text((x, y), 'B', fontsize=14)

class BinaryTree(object):
    """a version of the lazy binary tree algorithm for cylindrical grids

    EXAMPLE

        lazy binary tree on a cylindrical grid
            A +---+---+---+---+---+---+---+---+---+---+ A
                            X |                        
              +   +---+---+   +   +---+---+---+   +   +
              |   |           | X |               |   |
              +   +   +   +   +   +   +---+   +   +---+
                  |   |   |   |   |   |       | X |    
              +---+   +---+   +   +---+   +---+---+---+
                      |       |   |     X |            
              +   +---+   +   +   +   +---+   +   +---+
                  |       |   |   |   |       | X |    
              +---+---+   +---+   +   +   +   +   +---+
                          |       |   |   | X |   |    
            B +---+---+---+---+---+---+---+---+---+---+ B
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    PROOF OF CORRECTNESS

        To adapt the lazy binary tree algorithm to a cylinder, it is
        necessary to put 'splitters' in each row.  The worker in the
        splitter cell simply carves nothward if he can.  (The top row
        splitter is lazy and takes a smoking break.) This condition
        guarantees that each worker (one per cell) carves exactly one
        passage, so we have v cells and (v-1) passages.  Except for
        the top row, each run ends in a rise.  The top row is a run
        starting with the cell east of the top row splitter.

        We can accordingly always reach the top row from any cell,
        and we can reach any cell in the top row.  Thus the maze is
        connected.

        A connected maze with v cells and (v-1) passages is a spanning
        tree and (equivalently, by definition) a perfect maze.

        To show that this tree is binary, take the splitter cell in
        the top row as the root of the tree.  It has at most two
        children, one to the west and possibly a second to the south.
        These two or three cells form a rooted binary tree.  Now
        suppose we have amassed a subset of the cells into a rooted
        binary tree with the top splitter as root.  Consider a cell on
        the frontier.  By construction, it must have either a passage
        north or a passage east, but not both.  If it has a passage west
        or south, neither can be part of the emerging tree as there
        would be a cycle in the maze.  (The path from the neighbor up
        the tree to root and back down through the frontier cell to the
        neighbor must contain a nontrivial circuit.)  So add the
        frontier cell to the emerging rooted binary tree -- the passage
        north or east takes this cell to its parent -- and repeat the
        the process with the larger tree. (Moving north or east takes us
        from child to parent, so each cell has one parent.  Moving south
        or west takes us from parent to child, so each cell has at most
        two children.)  As the maze is connected and has a finite number
        of cells, there must be a point in time when the emerging rooted
        binary tree contains every cell in the maze. 

    REMARK

        As a corollary, every cylinder grid has a binary spanning tree.
        

    MAZE BIASES

        1) Each run in every row except the top row has a rise from the
           eastmost cell.

        2) The top row is a complete run.
    """

    @classmethod
    def on(cls, maze, p=0.5, mark_split=False):
        """carve a binary tree on a cylindrical grid"""
        grid = maze.grid
        east, north = grid.EAST, grid.NORTH
        for i in range(grid.rows):
            splitter = randrange(grid.cols)
            row = grid.row(i, split=splitter)
            last = row.pop()      # the last cell in the row
            for cell in row:
                nbr_east = cell[east]
                nbr_north = cell[north]

                if nbr_east and nbr_north:
                        # flip a coin and carve accordingly
                    rand = random()     # heads with probability p
                    nbr = nbr_east if rand < p else nbr_north
                    cell.link(nbr)
                    continue

                if nbr_north:
                        # carve northward
                    cell.link(nbr_north)
                    continue

                if nbr_east:
                        # carve eastward
                    cell.link(nbr_east)

                # last in row
            if mark_split:
                last.text = 'X'
            nbr_north = last[north]
            if nbr_north:
                    # carve northward
                last.link(nbr_north)

        return maze

class CocktailShaker(object):
    """CocktailShaker - another of binary spanning tree algorithm

    Just a few lines need to be changed to turn the lazy binary tree
    into a cocktail shaker tree.  (These lines are commented '####'
    in the source code.  Those labelled '#### 1' are consequential
    changes, while those labelled '#### 2' just mark the change of
    one variable name from 'nbr_east' to 'nbr_side'.)

    EXAMPLE

              cocktail shaker binary tree on a cylindrical grid
        A +---+---+---+---+---+---+---+---+---+---+ A
                      | X                          
          +---+   +   +   +---+---+---+   +   +---+
                  | X |   |               |   |    
          +   +   +   +   +   +---+   +   +---+   +
          |   | X |   |   |       |   |       |   |
          +   +   +   +   +---+---+   +---+   +   +
          |   | X |   |   |           |       |   |
          +   +   +   +---+---+---+---+   +   +   +
          |   |   |                   |   | X |   |
          +---+---+---+   +---+   +   +   +---+---+
                          |     X |   |   |        
        B +---+---+---+---+---+---+---+---+---+---+ B
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    PROOF OF CORRECTNESS

        The proof of correctness carries over from the lazy binary tree
        algorithm, with a small cosmetic change in the first paragraph,
        to wit:

        To adapt the cocktail shaker tree algorithm to a cylinder, it
        is necessary to put 'splitters' in each row.  The worker in the
        splitter cell simply carves nothward if he can.  (The top row
        splitter is lazy and takes a smoking break.) This condition
        guarantees that each worker (one per cell) carves exactly one
        passage, so we have v cells and (v-1) passages.  Except for
        the top row, each run ends in a rise.  The top row is a run
        starting with the cell east of the top row splitter.

        We can accordingly always reach the top row from any cell,
        and we can reach any cell in the top row.  Thus the maze is
        connected.

        A connected maze with v cells and (v-1) passages is a spanning
        tree and (equivalently, by definition) a perfect maze.

        Proof that the tree is binary is similar to that for the lazy
        binary tree algorithm.  The only difference is that the
        east/west roles depend on whether the row is even or odd.

    MAZE BIASES

        1) Each run in every row except the top row has a rise from
           either the eastmost cell, for odd rows, or westmost cell,
           for even rows.

        2) The top row is a complete run.
    """

    @classmethod
    def on(cls, maze, p=0.5, mark_split=False):
        """carve a binary tree on a rectangular grid"""
        grid = maze.grid
        east, west, north = grid.EAST, grid.WEST, grid.NORTH  #### 1
        for i in range(grid.rows):
            rev = i%2==1                                      #### 1
            splitter = randrange(grid.cols)
            row = grid.row(i, split=splitter, reverse=rev)    #### 1
            last = row.pop()      # the last cell in the row
            for cell in row:
                nbr_side = cell[west] if rev else cell[east]  #### 1
                nbr_north = cell[north]

                if nbr_side and nbr_north:                    #### 2
                        # flip a coin and carve accordingly
                    rand = random()     # heads with probability p
                    nbr = nbr_side if rand < p else nbr_north #### 2
                    cell.link(nbr)
                    continue

                if nbr_north:
                        # carve northward
                    cell.link(nbr_north)
                    continue

                if nbr_side:                                  #### 2
                        # carve eastward
                    cell.link(nbr_side)                       #### 2

                # last in row
            if mark_split:
                last.text = 'X'
            nbr_north = last[north]
            if nbr_north:
                    # carve northward
                last.link(nbr_north)

        return maze

class Sidewinder(object):
    """SidewinderTree - the sidewinder maze passage carver

    EXAMPLE

            sidewinder tree on a cylindrical grid
        A +---+---+---+---+---+---+---+---+---+---+ A
                                X |                
          +   +   +   +   +---+---+---+---+---+   +
          |   |   |   |                     X |   |
          +---+---+---+   +---+---+   +---+   +---+
                          |               | X |    
          +   +   +---+---+   +   +   +---+   +   +
          |   |           |   |   | X |       |   |
          +   +---+   +---+---+   +---+   +   +   +
          | X |           |       |       |   |   |
          +---+   +---+   +   +   +---+   +   +   +
          |     X |       |   |   |       |   |   |
        B +---+---+---+---+---+---+---+---+---+---+ B
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    PROOF OF CORRECTNESS

        The proof of correctness for the lazy binary tree can be adapted
        to show that the algorithm always produces a spanning tree, but
        not necessarily a binary tree.
        
        (The sidewinder algorithm is more general than the lazy binary
        tree algorithm and the cocktail shaker algorithm. The former is
        the special case in which the 'random' run element is always the
        last.  The latter is the case where the 'random' run element is
        repectively first or last as the row number is even or odd.)
"""

    @classmethod
    def on(cls, maze, mark_split=False, p=0.5):
        """carve a sidewinder tree on a cylindrical grid"""
        east, north = 'east', 'north'
        grid = maze.grid
        for i in range(grid.rows-1):
            run = []
            splitter = randrange(grid.cols)       #### split the row
            row = grid.row(i, split=splitter)     ####
            for j in range(grid.cols-1):
                run.append(j)
                rand = random()       # the digger flips a coin
                if rand < p:              # heads it is!
                    cell = row[j]                 ####
                    cell.link(cell[east])
                    continue
                k = choice(run)       # carve north somewhere
                cell = row[k]                     ####
                cell.link(cell[north])
                run = []              # close the run

                # end of row
            if mark_split:                        ####
                row[-1].text = 'X'                ####
            j = grid.cols-1           # last cell in row
            run.append(j)
            k = choice(run)
            cell = row[k]                         ####
            cell.link(cell[north])

        i = grid.rows - 1
        splitter = randrange(grid.cols)           #### split the row
        row = grid.row(i, split=splitter)         ####
        if mark_split:                            ####
            row[-1].text = 'X'                    ####
        for j in range(grid.cols-1):
            cell = row[j]                         ####
            cell.link(cell[east])

        return maze

# end of cylinder_grid.py
