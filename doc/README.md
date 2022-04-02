# mazes - a Python3 maze package

 1. Grids

    * rectangular grids
      + 4-connected
        The basic *rectangular grid* consists of a two-dimensional array of nominally square cells of identical size, arranged in a rectangle.  Cells may have neighbors to the north, south, east and west, using the customary map layout with north at top and east to the right.  The class is implemented as 'RectangularGrid' in module 'grid.py'. Because its cells are square, it is customarily called a *square grid*.

      + 8-connected
        The *8-connected rectangular grid* adds neighbors at the four corners of the square, to the northeast, northwest, southwest, and southeast.  Unlike its 4-connected counterpart, the 8-connected rectangular grid is generally not planar, and requires weaving to maintain its usual rectangular arrangement.  This class of grids is implemented as 'Rectangular8Grid', a subclass of 'RectangularGrid' in module 'grid8.py'.  Grids in this class are sometimes (unfortunately!) called *octagonal*.

      + 6-connected
        The *6-connected rectangular grid* adds just two opposite corners of the square, either southwest and northeast or southeast and northwest, to the four basic compass directions.  The grid is planar, requiring no weaving, and has some topological advantages over both the 4-connected and 8-connected grids.  This class of grids is implemented as 'Rectangular6Grid', a subclass of 'RectangularGrid' in module (*sic*!) 'grid8.py'.  Grids in this class are sometimes (justifiably!) called *hexagonal*.

    * glued rectangular grids
      + cylindrical
        Taking a rectangular sheet of paper, we can form a cylinder by gluing a pair of opposite edges.  Using virtual glue, this is exactly how we form a *cylindrical grid* from a 4-connected rectangular grid.  This class of grids is implemented as 'CylinderGrid', a subclass of 'RectangularGrid' in module 'cylinder_grid.py'.

      + toroidal
        Taking a rectangular sheet of flexible material, we can first form a cylinder by gluing one pair of opposite edges. Then we can stretch the free circular edges around to meet, and glue them to form a donut-like surface called a torus.  Again using virtual glue, this is precisely how we form a *toroidal grid* from a 4-connected rectangular grid.  This class of grids is implemented as 'TorusGrid', a subclass of 'RectangularGrid' in module 'torus_grid.py'.

      + Moebius strip
        Taking a long rectangular strip of paper, we can form a Moebius strip by giving it a half twist along its axis and then gluing the ends.  Using our virtual glue, we form a *Moebius strip grid* from a 4-connected rectangular grid in the same way.  This class of grids is implemented as 'MoebiusGrid', a subclass of 'RectangularGrid' in module 'Moebius_grid.py'.

    * Kuratowski grids
      The Kuratowski graphs include several families of highly-connected graphs.  The simplest family are the complete graphs K(n) in which each of the *n* vertices is incident to every other vertex.  A complete grid on n cells is one in which each cell has every other cell as a neighbor.  Also important are the complete bipartite graphs K(m,n) with m red vertices and n blue vertices, in which each red vertex has every blue vertex as a neighbor, but no vertex neighbors a vertex of the same color.  (The graphs K(5) and K(3,3) are especially important as they mark the boundary between planar graphs and non-planar graphs -- having one of these as a minor is both a necessary and sufficient condition for a graph to have no planar embedding.) Grids based on Kuratowski graphs are implemented as classes 'CompleteGrid' and 'PartiteGrid' in module 'kuratowski.py' -- subclass 'BipartiteGrid' of 'PartiteGrid' covers the bibipartite cases.

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
 
 
