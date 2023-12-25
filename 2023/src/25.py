import argparse
import pathlib
import random
from copy import deepcopy


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    # using Karger's algorithm

    edges = []
    node_names = []
    nodes_contained_per_node = {}
    for line in inp:
        words = line.split()
        lhs = words[0][:-1]
        if lhs not in node_names:
            node_names.append(lhs)
            nodes_contained_per_node[lhs] = 1

        for rhs in words[1:]:
            if rhs not in node_names:
                node_names.append(rhs)
                nodes_contained_per_node[rhs] = 1

            if not ([rhs, lhs] in edges or [lhs, rhs] in edges):
                edges.append([rhs, lhs])

    while True:
        edges_copy = deepcopy(edges)
        nr_nodes_left = len(node_names)
        new_node_name = '0'
        while nr_nodes_left > 2:
            r = random.randint(0, len(edges_copy) - 1)  # edge to merge
            node1, node2 = edges_copy[r]  # nodes to merge

            # rename all mentions of old node names in edges list
            for i in range(len(edges_copy)-1, -1, -1):
                if edges_copy[i][0] in [node1, node2]:
                    if edges_copy[i][1] in [node1, node2]:
                        edges_copy.pop(i)
                    else:
                        edges_copy[i][0] = new_node_name
                elif edges_copy[i][1] in [node1, node2]:
                    edges_copy[i][1] = new_node_name

            nodes_contained_per_node[new_node_name] = nodes_contained_per_node[node1] + nodes_contained_per_node[node2]

            nr_nodes_left -= 1
            new_node_name = str(int(new_node_name) + 1)

        if len(edges_copy) == 3:
            return nodes_contained_per_node[edges_copy[0][0]] * nodes_contained_per_node[edges_copy[0][1]]

def b(_):
    return 'Merry Christmas!'

def test_a():
    assert a(get_input()) == 562978

def test_b():
    assert b(get_input()) == 'Merry Christmas!'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    parser.add_argument('-p', '--profile', dest='profile', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    if args.profile:
        print('\n### Profiling part 1 ###\n')
        __import__('cProfile').run('a(inp)')
        print('### Profiling part 2 ###\n')
        __import__('cProfile').run('b(inp)')
    else:
        #print('a:', a_faster(inp))
        #print('a:', a_remove_nodes(inp))
        print('a:', a(inp))
        print('b:', b(inp))
