import copy


class Node:
    def __init__(self, symbol, prev, x, y, ID):
        self.symbol = symbol
        self.flag = 0
        self.prev = prev
        self.x = x
        self.y = y
        self.id = ID


def hamiltonian(vertices, double_edges):
    """
    visit each node only once by creating shortcuts between nodes
    """
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
        node_pos = guide[next_node.id]
    print("\nSMART VACUUM SEQUENCE OF STEPS")
    # shortcut
    visited = []
    pos = 0
    limit = len(walk)
    while pos < limit:
        element = walk[pos]
        if element not in visited:
            visited.append(element)
            print(element.id, end='->')
        pos += 1
    print('FINISH')
    return visited


def eulerian(vertices):
    """
    Add extra edge between nodes connected in MST
    visit each edge once, create walk
    """
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
    """
    create complete graph of vertices from dust_nodes and robot location
    calculate price of every edge between vertices
    create minimal spanning tree by hungry algorithm by assigning previous
    node to each node
    """
    vertices = [room[robot_location[1]][robot_location[0]]]
    vertices.extend(dust_nodes)
    min_edges = []
    aux_vertices = copy.deepcopy(vertices)
    for start in vertices:
        for end in aux_vertices:
            if start.id == end.id:
                continue
            price = edge_price(start, end, copy.deepcopy(room))
            min_edges.append([price, start, end])
        aux_vertices.pop(0)
    min_edges.sort(key=lambda x: x[0], reverse=True)
    free_nodes = []
    guide = {}
    i = 0
    used_nodes = []
    for v in vertices:
        free_nodes.append(v.id)
        guide[v.id] = i
        i += 1
    m = []
    while len(min_edges) > 0:
        last = min_edges.pop()
        flag = False
        if last[1].id not in used_nodes:
            used_nodes.append(last[1].id)
            flag = True
        if flag:
            last[2].prev = last[1]
            m.append((last[1], last[2]))
            prev_pos = guide[last[1].id]
            pos = guide[last[2].id]
            vertices[prev_pos].prev = vertices[pos]
    return vertices

# MST: first create minimum spanning tree of nodes: robot_location and all dust_nodes
# graph is complete Kn graph, where distance is computed using BFS between nodes(robot and dust nodes)

# EULERIAN: double every edge between nodes and create Eulerian walk = sequence of nodes which can be visited > 1

# HAMILTIONIAN: because all dust nodes and robot nodes are accessible, create shortcuts by leaving out
# already accessed nodes (from 1-2-2-3-4-5-5-6 create 1-2-3-4-5-6)

# this sequence is proposed order of visit between nodes
def vacuum_smart(room, dust_nodes, robot_location):
    # MST
    vertices = mst(room, dust_nodes, robot_location)
    # EULERIAN
    double_edges = eulerian(vertices)
    # HAMILTONIAN
    walk = hamiltonian(vertices, double_edges)
    steps = 0
    # clean node.prev values for calculating steps
    for yline in room:
        for v in yline:
            if v.flag != 0:
                print(v.id, "not zero")
            if v.prev:
                v.prev = None
    # calculate price of tour for collecting all dust

    for i in range(len(walk) - 1):
        steps += edge_price(walk[i], walk[i+1], copy.deepcopy(room))
    print("SMART VACUUM:", steps, "steps.")
    return steps


def task1(room):
    """
    Vacuum cleaner, find route to collect all dust (symbol @)
    Robot starts at position with symbol big O
    Symbol x is wall, other is accessible
    """
    printroom(room)
    dust_locations = []
    dust_nodes = []
    robot_location = (0, 0)
    y = 0
    # find locations of all dusts
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
    solution_bfs = vacuum_bfs(copy.deepcopy(room), robot_location)
    solutin_smart = vacuum_smart(room, dust_nodes, robot_location)


def bfs(room, robot_location, spanning_tree=False, ID=None):
    """
    Using bfs find dust (or node with ID).
    """
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
    """
    Naive solution - find dust closest to robot.
    Collect it and find another closest to current location.
    All using BFS.
    """
    start_location = room[robot_location[1]][robot_location[0]]
    dust = bfs(copy.deepcopy(room), robot_location)
    moves = []
    print('Robot location:', robot_location)
    while dust:
        robot_location = (dust.x, dust.y)
        room[dust.y][dust.x].symbol = '.'
        while dust.prev:
            moves.append(dust)
            dust = dust.prev
        dust = bfs(copy.deepcopy(room), robot_location)
    print("\nBFS:", len(moves), "steps.")
    print("SEQUENCE OF DUSTS")
    start_location.symbol = 'O'
    moves.insert(0, start_location)
    visited = []
    for node in moves:
        if node.symbol == '@' or node.symbol =='O':
            if node.id not in visited:
                print(node.id, end='->')
                visited.append(node.id)
    print("FINISH")
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
    room = readfile('data/3_2.txt')
    task1(room)
