import random
import time

def generate(n):
    random.seed(time.time_ns())
    vertices = [
        [] for i in range(n)
    ]

    for node_start in range(n):
        n_edges = random.randint(0, n)
        for edge in range(n_edges):
            node_end = random.randint(0, n-1)
            if node_start == node_end:
                continue
            if node_end in vertices[node_start]:
                continue
            if node_start in vertices[node_end]:
                continue
            else:
                vertices[node_start].append(node_end)
                vertices[node_end].append(node_start)
    return vertices
