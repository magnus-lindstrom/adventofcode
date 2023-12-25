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
    possible = 0
    for line in inp:
        words = line.split()
        one, two, three = int(words[0]), int(words[1]), int(words[2])
        if one + two > three and one + three > two and two + three > one:
            possible += 1
    return possible

def b(inp):
    possible = 0
    for line in range(0, len(inp), 3):
        for col in range(3):
            one = int(inp[line].split()[col])
            two = int(inp[line + 1].split()[col])
            three = int(inp[line + 2].split()[col])
            if one + two > three and one + three > two and two + three > one:
                possible += 1
    return possible

def test_a():
    assert a(get_input()) == 983

def test_b():
    assert b(get_input()) == 1836

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
