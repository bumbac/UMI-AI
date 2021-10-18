import random


def generate(n):
    vertices = [
        [] for i in range(n)
    ]

    for node_start in range(n):
        n_edges = random.randint(0, n)
        for node_end in range(n_edges):
            where = random.randint(0, n)
            if node_start == node_end:
                continue
            if node_end in vertices[node_start]:
                continue
            else:
                vertices[node_start].append(node_end)
                vertices[node_end].append(node_start)
    return vertices
