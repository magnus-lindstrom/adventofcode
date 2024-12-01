import argparse
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    list1 = []
    list2 = []
    for line in inp:
        nr1 = int(line.split()[0])
        list1.append(nr1)
        nr2 = int(line.split()[1])
        list2.append(nr2)
    list1.sort()
    list2.sort()
    summ = 0
    for nr1, nr2 in zip(list1, list2):
        summ += abs(nr1 - nr2)
    return summ

def b(inp):
    list1 = []
    list2 = []
    for line in inp:
        nr1 = int(line.split()[0])
        list1.append(nr1)
        nr2 = int(line.split()[1])
        list2.append(nr2)

    appearances = {}
    for nr1 in list1:
        if nr1 not in appearances:
            appearances[nr1] = 0
        for nr in list2:
            if nr == nr1:
                appearances[nr1] += 1

    summ = 0
    for nr, nr_of_appearances in appearances.items():
        summ += nr * nr_of_appearances
    return summ

def test_a():
    assert a(get_input()) == 1941353

def test_b():
    assert b(get_input()) == 22539317

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
