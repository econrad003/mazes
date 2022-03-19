"""Moebius_grid.py - implementation of the MoebiusGrid class
Copyright 2022 by Eric Conrad

IMPLEMENTS

    class MoebiusGrid

REMARK

    Since a Moebius strip surface is not orientable, it is not clear
    how the lazy binary tree algorithm, the cocktail shaker algorithm
    or the sidewinder algorithm might be adapted.  (There is a trivial
    adaptation which is equivalent to cutting the strip along the
    column where it was taped.)

DESCRIPTION

    The Moebius strip grid can be viewed as a rectangular strip of
    quadrille paper with a pair of opposite ends taped (after twisting
    the strip one half revolutation) as in Figure 1.

              +---+---+---+---+---+
           A  | 1 |   |   |   | 6 | C'    Figure 1:
              +---+---+---+---+---+         a 3x5 cylindrical grid
           B  | 2 |   |   |   | 5 | B'
              +---+---+---+---+---+
           C  | 3 |   |   |   | 4 | A'
              +---+---+---+---+---+

    As a result of the taping of the two ends ABC and A'B'C', the
    nodes and edges along boundary ABC and those along boundary
    A'B'C' are identified and faces 1, 2 and 3 are respectively
    east of faces 4, 5 and 6.

    When crossing from 1, 2 or 3 respectively into 4, 5 or 6 (or
    vice versa,) the compass suddenly changes with NESW becoming
    SWNE.

EXAMPLE

    Here is an example of a binary spanning tree maze on a Moebius
    strip grid that was produced using depth-first search.  The
    root cell of the rooted tree found by DFS is the cell marked
    'r' for 'root'.  Note that cell (3,9) on the right exits east
    to cell (2,0) on the left.  The exit is through nodes C and D.
    Note also that nodes C and D are oriented NS at exit right and
    SN at entrance left. (Cell (0,0) is marked with a capital 'O'.)

    

            a binary spanning maze on a Moebius strip grid
        G +---+---+---+---+---+---+---+---+---+---+ A
                              |                   |
        F +---+---+---+---+   +   +---+---+---+   + B
                          |   |       |       |   |
        E +   +---+---+---+   +   +   +   +   +   + C
              |               |   |       |   |   ------>
        D +---+   +---+---+---+   +---+---+   +---+ D
      ----->  |       |           |       |
        C +   +---+   +---+---+---+   +   +---+---+ E
          |   |   |   |               |       |
        B +   +   +   +   +---+---+---+---+   +   + F
          | O     |                   | r     |
        A +---+---+---+---+---+---+---+---+---+---+ G
                Maze characteristic:
                       number of nodes:         v = 60
                       number of edges:         e = 59
                  number of components:         k = 1
                  Euler characteristic: v - e - k = 0
                A perfect maze!

    The identification of the left and right edges of the fundamental
    rectangle shows up in the Euler characteristic:

                Grid characteristic:
                       number of nodes:             v = 71
                       number of edges:             e = 131
                       number of faces:             f = 60
                  number of components:             k = 1
                  Euler characteristic: v - e + f - k = -1

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
from grid import RectangularGrid

class MoebiusGrid(RectangularGrid):
    """MoebiusGrid - a Moebius strip grid class"""

    def transform(self, x, y):
        """coordinate transformation

        For a rectangular grid, coordinates are not transformed.  This
        is a stub for derived classes (for example ToroidalGrid).

        If integers are input, integers should be output.  The modulus
        operation (%) preserves integer input, but the divide opration
        (/) does not.
        """
        q = x // self.cols      # Python 3: q=floor(x/c), r=c - qx
        xprime = x % self.cols

        yprime = y if q % 2 == 0 else \
            self.rows - y - 1
        return (xprime, yprime)

    def __str__(self):
        """string representation of the maze"""
            # assemble the string image, row by row
        s = ''
        markers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if len(markers) < self.rows + 1:
            markers *= (self.rows + 1) // len(markers) + 1
        markers = markers[:self.rows + 1]
        reverse_markers = markers[::-1]
        
        for i in range(self.rows-1, -1, -1):
            row = self.row(i)
            marker1 = markers[i+1] + ' '
            marker2 = ' ' + reverse_markers[i+1] + '\n'
            s += marker1 + self._make_wall(i, row) + marker2 
            marker1 = '  '
            marker2 = '\n'
            s += marker1 + self._make_faces(i, row) + marker2

        row = self.row(0)
        s += markers[0] + ' '
        s += self._make_wall(0, row, direction=self.SOUTH,
                             walls=['   ', ' ^ ', ' v ', '---'])
        s += ' ' + reverse_markers[0]

        return s

        # sketching is almost the same as cylindrical grid
        # We just swap the A/B indicators on one end.

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
        sketcher.draw_text((x, y), 'B', fontsize=14)

        x, y = hmargin // 2, cheight * self.rows + vmargin // 2
        sketcher.draw_text((x, y), 'B', fontsize=14)
        x += cwidth * (self.cols + 1) + hmargin // 5
        sketcher.draw_text((x, y), 'A', fontsize=14)

# end of Moebius_grid.py
