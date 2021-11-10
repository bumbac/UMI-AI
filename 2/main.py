from graph_generator import generate
from example_graphs import graphs
import pickle
import json
import time
import os
import copy

class Node:
    '''Node for backtracking. Chooses where to go in fixed order.'''
    def __init__(self, ID, edges):
        self.ID = ID
        self.prev = None
        self.nxt = None
        # edges not yet explored
        self.free = edges
        # original list of all edges
        self.original = edges
        # Used in path? If yes, cannot connect here, prevent cycles.
        self.used = False

    def change(self, vertices):
        '''Propose next (not used) edge and return True if there is any.'''
        for nxt in self.free:
            if vertices[nxt].used:
                continue
            self.nxt = nxt
            return True
        return False

    def rollback(self):
        '''Reinitialize node, backtracking went back.'''
        # if self.nxt:
        #     self.free.append(self.nxt.ID)
        self.free = self.original
        self.prev = None
        self.nxt = None
        self.used = False

    def move(self, vertices):
        '''Execute exploration, extend path, remove edge.'''
        self.free.remove(self.nxt)
        self.nxt = vertices[self.nxt]
        self.nxt.prev = self
        self.used = True
        return self.nxt

    def edge(self, other):
        '''Check if there is (free) edge between these two nodes.'''
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
    '''Constraint for checking validity of constructed path.'''
    visited = []
    for node in path:
        # some vortex was visited twice
        if node.ID in visited:
            return False, visited
        visited.append(node.ID)
    return True, visited


def is_hamiltonian(vertices, path):
    '''Constraing for checking the validity of hamiltonian path.'''
    answer, visited = is_valid(path)
    if not answer:
        # path invalid, vortex visited twice
        return False
    if len(vertices) != len(visited):
        # not every vortex was visited
        return False
    else:
        # is there edge between last and first node?
        first = path[0]
        last = path[-1]
        if first.edge(last):
            # path is hamiltonian
            return True
    return False


def csp_ham(vertices):
    '''CSP algorithm using backtracking to find hamiltonian cycle.'''
    # begin arbitrarily at first node
    path = [vertices[0]]
    visited = [vertices[0].ID]
    while not is_hamiltonian(vertices, path):
        current = path[-1]
        valid, blank = is_valid(path)
        if not valid or len(visited) == len(vertices):
            # backtracking
            visited.remove(current.ID)
            current.rollback()
            path.pop()
            if len(path) > 0:
                current = path[-1]
            else:
                # all subgraphs were explored, not hamiltonian
                return False

        # try to expand next node
        while not current.change(vertices):
            # expand not possible, backtrack
            visited.remove(current.ID)
            current.rollback()
            path.pop()
            if len(path) > 0:
                current = path[-1]
            else:
                # all subgraphs were explored, not hamiltonian
                return False

        path.append(current.move(vertices))
        visited.append(path[-1].ID)

    # found Hamiltonian path
    # print("Starting from:", end='')
    # for step in path:
    #     print(step.ID, end='->')
    # print(path[0].ID)
    return True


def make_node_graph(graph):
    vertices = []
    idx = 0
    for v in graph:
        vertices.append(Node(idx, copy.deepcopy(v)))
        idx += 1
    return vertices


def example_run():
    for example in graphs:
        vertices = make_node_graph(example)
        answer = check_possibility(example)
        print("Is Hamiltonian cycle possible? ", "Yes." if answer else "Not sure.")
        solution = csp_ham(vertices)
        if solution is False and answer is True:
            print("\t\t\tMismatch.")


def generated_run(n=1000, size=4):
    mistakes = 0
    fails = []
    print("generated\n\n")
    hamiltonian_proved = 0
    hamiltonian_found = 0
    hamiltonian_not_sure = 0
    hamiltonian_not_found = 0
    for i in range(n):
        graph = generate(size)
        fails.append(copy.deepcopy(graph))
        #print(graph)
        vertices = make_node_graph(graph)
        theorem = check_possibility(copy.deepcopy(graph))
        #print("Is Hamiltonian cycle possible? ", "Yes." if theorem else "Not sure.")
        solution = csp_ham(vertices)
        if solution is False and theorem is True:
            #print("\t\t\tMismatch.")
            mistakes += 1
        # if not solution:
        #     print("\tNot found hamiltonian.")
        hamiltonian_proved += 1 * int(theorem)
        hamiltonian_not_sure += 1 - 1 * int(theorem)
        hamiltonian_found += 1 * int(solution)
        hamiltonian_not_found += 1 - 1 * int(solution)
    print("Graph size: ", size, ", generated graphs: ", n)
    print("Hamiltonians proved by theorem: ", hamiltonian_proved)
    print("Hamiltonians found: ", hamiltonian_found)
    print("Graphs without hamiltonian: ", hamiltonian_not_found)
    print("Mistakes: ", mistakes)
    if mistakes > 0:
        fname = time.time_ns()
        json.dump(fails, open("data/"+str(fname), "w"))


def check_previous_fails():
    mistakes = 0
    for fail in os.listdir("data/"):
        fails = json.load(open("data/" + fail, "r"))
        for graph in fails:
            vertices = make_node_graph(graph)
            answer = check_possibility(graph)
#            print("Is Hamiltonian cycle possible? ", "Yes." if answer else "Not sure.")
            solution = csp_ham(vertices)
            if solution is False and answer is True:
                mistakes += 1
    print("Mistakes in previous failed graphs: ", mistakes)


if __name__ == '__main__':
    #example_run()
    generated_run()
    check_previous_fails()
