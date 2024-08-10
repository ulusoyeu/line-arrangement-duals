# line-arrangement-duals

This repository will include C++ / Python code to implement and analyse the dual graphs induced by certain convex-configurations. The goals to include are:

1) Use CGAL to access the dual / incidence graph structures of point configurations in 2D.
2) Search for relations between the existence of a certain convex subset and graph-minor relations of the dual graphs.

# Configuration

Initially, it started as a project to implement the line arrangement algorithm specified in [1], yet then realized that the CGAL implementation is more robust and efficient although it is annoying to set up.
The most accurate way to set up is to exactly follow the specifications in https://doc.cgal.org/latest/Manual/windows.html, however there are some parts that are unclear. As a future reference, below are some important notes on configuring the CGAL library.

1) In the project folder, create the CMakeLists.txt file using the built in .\CGAL-5.6.1\scripts\cgal_create_CMakeLists file.
2) Once the file exists, create a subdiretory named \build using "mkdir build" command.
3) Change to the \build directory using "cd build" command.
4) Run "cmake-gui .." command - there first configure the files, by clicking configure, then picking the latest version of VS and x64.
5) Then click "Generate".
6) Once it is all created, there will be a file named <your_project_name>.sln. Open it in VS.
7) Build it from the tabs (and set your project as startup project by right clicking on it, and clicking "Set as Startup Project")
8) Run it. (your exe file should be in the Debug subdirectory of \build if you built it there)

## Notes

There are other annoying issues surrounding the configuration process.

1) If it cannot find libgmp-10.dll or libmpfr-4.dll, in the auxiliary files of your CGAL directory, find the corresponding dll files and add them to the folder with your .exe files.


[1] Mark de Berg, Otfried Cheong, Marc van Kreveld, and Mark Overmars. 2008. Computational Geometry: Algorithms and Applications (3rd ed. ed.). Springer-Verlag TELOS, Santa Clara, CA, USA.
