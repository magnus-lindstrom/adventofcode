import argparse
import pathlib
from copy import deepcopy


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def is_safe(numbers):
    prev = numbers[0]
    increasing = False
    decreasing = False
    for i_num, num in enumerate(numbers[1:]):
        if num > prev:
            if decreasing:
                break
            increasing = True
            if not 1 <= num - prev <= 3:
                break
        elif num < prev:
            if increasing:
                break
            decreasing = True
            if prev - num > 3:
                break
        else:
            break

        if i_num == len(numbers) - 2:
            return True

        prev = num
    return False

def a(inp):
    summ = 0
    for line in inp:
        numbers = [int(n) for n in line.split()]
        if is_safe(numbers):
            summ += 1


    return summ

def b(inp):
    summ = 0
    for line in inp:
        numbers = [int(n) for n in line.split()]
        if is_safe(numbers):
            summ += 1
        else:
            for pop_i, _ in enumerate(numbers):
                new_numbers = deepcopy(numbers)
                del new_numbers[pop_i]
                if is_safe(new_numbers):
                    summ += 1
                    break

    return summ

def test_a():
    assert a(get_input()) == 213

def test_b():
    assert b(get_input()) == 285

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
