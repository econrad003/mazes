# mazes - a Python3 maze package

COPYRIGHT 2022 by Eric Conrad.
LICENSE: GPLv3

 1. Grids

    * rectangular grids
      + 4-connected
        The basic *rectangular grid* consists of a two-dimensional array of nominally square cells of identical size, arranged in a rectangle.  Cells may have neighbors to the north, south, east and west, using the customary map layout with north at top and east to the right.  The class is implemented as `RectangularGrid` in module `grid.py`. Because its cells are square, it is customarily called a *square grid*.

      + 8-connected
        The *8-connected rectangular grid* adds neighbors at the four corners of the square, to the northeast, northwest, southwest, and southeast.  Unlike its 4-connected counterpart, the 8-connected rectangular grid is generally not planar, and requires weaving to maintain its usual rectangular arrangement.  This class of grids is implemented as `Rectangular8Grid`, a subclass of `RectangularGrid` in module `grid8.py`.  Grids in this class are sometimes (unfortunately!) called *octagonal*.

      + 6-connected
        The *6-connected rectangular grid* adds just two opposite corners of the square, either southwest and northeast or southeast and northwest, to the four basic compass directions.  The grid is planar, requiring no weaving, and has some topological advantages over both the 4-connected and 8-connected grids.  This class of grids is implemented as `Rectangular6Grid`, a subclass of `RectangularGrid` in module (*sic*!) `grid8.py`.  Grids in this class are sometimes (justifiably!) called *hexagonal*.

    * glued rectangular grids
      + cylindrical
        Taking a rectangular sheet of paper, we can form a cylinder by gluing a pair of opposite edges.  Using virtual glue, this is exactly how we form a *cylindrical grid* from a 4-connected rectangular grid.  This class of grids is implemented as `CylinderGrid`, a subclass of `RectangularGrid` in module `cylinder_grid.py`.

      + toroidal
        Taking a rectangular sheet of flexible material, we can first form a cylinder by gluing one pair of opposite edges. Then we can stretch the free circular edges around to meet, and glue them to form a donut-like surface called a torus.  Again using virtual glue, this is precisely how we form a *toroidal grid* from a 4-connected rectangular grid.  This class of grids is implemented as `TorusGrid`, a subclass of `RectangularGrid` in module `torus_grid.py`.

      + Moebius strip
        Taking a long rectangular strip of paper, we can form a Moebius strip by giving it a half twist along its axis and then gluing the ends.  Using our virtual glue, we form a *Moebius strip grid* from a 4-connected rectangular grid in the same way.  This class of grids is implemented as `MoebiusGrid`, a subclass of `RectangularGrid` in module `Moebius_grid.py`.

    * Kuratowski grids
      The *Kuratowski graphs* include several families of highly-connected graphs.  The simplest family are the complete graphs K(n) in which each of the *n* vertices is incident to every other vertex.  A complete grid on n cells is one in which each cell has every other cell as a neighbor.  Also important are the complete bipartite graphs K(m,n) with m red vertices and n blue vertices, in which each red vertex has every blue vertex as a neighbor, but no vertex neighbors a vertex of the same color.  (The graphs K(5) and K(3,3) are especially important as they mark the boundary between planar graphs and non-planar graphs -- having one of these as a minor is both a necessary and sufficient condition for a graph to have no planar embedding.) Grids based on Kuratowski graphs are implemented as classes `CompleteGrid` and `PartiteGrid` in module `kuratowski.py` -- subclass `BipartiteGrid` of `PartiteGrid` in the same module covers the bipartite cases.

    * Petersen grids
      The *Petersen graph* is a graph consisting of 10 vertices, with five vertices linked outside to form a pentagon, the other five linked inside to form a pentagram, and with each of the vertices of the pentagon linked to the nearest vertex of the pentagram. (The Petersen graph is closely linked to the complete graph K(5) and and the complete bipartite graph K(3,3).)  This graph generalizes to form a family of graphs. By replacing vertices with cells or faces, we obtain grids.  Grids based on the generalized Petersen graphs are implemented in class `PetersenGrid` in module `petersen.py`.

    * polar grids
      Circular mazes -- mazes embedded on circular disks -- consist of corridors running along circles of latitude connected perpendicular passages along lines of longitude.  (These mazes, also known as theta mazes, might also be thought of as hemispherical mazes, mazes on the surface of a hemisphere.)  The underlying grids are called *polar grids* or *theta grids*, and are implemented as class `PolarGrid` in module `polar_grid.py`.
 
 2. Maze generation algorithms

    A *perfect maze* is a _connected_ maze for which there is a unique simple path joining each pair of cells.  In graph-theoretic terms, a perfect maze is a spanning tree on its cells.  A perfect maze with *n* cells must have exactly *n-1* passages (or edges) joining each pair of cells.  This condition is not sufficient -- the maze must in addition be connected. A connected maze with *n* cells and *n-1* passages is a perfect maze.  Yet another way of stating this is that a perfect maze (or a spanning tree) is connected and circuit-free.

    Not all mazes are 'perfect', and use of the term 'perfect' does not accord with common notions of 'perfection'.  Instead, 'perfect' is used in a precise mathematical sense.  A maze which is perfect is minimal -- it has just enough passages to connect the maze -- no more and no less.

    The term 'spanning' implies that all cells (or vertices) are incorporated in the graph, and that the spanning graph is restricted to edges of its parent graph.  We can speak of spanning graphs of various types.  A 'tree' is a type of graph obtained recursively from a single cell: (1) a single cell is a tree; (2) given two trees and one cell in each tree, we can produce a third tree by connecting the two given cells with a passage (or edge); and (3) every tree can be produced by applying rules (1) and (2) a finite number of times.  Using the recursive definition, it is easy to show that every tree is connected, and the difference in the number of vertices and the number of edges in every tree is always exactly one.

    * grid-specific spanning tree algorithms
      + lazy binary trees
        In its implementation on a 4-connected rectangular grid, we start with two perpendicular directions, for example, south and east.  A worker is sent to each cell in the grid armed with a coin and a pickaxe.  A bell sounds and each worker flips his coin.  If the coin lands head face up, the worker is to carve a passage south if he can, or eastward, if south is not an option.  Conversely, if the coin lands tail face up, the worker is to carve eastward if he can, or southward if he cannot. One lucky worker, the worker in the southeast corner cannot go either way, so he simply eats his lunch.  A version of this algorithm, using east and north respectively instead of south and east is implemented as method `BinaryTree.on` in module `binary_tree.py`.  A variant which produces slightly different binary spanning trees by alternating lateral direction according to whether the row is even or odd is implemented as method `CocktailShakerTree.on` in module `cocktail_shaker_tree.py`. With some care, the algorithm can be adapted to cylindrical grids and to polar grids.
        Implementations for cylindrical grids are methods `BinaryTree.on` and `CocktailShaker.on` in module `cylinder_grid.py`.  Polar grid implementations are available as special cases of the inward and outward winder methods.
        Note that lazy binary trees are only some of the binary spanning trees that can be produced on rectangular grids.  For more general binary trees, see _binary trees via search_ below under _grid-independent spanning tree algorithms_.

      + sidewinder trees
        This algorithm is a generalization of the lazy binary tree algorithm.  Here we again use directions south and east for our informal description.  Each worker is assigned a north/south column and positions himself in the northmost cell of the column.  This time he flips his coin once for all but the southmost cell.  On heads, he carves a passage south and moves to the next cell.  On tails, he randomly picks one of the cells in his current southward run and carves a passage eastward. He is then transported to the next cell in his column where he starts a new run.  Of course the worker assigned to the eastmost column cannot go eastward, so he simply carves a long southward corridor.  A version of this algorithm, with virtual worker proceeding eastward on heads and northward on tails, is implemented as method `Sidewinder.on` in module `sidewinder.py`.
        An implementation for cylindrical grids is method `Sidewinder.on` in module `cylinder_grid.py`.

      + inward and outward winder trees for polar grids
        It isn't too hard to see how to adapt sidewinder to polar grids once one has done so for cylindrical grids.  Because of outward splitting, the inward case is a bit easier than the outward case.  Here we envision that our virtual workers are each assigned one latitudinal row.  The worker lands in a cell and places a marker atop the counterclockwise wall. He then starts his first clockwise run by flipping his coin -- if he has a choice of going clockwise or inward: heads he carves clockwise, tails he picks one of the cells in his current run and carves inward.  His last run ends when he reaches the marked wall.If, when closing a run, the workers always chooses either the first exit inward or the last exit inward, the result is a binary tree.  Any other choice leads to a cell with three 'children', and thus not a binary tree. (The outward winder algorithm works the same way, except that the worker must choose a cell in the run to carve outward, and, if the cells splits, then the worker must additionally choose an outward neighbor.)  In module `polar_grid.py`, the inward and outward winders are implemented respectively in methods `InWinder.on` and `OutWinder.on`.  By tailoring the `row_choice` and, for outward winder, the `exit_choice` keyword arguments, one may bias the choices to produce lazy binary trees and other specialize configurations.

    * grid-independent spanning tree algorithms
      + uniform spanning trees
        An unbiased spanning tree algorithm is an algorithm which produces any possible spanning tree on a given connected graph with uniform probability.  For lack of a better name, the result is called an _unbiased spanning tree_ or a _uniform spanning tree_.  For grids, the result is a _perfect maze_, customarily called an _unbiased maze_ or a _uniform maze_ or a _random maze_.  Because of computational limitations in pseudorandom number generators, implementations of these algorithms will introduce biases that may be difficult to quantify.
        A bias in maze generation is the tendency to produce certain artifacts.  The long corridors in the terminal row and the terminal column produced by the lazy binary tree algorithm on the rectangular grid is a simple example of a bias.  Depth-first search tends to produce mazes of large _diameter_. (The diameter of a maze or graph is the length of a longest path.)

      + Aldous/Broder (unbiased)
      + Wilson's algorithm (unbiased)
      + growing tree algorithms (DFS, BFS, RFS, Prim)
      + binary tree via search

    * tweaking
      + dead-end removal

 3. Support algorithms

    * Bellman-Ford distance and shortest path
 
 
