"""torus_grid.py - implementation of the TorusGrid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class TorusGrid

DESCRIPTION

    The toroidal grid can be viewed as a rectangular strip of
    flexible quadrille paper with pairs of opposite sides taped as
    in Figure 1.

                D   E   F   G   H
              +---+---+---+---+---+
           A  | 1 |   |   |   | 4 | A'    Figure 1:
              +---+---+---+---+---+         a 3x5 cylindrical grid
           B  | 2 |   |   |   | 5 | B'
              +---+---+---+---+---+
           C  | 3 |   |   |   | 6 | C'
              +---+---+---+---+---+
                D'  E'  F'  G'  H'

    First, one pair of sides is taped to form a cylinder.  Then, One
    of the remaining sides is rolled inside the cylinder to meet its
    opposite, forming a donut or bagel shaped figure called a torus.

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

class TorusGrid(RectangularGrid):
    """TorusGrid - a toroidal grid class

    The identification of the left and right boundaries, and of the top
    and bottom boundaries of the fundamental rectangle shows up in the
    Euler characteristic.  Starting with a 6x10 rectangular grid with
    60 cells or faces, there are:

        (6+1)x(10+1) = 77 nodes,

    of which the 7 in the last column are identified with the 7 in the
    first column, and the remaining 10 nodes at top row are identified
    with their counterparts at bottom leaving v = 60 nodes.

    The 6x10 rectangular grid has

        6(10+1) = 66 vertical edges, and
        (6+1)10 = 70 horizontal edges, of which
        6 vertical edges are paired with their mates at row's end, and
        10 horizontal edges at top are identified with mates at bottom,

    leaving e = 120 edges.

    The toroidal grid is connected (k=1) and has the same f=60 faces
    as its rectangular counterpart.

                Grid characteristic for the 6x10 toroidal grid:
                       number of nodes:             v = 60
                       number of edges:             e = 120
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

                recursive backtracker on a toroidal grid
            C                                   D
        A +---+   +   +---+---+---+   +---+   +---+ A
              |                       |       |    
          +   +---+---+---+---+---+---+   +---+   +
          |                   |       |           |
          +---+---+---+---+   +   +   +---+---+---+
          |       |           |   |               |
          +   +   +   +---+---+   +   +---+---+---+
              |   |     r |       |                
          +---+   +---+---+   +---+---+---+---+---+
          |       |       |       |               |
          +   +---+   +---+---+   +---+   +---+---+
              |   |               |       |        
        B +---+   +   +---+---+---+   +---+   +---+ B
            C                                   D

                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    AN APPLICATION

          Here is the path the Red Cap took from her home (r) through
          the dark woods to her grandmother's house (*):

                    v               ^       ^
          +---+   + v +---+---+---+ ^ +---+ ^ +---+
        <-- A |     g   h   i   j   k | F   G | B <--
          +   +---+---+---+---+---+---+   +---+   +
          | 9   8   7   6   5 | W   V | E   D   C |
          +---+---+---+---+   +   +   +---+---+---+
          | O   N | 2   3   4 | X | U             |
          +   +   +   +---+---+   +   +---+---+---+
        <-- P | M | 1   r | Z   Y | T   S   R   Q <--
          +---+   +---+---+   +---+---+---+---+---+
          | K   L |       | a   b |     n   o   * |
          +   +---+   +---+---+   +---+   +---+---+
        --> J |   | f   e   d   c | l   m | H   I -->
          +---+   + v +---+---+---+ ^ +---+ ^ +---+ B
                    v               ^       ^
    """

    def transform(self, x, y):
        """coordinate transformation

        For a rectangular grid, coordinates are not transformed.  This
        is a stub for derived classes (for example ToroidalGrid).

        If integers are input, integers should be output.  The modulus
        operation (%) preserves integer input, but the divide opration
        (/) does not.
        """
        return (x % self.cols, y % self.rows)

    def __str__(self):
        """string representation of the maze"""
            # assemble the string image, row by row
        s = ''
        s += '    C  ' + '    ' * (self.cols - 2) + ' D\n'
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
        s += ' B\n'
        s += '    C  ' + '    ' * (self.cols - 2) + ' D'

        return s

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
        if not self._kwargs.get('vmargin'):
            self._kwargs['vmargin'] = MARGIN
        super().sketch_setup()

    def sketch_epilogue(self, sketcher):
        """sketching epilogue"""
        super().sketch_epilogue(sketcher)
        cwidth = self._kwargs['cell_width']
        cheight = self._kwargs['cell_height']
        hmargin = self._kwargs['hmargin']
        vmargin = self._kwargs['vmargin']

            # row markers

        x, y = hmargin // 2, cheight + vmargin
        sketcher.draw_text((x, y), 'A', fontsize=14)
        x += cwidth * (self.cols + 1) + hmargin // 5
        sketcher.draw_text((x, y), 'A', fontsize=14)

        x = hmargin // 2
        y += cheight * (self.rows - 1)
        sketcher.draw_text((x, y), 'B', fontsize=14)
        x += cwidth * (self.cols + 1) + hmargin // 5
        sketcher.draw_text((x, y), 'B', fontsize=14)

            # column markers

        x, y = (5 * hmargin) // 4, int(0.9 * vmargin)
        sketcher.draw_text((x, y), 'C', fontsize=14)
        y += cheight * (self.rows + 1)
        sketcher.draw_text((x, y), 'C', fontsize=14)

        x += cwidth * (self.cols - 1)
        y = int(0.9 * vmargin)
        sketcher.draw_text((x, y), 'D', fontsize=14)
        y += cheight * (self.rows + 1)
        sketcher.draw_text((x, y), 'D', fontsize=14)

# end of torus_grid.py
