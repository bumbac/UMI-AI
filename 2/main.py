def check_possibility(vertices):
    # diracs theorem
    min_level = 0
    n = len(vertices)
    if n < 3:
        return False
    for vortex in vertices:
        min_level = max(min_level, len(vortex))
    if min_level < n/2:
        return False
    # orecs theorem
    vertices_id = [i for i in range(len(vertices))]
    for v in vertices_id:
        for w in vertices_id:
            # identity
            if v == w:
                continue
            # non-adjacent vertices
            if w in vertices[v]:
                continue
            deg_v = len(vertices[v])
            deg_w = len(vertices[w])
            if (deg_v + deg_w) < n:
                return False
    return True


def csp_ham(vertices):
    path = []
    visited = []
    for v in range(len(vertices)):
        if v in visited:
            pass
    return False


if __name__ == '__main__':
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
    vertices = [
        # node 0
        [1, 2, 4],
        # node 1
        [0, 3, 4],
        # node 2
        [0, 3, 4],
        # node 3
        [2, 1],
        # node 4
        [0, 1, 2],
    ]

    print("Is Hamiltonian cycle possible? ", "Yes." if check_possibility(triv_vertices_no2) else "No.")
    answer = csp_ham(vertices)
