Mazelib - an amazing maze library for Python3
Copyright 2022 by Eric Conrad.
Licensed under the Gnu GPL v3.

# mazelib package contents

  * Packaging
    * `__init__.py` - Initialization of the **mazelib** package.
    * `README.md` - This file.
    * `gpl-3.0.txt` - Licensing information.

  * Grid and maze configuration
    * `cell.py` - implements classes `Cell` and `SquareCell`.
    * `grid.py` - implements classes `Grid` (a _stub_) and `RectangularGrid`.
    * `maze_pillow.py` - implements a maze sketching class `MazeSketcher` built upon Python `PIL`.
    * `maze.py` - implements class `Maze` (a usable _stub_).

  * Grid alternatives
    * `cylinder_grid.py` - implements class `CylinderGrid` and adapts some lazy spanning tree algorithms.
    * `Moebius_grid.py` - implements class `MoebiusGrid` for a topological Moebius strip surface.
    * `torus_grid.py` - implements class `TorusGrid.py` for a topological toroidal surface.

  * Maze generation algorithms (see the note on _perfect mazes_ for information on spanning trees)
    * `aldous_broder.py` - for generating uniform random spanning trees using a random walk on the grid.
    * `aldous_broder_wilson.py` - combining the best parts of Aldous/Broder and Wilson's algorithm.
    * `binary_search_tree.py` - for generating binary spanning trees on arbitrary grids.
    * `binary_tree.py` - a lazy binary tree algorithm for generating binary spanning trees on a rectangular grid.
    * `cocktail_shaker_tree.py` - another lazy binary tree algorithm for the rectangular grid.
    * `hunt_kill.py` - for generating spanning trees on arbitrary grids.
    * `recursive_backtracker.py` - some growing tree algorithms for generating spanning trees.
    * `sidewinder.py` - a lazy tree algorithm for generating spanning trees on a rectangular grid.
    * `wilson.py` - for generating uniform random spanning trees using circuit-erased random walks.

  * Miscellaneous algorithms
    * `dead_end.py` - for finding, counting, and removing dead ends in mazes.
    * `distances.py` - for measuring distances and finding shortest paths using Bellman/Ford.
    * `maze_support.py` - some support routines (includes queuing classes).

# Brief Notes

Adapt `__init__.py` as needed. It is set up here to append the **mazelib** folder to the python path and to `import` a few basic modules.

A _perfect maze_ is a spanning tree on a grid. To say a maze is _perfect_ means two things:
  1. the maze is connected, that is, there is an undirect path from every cell to every other cell; and
  2. the maze is circuit-free, that is, there is no more than one such undirected path.

# Passage Carvers

A _passage carver_ is a maze generating algorithm which produces a maze from a grid by linking pairs of cells, that is, by carving passages into walls.  By contrast, a _wall builder_ is a maze generating algorithm which produces a maze from a grid by unlinking pairs of cells, that is by erecting walls to block passage.
 
**Aldous/Broder** uses a random walk of the grid to generate a uniformly random perfect maze.  The walk is complete when all cells are visited.  There are several ways the random walk can be used: the principle ones are _first entry_ and _last exit_.  The first-entry version simply adds the current edge to the spanning tree if the destination is being visited for the first time.  The last-exit version records each edge used in the walk and, on completion, the last edge used to leave a cell is added to the spanning tree. (`from aldous_broder import AldousBroder`)

**Wilson**'s algorithm, asymptotically faster than Aldous/Broder, uses a different approach to the problem of finding a uniformly random spanning tree. In each pass, the explorer is placed somewhere in the unvisited areas and must walk back to the visited region.  As the explorer walks randomly, he sometimes crosses his own path.  The circuit is erased (hence: `circuit-erased random walk`) and the explorer continues.  The result is a simple path from an unvisited cell to the visited region.  This path is added to the visited region (a tree).  When the visited region encompasses the entire grid, the visited region is a spanning tree. (`from wilson import Wilson`)

At the outset, the Aldous/Broder first-entrance algorithm tends to produce a rapidly growing tree spanning the visited region.  But progress slows as more cells are visited. Wilson's Algorithm, by contrast, tends to start out slowly, by gains traction as the unvisited areas become smaller and more fragmented. A **hybrid algorithm** can use both to advantage to produce a spanning tree which, if it is not uniformly random, it is certainly a good approximation. (`from aldous_broder_wilson import HybridABW`)

The **lazy binary spanning tree** algorithm described in chapter 2 of the excellent Jamis Buck book (Jamis Buck. _Mazes for Programmers_. Pragmatic Programmers, 2015.) is not the only way to produce a binary spanning tree, but it is about the simplest way to do so.  It is designed specifically for a 4-connected or 8-connected rectangular grid.  Essentially at each cell, a coin is flipped.  If the flip is a head, an eastward passage is carved where possible; if tails, then northward.  Along the north boundary wall where northward passage is impossible, eastward passages are carved; along the east boundary wall, northward.  It is easy to verify that the resulting spanning tree is a binary tree. (`from binary_tree import BinaryTree`)  While it won't work as described on a cylindrical grid, the lazy binary tree is easily adapted to that grid. The problem is that there is no eastern boundary wall in the grid.  The fix is to put a small east boundary wall somewhere in each row. (`from cylinder_grid import BinaryTree`.)  This adaptation does not easily geralize to the Moebius strip or to the torus.

A simple way of modifying the lazy binary tree algorithm is to alternate going east with going west depending on whether rows are even or odd.  Since this is the same approach used to turn a bubble sort into a cocktail shaker sort, I call this a **cocktail shaker binary spanning tree**.  The result is a maze which, while still very easy to solve, still looks more daunting than the lazy binary tree. (`from cocktail_shaker_tree import CocktailShakerTree`, or for the cylindrical grid, `from cylinder_grid import CocktailShaker`)

A generalization of both these algorithms is the **sidewinder algorithm**. While both the lazy binary tree and the cocktail shaker binary tree are special cases of the sidewinder tree, a sidewinder tree is not, in general, a binary tree.  It is however always a ternary tree.  The algorithm is designed for 4-connected rectangular grids, but is easily adapted for cylindrical grids in the same way as the lazy binary tree. (`from sidewinder import Sidewinder`, or for the cylindrical grid, `from cylinder_grid import Sidewinder`)

While not every grid has a binary spanning tree, many do. On grids that do, a **binary spanning tree** can often be found by using depth-first search, breadth-first search or some variant.  Note that the method will sometimes fail.  When it fails, there will be some isolated cells. (`from binary_search_tree import DFSBinaryTree, BFSBinaryTree, BinarySearchTree`)

Depth-first search can always be used to **grow spanning trees** on a connected grid to produce mazes with long winding corridors.  The algorithm is commonly called _recursive backtracker_, but it really is just depth-first search.  Replace the stack with some other queing technique such as a queue or a heap, and the result is will still be a spanning tree, but with different biases.  (`from recursive_backtracker import DFSSpanningTree, BFSSpanningTree, RFSSpanningTree, Prim, FalsePrim`)  The penultimate algorithm `Prim` is an implementation of Prim's algorithm to find a minimum-weight spanning tree, while that last mentioned, namely `FalsePrim` is an implementation of a maze algorithm called `vertex Prim` that does produce spanning trees, but not minimum-weight spanning trees.  (See chapters 5 and 11 in the Jamis Buck book.)

# Wall Builders

# Miscellaneous Algorithms

The module `dead_end_.py` implements several algorithms for removing dead ends, as well as a means of listing and counting them. Two classes, namely `DeadEnds` and `DeadEndRemoval` are provided:
  * `DeadEnds.on` returns a list of dead ends;
  * `DeadEnds.count` returns the number of dead ends;
  * `DeadEndRemoval.clip` removes dead ends by isolating them with probability `p`; and
  * `DeadEndRemoval.on` is a filter for the remaining dead end removal methods:
    * `DeadEndRemoval.add_passage` chooses an unlinked neighbor at random and links with probability `p`;
    * `DeadEndRemoval.directed_passage` chooses an unlinked neighbor from a list of directions, the order of the list determining the priority, and links with probability `p`; and
    * `DeadEndRemoval.roundabout` chooses an unlinked neighbor which is also a dead end, and links with probability `p`.

The module `distances.py` implements the Bellman/Ford algorithm for finding distances and shortest paths in a maze.  The arcs can be unweighted or weighted, and negative weights are permitted as long as there is no cycle of negative weight.  Implemented are a black box class `Distances` which is returned from the methods, and class `BellmanFord` which implements three methods:
  * `BellmanFord.on` which is a dispatcher which initializes the `Distances` object and calls one of the other two methods;
  * `BellmanFord.unweightedOn` which gives each arc weight 1; and
  * `BellmanFord.weightedOn` which uses the arc weight set at the time the link was last updated.
Distances can be read from the returned `Distances` object `status` using the hash `status.distances`.  A shortest path can be rebult using the hash `status.predecessor` starting with the target cell and continng until the source cell (`status.source`) is found. If a negative weight cycle is present, problem cells will be flagged in the hash `status.flagged`, and the calculated distance in `status.save_distances` -- in this instance, distances in `status.distances` will not be valid -- moreover, reconstructing a shortest path from a flagged cell will result in an infinite loop.

The module `maze_support` contains various kinds of queue structures, including `Unqueue` (random in, random out), `Queue` (first in, first out), `Stack` (last in, first out), and `Heap` (the native heap implementation used as a priority queue).  The key methods are `q.enter` for placing items in the queue, `q.serve` for removing items from the queue, and `q.isEmpty`for determining whether the queue is empty.

# References

 1. Jamis Buck. _Mazes for programmers: code your own twisty little passages_.  Pragmatic Programmers, 2015.

Reference (1) is an excellent introduction to programming in Ruby as well as an excellent introduction to programming mazes.
