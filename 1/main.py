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


def printroom(room):
    for y_line in room:
        for node in y_line:
            print(node.symbol, end='')
        print('\n')


def adjacency_matrix(room):
    x_lim = len(room[0])
    y_lim = len(room)
    matrix = [[[] for i in range(x_lim)] for j in range(y_lim)]
    for y_line in room:
        for node in y_line:
            if node.symbol == 'x':
                continue
            for x_offset in [1, 0, -1]:
                for y_offset in [1, 0, -1]:
                    if x_offset*y_offset == 0:
                        x_curr = node.x + x_offset
                        y_curr = node.y + y_offset
                        if x_lim > x_curr >= 0 and 0 <= y_curr < y_lim:
                            if room[y_curr][x_curr].symbol != 'x':
                                matrix[node.y][node.x].append(room[y_curr][x_curr])
    return matrix


def mst(room, dust_locations, robot_location):
    st = []
    bfs_tree = bfs(copy.deepcopy(room), robot_location, spanning_tree=True)
    rep = 1
    for dust in dust_locations:
        st.append([0, bfs_tree[dust[1]][dust[0]]])
        node = st[-1][1]
        price = 0
        while node:
            price += 1
            if node.symbol == 'O':
                print("Found start.")
                break
            node.symbol = str(rep)
            node = node.prev
        rep += 1
        st[-1][0] = price
    printroom(bfs_tree)
    sorted_st = sorted(st, key=lambda x: x[0])


    adj_matrix = adjacency_matrix(room)


def task1(room):
    dust_locations = []
    robot_location = (0, 0)
    y = 0
    for y_line in room:
        x = 0
        for node in y_line:
            if node.symbol == 'O':
                robot_location = (x, y)
            if node.symbol == '@':
                dust_locations.append((x, y))
            x += 1
        y += 1
    start_time = time.time_ns()
    solution_bfs = vacuum_bfs(copy.deepcopy(room), robot_location)
    benchmark = time.time_ns() - start_time
    print("BENCHMARK BFS", benchmark)
    printroom(solution_bfs)
    solution_mst = mst(room, dust_locations, robot_location)


def bfs(room, robot_location, spanning_tree=False):
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
