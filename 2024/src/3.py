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
    #print(p.groups())
    return summ

def a(inp):
    summ = 0
    for line in inp:
        summ += get_mult_sum(line)
    return summ

def b(inp):
    summ = 0
    for line in inp:
        print()
        do_spans = []
        dont_spans = []
        for m in re.finditer(r"do\(\)", line):
            do_spans.append(m.span())
        print('dos:', do_spans)
        for m in re.finditer(r"don't\(\)", line):
            dont_spans.append(m.span())
        print('don\'ts:', dont_spans)
        print(f'line length: {len(line)}')

        i_do = 0
        # i_dont is the first character after the text "don't"
        if dont_spans:
            i_dont = dont_spans[0][1]
        else:
            i_dont = 10000000

        more_substrings_to_check = True
        while(more_substrings_to_check):
            more_substrings_to_check = False
            print(f'checking {i_do} - {i_dont}')

            if i_dont > len(line):
                extra = get_mult_sum(line[i_do:])
                summ += extra
                print('adding ', extra)
            else:
                extra = get_mult_sum(line[i_do:i_dont])
                summ += extra
                print('Adding ', extra)

            # update i_do
            for span in do_spans:
                if span[1] > i_dont:
                    i_do = span[1]
                    more_substrings_to_check = True
                    break

            # update i_dont
            for span in dont_spans:
                if span[1] > i_do:
                    i_dont = span[1]
                    break

            if i_dont < i_do:
                i_dont = 10000000

    return summ

def test_a():
    assert a(get_input()) == 0

def test_b():
    assert b(get_input()) == 0

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
