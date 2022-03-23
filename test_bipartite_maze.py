"""test_bipartite_maze.py - test the Kuratowski complete grid
Copyright 2022 by Eric Conrad

USAGE

    usage: test_bipartite_maze.py [-h] [-r ROW ROW]

    Test the Kuratowski complete bipartite grid K(m,n).

    optional arguments:
        -h, --help
                          show this help message and exit
        -r ROW ROW, --row ROW ROW
                          the row lengths (m and n)

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

import mazelib
from kuratowski_grid import BipartiteGrid
from maze import Maze
from wilson import Wilson
from maze_pillow import MazeSketcher

if __name__ == '__main__':
    import argparse

    desc = 'Test the Kuratowski complete bipartite grid K(m,n).'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-r', '--row', type=int, nargs=2,
        default=[5,4],
        help='the lengths of the rows (m and n)')
    args = parser.parse_args()

    m, n = args.row

        # The grid will have m+n cells and mn grid edges.

        # --------- TESTING STARTS HERE ----------
    print('Test 1)',
          f'The complete grid K({n})')
    grid = BipartiteGrid(m, n, wall_builder=True, cell_radius=10)
    print(len(grid.cells))
    assert len(grid.cells) == m+n
    assert len(grid[(0,0)].neighbors) == n, \
        f'Cell 0 has {len(grid[(0,0)].neighbors)} neighbors'
    maze = Maze(grid)
    sketcher = MazeSketcher(maze, \
        title=f'The complete bipartite grid K({m},{n})')
    maze.sketch()

    print('Test 2) Wilson\'s algorithm',
          f'on the complete bipartite grid K({m},{n})')
    grid = BipartiteGrid(m, n)
    maze = Maze(grid)
    Wilson.on(maze)
    sketcher = MazeSketcher(maze, \
        title='Wilson\'s algorithm ' + \
        f'on the complete bipartite grid K({m},{n})')
    maze.sketch()

    print('Success!')

# end of test_complete_maze.py
