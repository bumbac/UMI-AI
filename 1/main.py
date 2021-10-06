import copy
import time


class Node:
    def __init__(self, symbol, prev, x, y, ID):
        self.symbol = symbol
        self.flag = 0
        self.prev = prev
        self.x = x
        self.y = y
        self.id = ID


def hamiltonian(vertices, double_edges):
    guide = {}
    node_pos = 0
    for v in vertices:
        guide[v.id] = node_pos
        node_pos += 1
    node_pos = 0
    walk = []
    while len(double_edges[node_pos]) != 0:
        next_node = double_edges[node_pos][0]
        for next_edge in double_edges[node_pos]:
            if double_edges[node_pos].count(next_edge) == 2:
                next_node = next_edge
                break
        reverse_node_pos = guide[next_node.id]
        this_node = vertices[node_pos]
        double_edges[node_pos].remove(next_node)
        double_edges[reverse_node_pos].remove(this_node)
        walk.append(vertices[node_pos])
        print(walk)
        node_pos = guide[next_node.id]
    # shortcut
    visited = []
    pos = 0
    limit = len(walk)
    while pos < limit:
        element = walk[pos]
        if element not in visited:
            visited.append(element)
        pos += 1
    return visited


def eulerian(vertices):
    double_edges = [[] for i in range((len(vertices)))]
    node_pos = 0
    for vortex in vertices:
        prev = vortex.prev
        if prev:
            double_edges[node_pos].append(prev)
            double_edges[node_pos].append(prev)
            idx = vertices.index(prev)
            double_edges[idx].append(vortex)
            double_edges[idx].append(vortex)
        node_pos += 1
    return double_edges


def edge_price(start, end, room):
    return bfs(room, (start.x, start.y), spanning_tree=True, ID=end.id)


def mst(room, dust_nodes, robot_location):
    printroom(room)
    edges = [[99999 for i in range(len(dust_nodes) + 1)] for i in range((len(dust_nodes) + 1))]
    vertices = [room[robot_location[1]][robot_location[0]]]
    vertices.extend(dust_nodes)
    y = 0
    for start in vertices:
        x = 0
        for end in vertices:
            if start == end:
                x += 1
                continue
            edges[y][x] = edge_price(start, end, copy.deepcopy(room))
            x += 1
        y += 1
    for node in vertices:
        print(node.id, node.symbol)
    node = vertices[0]
    node_pos = 0
    free_nodes = [i for i in range(len(vertices))]
    free_nodes.remove(node_pos)
    while free_nodes:
        next_pos = edges[node_pos].index(min(edges[node_pos]))
        edges[node_pos][next_pos] = 99999
        if next_pos not in free_nodes:
            continue
        vertices[next_pos].prev = node
        node = vertices[next_pos]
        node_pos = next_pos
        free_nodes.remove(node_pos)
    return vertices

# MST: first create minimum spanning tree of nodes: robot_location and all dust_nodes
# graph is complete Kn graph, where distance is computed using BFS between nodes(robot and dust nodes)

# EULERIAN: double every edge between nodes and create Eulerian walk = sequence of nodes which can be visited > 1

# HAMILTIONIAN: because all dust nodes and robot nodes are accessible, create shortcuts by leaving out
# already accessed nodes (from 1-2-2-3-4-5-5-6 create 1-2-3-4-5-6)

# this sequence is proposed order of visit between nodes,
def vacuum_smart(room, dust_nodes, robot_location):
    vertices = mst(room, dust_nodes, robot_location)
    print("MST")
    for v in vertices:
        print(v.id)
        prev = v.prev
        while prev:
            print(prev.id)
            prev = prev.prev
        print()
    double_edges = eulerian(vertices)
    print("EULERIAN WALK")
    pos = 0
    for e in double_edges:
        print("FROM", vertices[pos].id)
        pos += 1
        for node in e:
            print(node.id)
        print()
    print("HAMILTONIAN")
    walk = hamiltonian(vertices, double_edges)
    for w in walk:
        print(w.id, end='->')
    



def task1(room):
    dust_locations = []
    dust_nodes = []
    robot_location = (0, 0)
    y = 0
    for y_line in room:
        x = 0
        for node in y_line:
            if node.symbol == 'O':
                robot_location = (x, y)
            if node.symbol == '@':
                dust_locations.append((x, y))
                dust_nodes.append(node)
            x += 1
        y += 1
    # start_time = time.time_ns()
    # solution_bfs = vacuum_bfs(copy.deepcopy(room), robot_location)
    # benchmark = time.time_ns() - start_time
    # print("BENCHMARK BFS", benchmark)
    # printroom(solution_bfs)
    #solution_mst = mst(room, dust_locations, robot_location)
    vacuum_smart(room, dust_nodes, robot_location)



def bfs(room, robot_location, spanning_tree=False, ID=None):
    start = room[robot_location[1]][robot_location[0]]
    x_lim = len(room[0])
    y_lim = len(room)
    start.flag = 1
    queue = [start]
    visited = []
    while queue:
        node = queue.pop(0)
        if node.flag == 1:
            node.flag = 2
            if node.id == ID:
                price = 0
                while node:
                    node = node.prev
                    price += 1
                return price
            if node.symbol == '@':
                if not spanning_tree:
                    return node
            visited.append(node)
            for x_offset in [1, 0, -1]:
                for y_offset in [1, 0, -1]:
                    if x_offset*y_offset == 0:
                        x_curr = node.x + x_offset
                        y_curr = node.y + y_offset
                        if x_lim > x_curr >= 0 and 0 <= y_curr < y_lim:
                            nbor = room[y_curr][x_curr]
                            if nbor.flag == 0 and nbor.symbol != 'x':
                                nbor.flag = 1
                                nbor.prev = node
                                queue.append(nbor)
    if spanning_tree:
        return room
    else:
        return None


def vacuum_bfs(room, robot_location):
    dust = bfs(copy.deepcopy(room), robot_location)
    moves = []
    rep = 'a'
    position = 1
    while dust:
        robot_location = (dust.x, dust.y)
        room[dust.y][dust.x].symbol = str(position)
        while dust.prev:
            dust.symbol = rep
            room[dust.y][dust.x].symbol = rep
            moves.append(dust)
            dust = dust.prev
        moves.append(dust)
        dust = bfs(copy.deepcopy(room), robot_location)
        rep = chr(ord(rep) + 1)
        position += 1
    return room


def printroom(room):
    for y_line in room:
        for node in y_line:
            print(node.symbol, end='')
        print('\n')


def readfile(filename):
    f = open(filename)
    flag = True
    room = []
    y = 0
    id = 1
    while flag:
        line = f.readline()
        if not line:
            flag = False
        room.append([])
        x = 0
        for symbol in line:
            if symbol != '\n':
                room[y].append(Node(symbol, None, x, y, id))
                id += 1
            x += 1
        y += 1
    room = room[:-1]
    return room


if __name__ == '__main__':
    room = readfile('data/3_1.txt')
    task1(room)
