class Node:
    def __init__(self, ID, edges):
        self.ID = ID
        self.prev = None
        self.nxt = None
        self.ban = []
        self.free = edges
        self.used = False

    def change(self, vertices):
        for nxt in self.free:
            if vertices[nxt].used:
                continue
            self.nxt = nxt
            return True
        return False

    def rollback(self):
        if self.nxt:
            self.ban.remove(self.nxt.ID)
            self.free.append(self.nxt.ID)
        self.prev = None
        self.nxt = None
        self.used = False

    def move(self, vertices):

        self.free.remove(self.nxt)
        self.ban.append(self.nxt)
        self.nxt = vertices[self.nxt]
        self.nxt.prev = self
        self.used = True
        return self.nxt

    def edge(self, other):
        if other.ID == self.ID:
            return False
        if other.ID in self.free:
            return True
        if other.ID in self.ban:
            return True
        return False


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


def is_valid(path):
    visited = []
    for node in path:
        # some vortex was visited twice
        if node.ID in visited:
            return False, visited
        visited.append(node.ID)
    return True, visited


def is_hamiltonian(vertices, path):
    answer, visited = is_valid(path)
    if not answer:
        return False
    # not every vortex was visited
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


def csp_ham(vertices):
    path = [vertices[0]]
    visited = [vertices[0].ID]
    while not is_hamiltonian(vertices, path):
        current = path[-1]
        valid, blank = is_valid(path)
        if not valid or len(visited) == len(vertices):
            visited.remove(current.ID)
            path.pop()
            current = path[-1]

        while not current.change(vertices):
            visited.remove(current.ID)
            current.rollback()
            path.pop()
            if len(path) > 0:
                current = path[-1]
            else:
                print(False)
                return False

        path.append(current.move(vertices))
        visited.append(path[-1].ID)
    print("Starting from:", end='')
    for step in path:
        print(step.ID, end='->')
    print(path[0].ID)
    return True


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
    for graph in graphs:
        vertices = []
        idx = 0
        for v in graph:
            vertices.append(Node(idx, v))
            idx += 1

        print("Is Hamiltonian cycle possible? ", "Yes." if check_possibility(graph) else "No.")

        csp_ham(vertices)
