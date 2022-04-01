"""test_annular_segment.py - test a drawing primitive
Copyright 2022 by Eric Conrad

USAGE

    usage: test_annular_segment.py [-h]

    Test the maze_pillow implementation of draw_segment.

    optional arguments:
        -h, --help
                          show this help message and exit
        -c H1 H2, -clock H1 H2
                          timespan on a 12-hour clock

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
from math import pi
import mazelib
from grid import Grid
from maze import Maze
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'test_annular_segment.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--clock', type=int, nargs=2,
        default=(5, 10),      # 5 o'clock to 10 o'clock
        help='timespan on a 12-hour clock')
    args = parser.parse_args()

    h1, h2 = args.clock

        # The grid will have m+n cells and mn grid edges.

        # --------- TESTING STARTS HERE ----------
    print('Test',
          f'Draw an annular segment')
    grid = Grid()         # stub
    maze = Maze(grid)     # stub
    sketcher = MazeSketcher(maze, title='Yet another annular segment')
    sketcher.open(width=300, height=300)

    xy =((30,30), (60,60))
    sketcher.canvas.ellipse(xy, fill='yellow', width=3)
        # NB: angles in degrees (bleccch!) clockwise!
        # clockwise make sense since the coordinate system follows
        # the left-hand rule.
    sketcher.canvas.arc(xy, 0, 90, fill='green', width=5)
    sketcher.canvas.arc(xy, -180, -90, fill='black', width=5)
    
    center = (150,150)
    sketcher.draw_circle(center, 100, fill="white", outline="black")

    theta1 = (h1-3)/12
    theta2 = (h2-3)/12
    sketcher.draw_segment(center, 90, 70, theta1, theta2,
                          fill="red", outline='blue')

    sketcher.close(show=True)

    print('Success!')

# end of test_annular_segment.py
