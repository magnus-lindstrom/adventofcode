import sys
import argparse
from itertools import combinations_with_replacement
from more_itertools import distinct_permutations
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def recursive_solver(i_op, nrs, operators, results_map):
    if i_op == len(operators) - 1:  # at the end of the equation
        if operators[i_op] == '+':
            return results_map, nrs[-2] + nrs[-1]
        elif operators[i_op] == '*':
            return results_map, nrs[-2] * nrs[-1]
        elif operators[i_op] == '||':
            # backwards order since we are solving back to front
            return results_map, int(str(nrs[-1]) + str(nrs[-2]))
        else:
            sys.exit(1)

    remaining_operators = operators[i_op:]
    remaining_nrs = nrs[i_op:]
    key = (tuple(remaining_nrs), tuple(remaining_operators))
    if key in results_map:
        remaining_value = results_map[key]
    else:
        results_map, remaining_value = recursive_solver(i_op + 1, nrs, operators, results_map)
        results_map[key] = remaining_value


    if operators[i_op] == '+':
        return results_map, nrs[i_op] + remaining_value
    elif operators[i_op] == '*':
        return results_map, nrs[i_op] * remaining_value
    elif operators[i_op] == '||':
        # backwards order since we are solving back to front
        return results_map, int(str(remaining_value) + str(nrs[i_op]))
    else:
        sys.exit(1)

def common_func(inp, operators):
    summ = 0
    for line in inp:
        words = line.split()
        result = int(words[0][:-1])
        nrs = [int(n) for n in words[1:]]
        nrs.reverse()  # because I'm solving from back to front
        nr_of_operators = len(nrs) - 1
        combinations = combinations_with_replacement(operators, nr_of_operators)
        results_map = {}
        line_is_done = False
        for comb in combinations:
            for perm in distinct_permutations(comb):
                results_map, prod = recursive_solver(0, nrs, perm, results_map)
                if prod == result:
                    summ += result
                    line_is_done = True
                    break
            if line_is_done: break
    return summ

def a(inp):
    return common_func(inp, ['+', '*'])

def b(inp):
    return common_func(inp, ['+', '*', '||'])

def test_a():
    assert a(get_input()) == 12553187650171

def test_b():
    assert b(get_input()) == 96779702119491

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
        print('a:', a(inp))
        print('b:', b(inp))
