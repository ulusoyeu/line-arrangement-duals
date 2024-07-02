# line-arrangement-duals

This repository includes the codes used to experiment with the dual graphs induced by certain convex-configurations. The goals to include are:

1) Implement the DCEL Data Structure (specific to be used in line arrangements)
2) Implement the $O(n^2)$ time / space algorithm to find the DCEL of a line arrangement [1]
3) Give alternative representations / substructures of line arrangements (Dual Graph of an arrangement / Incidence Graph)

Furthermore, for the specific analysis cases, we will focus on line arrangements created by a set of points, by adding all lines created by pairs of points.
The goal is to provide a nice way of representing the dual graph of such arrangements, and provide the tools to analyse the relevant concepts, such as graph-minor relation, for detecting convex subsets.

[1] Mark de Berg, Otfried Cheong, Marc van Kreveld, and Mark Overmars. 2008. Computational Geometry: Algorithms and Applications (3rd ed. ed.). Springer-Verlag TELOS, Santa Clara, CA, USA.
