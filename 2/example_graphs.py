# trivial example with Hamiltonian cycle
#    2
#  /   \
# 0  -  1
triv_vertices_yes = [
    [1, 2],
    [0, 2],
    [0, 1]
]

# trivial example without Hamiltonian cycle
#    2
#      \
# 0  -  1
triv_vertices_no = [
    [1],
    [0, 2],
    [1]
]

# trivial example without Hamiltonian cycle
#    2  -  3
#  /   \
# 0  -  1
triv_vertices_no2 = [
    [1, 2],
    [0, 2],
    [0, 1, 3],
    [2]
]

# trivial example with Hamiltonian cycle
#    2   -  3
#  /   \   /
# 0  -   1
triv_vertices_yes2 = [
    [1, 2],
    [0, 2, 3],
    [0, 1, 3],
    [2, 1]
]

# trivial example without Hamiltonian cycle
#    2   -  3    -   4
#  /   \   /       /   \
# 0  -   1        5  -  6
triv_vertices_no3 = [
    # 0
    [1, 2],
    # 1
    [0, 2, 3],
    # 2
    [0, 1, 3],
    # 3
    [2, 1, 4],
    # 4
    [3, 5, 6],
    # 5
    [4, 6],
    # 6
    [5, 4]
]

# trivial example with Hamiltonian cycle
#    2   -  3    -   4
#  /   \   /       /   \
# 0  -   1    -   5  -  6
triv_vertices_yes3 = [
    # 0
    [1, 2],
    # 1
    [0, 2, 3, 5],
    # 2
    [0, 1, 3],
    # 3
    [2, 1, 4],
    # 4
    [3, 5, 6],
    # 5
    [1, 4, 6],
    # 6
    [4, 5]
]

# trivial example without Hamiltonian cycle
#    2   -  3    -   4
#  /   \   /       /   \
# 0  -   1   -    5  -  6  - 7
triv_vertices_no4 = [
    # 0
    [1, 2],
    # 1
    [0, 2, 3, 5],
    # 2
    [0, 1, 3],
    # 3
    [2, 1, 4],
    # 4
    [3, 5, 6],
    # 5
    [1, 4, 6],
    # 6
    [5, 4, 7],
    # 7
    [6]
]

vertices1 = [
    # node 0
    [1, 2, 4],
    # node 1
    [0, 3, 4],
    # node 2
    [0, 3, 4],
    # node 3
    [2, 1],
    # node 4
    [0, 1, 2]
]

graphs = [triv_vertices_yes, triv_vertices_yes2, triv_vertices_yes3,
          triv_vertices_no, triv_vertices_no2, triv_vertices_no3, triv_vertices_no4,
          vertices1]
