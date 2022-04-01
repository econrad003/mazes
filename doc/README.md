# mazes - a Python3 maze package

 1. Grids

    * rectangular grids
      + 4-connected
        The basic *rectangular grid* consists of a two-dimensional array of nominally square cells of identical size, arranged in a rectangle.  Cells may have neighbors to the north, south, east and west, using the customary map layout with north at top and east to the right.  The class is implemented as 'RectangularGrid' in module 'grid.py'. Because its cella are square, it is customarily called a *square grid*.

      + 8-connected
        The *8-connected rectangular grid* adds neighbors at the four corners of the square, to the northeast, northwest, southwest, and southeast.  Unlike its 4-connected counterpart, the 8-connected rectangular grid is generally not planar, and requires weaving to maintain its usual rectangular arrangement.  This class of grids is implemented as a subclass of 'RectangularGrid' in module 'grid8.py'.  Grids in this class are sometimes called *octagonal*.

      + 6-connected

    * glued rectangular grids
      + cylindrical
      + toroidal
      + Moebius strip

    * Kuratowski grids

    * Petersen grids

    * polar grids
 
 2. Maze generation algorithms

    * grid-specific
      + lazy binary trees
      + sidewinder trees

    * grid-independent
      + Wilson's algorithm
      + Aldous/Broder
      + growing tree algorithms (DFS, BFS, RFS, Prim)
      + binary tree via search

    * tweaking
      + dead-end removal

 3. Support algorithms

    * Bellman-Ford distance and shortest path
 
 
