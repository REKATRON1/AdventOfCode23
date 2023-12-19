raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

class node():
    def __init__(self, _label, _next_l=None, _next_r=None):
        self.label = _label
        self.left = _next_l
        self.right = _next_r
    def next(self, is_left=True):
        if is_left and self.left != None and type(self.left) != str:
            return self.left
        if not is_left and self.right != None and type(self.right) != str:
            return self.right
        return None
    def set_node(self, node):
        if type(self.left) == str:
            if node.label == self.left:
                self.left = node
        if type(self.right) == str:
            if node.label == self.right:
                self.right = node

def input_conversion(inp):
    moves = inp[0]

    nodes = {}
    req_node = {}
    for line in inp[2:]:
        str_node = line.replace('=','').replace('(','').replace(',','').replace(')','').split()
        node_neighbours = nodes.get(str_node[1]) or str_node[1], nodes.get(str_node[2]) or str_node[2]
        new_node = node(str_node[0], node_neighbours[0], node_neighbours[1])
        if type(new_node.left) == str:
            if req_node.get(new_node.left) == None:
                req_node[new_node.left] = [new_node]
            else:
                req_node[new_node.left].append(new_node)
        if type(new_node.right) == str:
            if req_node.get(new_node.right) == None:
                req_node[new_node.right] = [new_node]
            else:
                req_node[new_node.right].append(new_node)
        if req_node.get(new_node.label) != None:
            for n in req_node[new_node.label]:
                n.set_node(new_node)
        nodes[str_node[0]] = new_node

    return moves, nodes

def both_parts(moves, nodes, start_node='AAA', end_node='ZZZ', skip_first=False):
    if nodes.get(start_node) == None:
        return -1
    steps = 0
    start = nodes[start_node]
    current_node = start
    visited_nodes_after_cycle = []
    while skip_first or (current_node.label != end_node and not current_node in visited_nodes_after_cycle):
        if not skip_first:
            visited_nodes_after_cycle.append(current_node)
        else:
            skip_first = False
        for move in moves:
            if move == 'L':
                current_node = current_node.next(True)
            elif move == 'R':
                current_node = current_node.next(False)
            steps += 1
    if current_node in visited_nodes_after_cycle:
        return -1
    else:
        return steps

import numpy as np

def smallest_common_stepamount(iterator):
    prod = iterator[0]
    for n in iterator[1:]:
        prod *= int(n/np.gcd(prod, n))
    return prod

def part2(moves, nodes):
    start_nodes = []
    end_nodes = []
    for label, n in nodes.items():
        if label[-1] == 'A':
            start_nodes.append(n.label)
        elif label[-1] == 'Z':
            end_nodes.append(n.label)
    steps_per_node = {s1: {e1: -1 for e1 in end_nodes} for s1 in start_nodes}
    cycle_steps = {e1: {e2: -1 for e2 in end_nodes} for e1 in end_nodes}
    for s1 in start_nodes:
        for e1 in end_nodes:
            steps_per_node[s1][e1] = both_parts(moves, nodes, s1, e1)
    for e1 in end_nodes:
        for e2 in end_nodes:
            cycle_steps[e1][e2] = both_parts(moves, nodes, e1, e2, skip_first=True)

    #Assumption thats just true for the given input: for every end-node there is just one 
    #end-cycle that lead to itself + just one end-node per start node with stepamount equal to the cycle size of the end-node...
    cycles = []
    for e in end_nodes:
        cycles.append(cycle_steps[e][e])

    return smallest_common_stepamount(cycles)

moves, nodes = input_conversion(inp)
sol1 = both_parts(moves, nodes) #=>13939

moves, nodes = input_conversion(inp)
sol2 = part2(moves, nodes)

print(sol1, sol2) #=>33865167419
