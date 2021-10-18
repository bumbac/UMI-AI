from graph_generator import generate
from example_graphs import graphs


class Node:
    def __init__(self, ID, edges):
        self.ID = ID
        self.prev = None
        self.nxt = None
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
            self.free.append(self.nxt.ID)
        self.prev = None
        self.nxt = None
        self.used = False

    def move(self, vertices):

        self.free.remove(self.nxt)
        self.nxt = vertices[self.nxt]
        self.nxt.prev = self
        self.used = True
        return self.nxt

    def edge(self, other):
        if other.ID == self.ID:
            return False
        if other.ID in self.free:
            return True
        return False


def check_possibility(vertices):
    # ONLY INFORMATIONAL
    # theorem in the form of implication, not equivalence
    # diracs theorem
    min_level = 0
    n = len(vertices)
    if n < 3:
        return False
    for vortex in vertices:
        min_level = max(min_level, len(vortex))
    if min_level < n/2:
        return False
    # ores theorem
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
            if len(path) > 0:
                current = path[-1]
            else:
                return False

        while not current.change(vertices):
            visited.remove(current.ID)
            current.rollback()
            path.pop()
            if len(path) > 0:
                current = path[-1]
            else:
                return False

        path.append(current.move(vertices))
        visited.append(path[-1].ID)
    print("Starting from:", end='')
    for step in path:
        print(step.ID, end='->')
    print(path[0].ID)
    return True


def make_node_graph(graph):
    vertices = []
    idx = 0
    for v in graph:
        vertices.append(Node(idx, v))
        idx += 1
    return vertices


if __name__ == '__main__':
    for example in graphs:
        vertices = make_node_graph(example)
        answer = check_possibility(example)
        print("Is Hamiltonian cycle possible? ", "Yes." if answer else "Not sure.")
        solution = csp_ham(vertices)
        if solution is False and answer is True:
            print("\t\t\tMismatch.")

    mistakes = 0
    print("generated\n\n")
    for i in range(1000):
        graph = generate(20)
        vertices = make_node_graph(graph)
        answer = check_possibility(graph)
        print("Is Hamiltonian cycle possible? ", "Yes." if answer else "Not sure.")
        solution = csp_ham(vertices)
        if solution is False and answer is True:
            print("\t\t\tMismatch.")
            mistakes += 1
        else:
            print(solution)
    print("mistakes", mistakes)
