# Hamiltonian path
## Problem definition using CSP
### Assignment #2 for NI-UMI 2021


Hamiltonian path is a path in an undirected or directed graph that visits each vertex exactly once.
A Hamiltonian cycle is a Hamiltonian path that is a cycle. 



CSP definition is made of three basic parts:

- *Finite set X*: set of variables, which decide the solution
- *domain range D for variables in X*: available choices for a decision
- *set of constaints C*: defines the constraints for a decison


Given undirected graph G = (V, E) formulate, as CSP, finding solution for Hamiltonian cycle in G.


**CSP** of problem


*X*: 
- undirected graph H = (V<sub>H</sub>, E<sub>H</sub>)


*D*: 
- &forall; v &isin; V: v &isin; V<sub>H</sub> 
  - vertices of graph H are vertices from V
- &forall; e &isin; E: e &isin; E<sub>H</sub>
  - edges of graph H are edges from E 


*C*:
- every vortex can be visited exactly once
- all vertices must be visited
- edges and vertices of graph H must create cycle
  - starting and ending in the same node, there are no leaves or isolated vertices