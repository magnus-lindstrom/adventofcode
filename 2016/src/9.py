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
    for line in inp:
        new_line = ''

        i_char = 0
        while i_char < len(line):
            if line[i_char] == '(':
                closing_bracket = line.find(')', i_char+1)
                nr_letters, reps = line[i_char+1:closing_bracket].split('x')
                i_char = closing_bracket + 1
                repeating_letters = line[i_char:i_char+int(nr_letters)]
                new_line += repeating_letters * int(reps)
                i_char += int(nr_letters)
            else:
                new_line += line[i_char]
                i_char += 1
        return len(new_line)

def decrease_multipliers(multipliers, decrease):
    for i_mult in range(len(multipliers) - 1, -1, -1):
        if multipliers[i_mult][1] <= decrease:
            multipliers.pop(i_mult)
        else:
            multipliers[i_mult][1] -= decrease

def get_factor_from_multipliers(multipliers):
    factor = 1
    for mult in multipliers:
        factor *= mult[0]
    return factor

def b(inp):
    # assume that no marker is split up through by partly repeated
    multipliers = []
    line = inp[0]
    new_line_length = 0

    i_char = 0
    while i_char < len(line):
        if line[i_char] == '(':
            closing_bracket = line.find(')', i_char+1)
            nr_letters, reps = line[i_char+1:closing_bracket].split('x')

            steps_forward = closing_bracket + 1 - i_char
            i_char += steps_forward
            mult_factor = get_factor_from_multipliers(multipliers)
            decrease_multipliers(multipliers, steps_forward)

            # start being valid after the marker
            multipliers.append([int(reps), int(nr_letters)])

        else:
            mult_factor = get_factor_from_multipliers(multipliers)
            new_line_length += mult_factor
            i_char += 1
            decrease_multipliers(multipliers, 1)
    return new_line_length

def test_a():
    assert a(get_input()) == 98135

def test_b():
    assert b(get_input()) == 10964557606

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
