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




### *Time to think*
Finding an hamiltonian cycle is a problem in graph theory.
It would be wise to see if there is some way to test the existence
of Hamiltonian cycle in graph without exhaustive construction.

### Dirac's theorem
    A simple graph with n vertices (n≥3) is Hamiltonian if:
    every vertex has degree n/2 or greater.
### Ore's theorem
    A simple graph with n vertices (n≥3) is Hamiltonian if:
    δ(x)+δ(y) ≥ n for each pair of non-adjacent vertices x and y.

These theorems are in the form of an implication to prove that in some conditions, there surely is
a Hamiltonian cycle present. Unfortunately, it does not tell us
in which conditions Hamiltonian cycle is not present.

### *Time to make algorithm*

### A) Backtracking

Algorithms using backtracking utilize the ability of algorithm
to spot a dead-end (incorrect solution) and by going step or steps back,
choose a different way to find solution.

My algorithm checks in each step whether it found the solution and if the step
was a valid move. Both of these checks are in described in CSP as the
set of constraints *C*.

*C*:

- every vortex can be visited exactly once
```Python
  def is_valid(path):
      visited = []
      for node in path:
          # some vortex was visited twice
          if node.ID in visited:
              return False, visited
          visited.append(node.ID)
      return True, visited
```


- all vertices must be visited
```Python
  def is_hamiltonian(vertices, path):
    answer, visited = is_valid(path)
    if not answer:
        return False
    # not every vortex was visited
    if len(vertices) != len(visited):
        return False
```

- edges and vertices of graph H must create cycle
  - starting and ending in the same node, there are no leaves or isolated vertices

  
*function is_hamiltonian continues*
```Python
      if len(vertices) != len(visited):
          return False
      else:
          # there is edge between last and first node
          first = path[0]
          last = path[-1]
          if first.edge(last):
              # path is hamiltonian
              return True
    return False
```
