import argparse
import pathlib
import re


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_mult_sum(line):
    summ = 0
    p = re.findall(r"mul\((\d+),(\d+)\)", line)
    for m in p:
        summ += (int(m[0]) * int(m[1]))
    return summ

def a(inp):
    summ = 0
    for line in inp:
        summ += get_mult_sum(line)
    return summ

def b(inp):
    summ = 0
    line = ''.join(inp)

    dos = []
    donts = []
    for m in re.finditer(r"do\(\)", line):
        dos.append(m.span()[1])
    for m in re.finditer(r"don't\(\)", line):
        donts.append(m.span()[1])

    # i_do is the first character after the text "do()"
    i_do = 0
    # i_dont is the first character after the text "don't()"
    i_dont = donts[0]

    more_substrings_to_check = True
    while(more_substrings_to_check):
        more_substrings_to_check = False

        extra = get_mult_sum(line[i_do:i_dont])
        summ += extra

        # update i_do
        for start in dos:
            if start > i_dont:
                i_do = start
                more_substrings_to_check = True
                break

        # update i_dont
        for start in donts:
            if start > i_do:
                i_dont = start
                break

        if i_dont < i_do:
            i_dont = len(line) - 1

    return summ

def test_a():
    assert a(get_input()) == 166630675

def test_b():
    assert b(get_input()) == 93465710

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
