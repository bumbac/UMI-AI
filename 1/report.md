# VACUUM ROBOT
## OPTIMAL TOUR SOLUTION
### Assignment \#1 for NI-UMI 2021

Robot is located on a rectangle grid where he can move in discrete steps
in 4 directions (up, down, left, right). On the grid are located dust particles that need to be collected.
Robot cannot enter walls or leave the grid.

Symbols on the grid are:

Robot: **O**

Dust: **@**

Wall: **x**

###First solution
#### Naive solution using BFS and hungry algorithm
Robot locates dust closest to him using BFS.
He collects this dust, and then robot repeats the process of localizing the closest dust using BFS.

This approach provides suboptimal results, for example on grid:

Steps:
1. @@.O..@
2. @@O...@
3. @O....@

and then robot needs to return to the rightmost cell.

###Second solution
#### Custom algorithm inspired by TSP tour approximated using MST
In preprocessing phase a complete graph *K* of dust vertices and initial robot location is created.
The edges are weighted by the distance between two vertices.
Later a MST is created using hungry algorithm. 
Each edge in MST is duplicated and Eulerian tour (each edge visited only once) is created. The algorithm
does not take into account the weight of any edge. Simple way to find Eulerian tour is to always 
choose an edge that is duplicated. By choosing an edge that has a duplicate, algorithm can always return 
and does not leave any node unvisited. This approach is called *not burning bridges*.

![alt text](https://slaystudy.com/wp-content/uploads/2020/07/eulercircuit.png)

*Example of Eulerian path, image taken from slaystudy.com/*


Eulerian tour is a sequence of visited vertices, in our case each vortex is visited twice because 
of duplicated edges. Since on a grid each vortex can be reached from any other vortex algorithm can make
shortcuts in the Eulerian tour by skipping every vortex that has been already visited.

For example: 

Euclidean tour  A-B-E-C-D-C-F-C-G

using shortcuts A-B-E-C-D-F-G

After this process a Hamiltonian tour (sequence of vertices) is created where each vortex is visited exactly once.
Robot will collect dust particles in this sequence.

This approach provides suboptimal results.




