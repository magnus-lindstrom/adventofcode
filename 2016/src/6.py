import argparse
import pathlib
from operator import itemgetter


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    repetitions = {}
    for line in inp:
        for i_char, char in enumerate(line):
            if i_char not in repetitions:
                repetitions[i_char] = {char: 1}
            elif char not in repetitions[i_char]:
                repetitions[i_char][char] = 1
            else:
                repetitions[i_char][char] += 1
    password = ''
    for key in repetitions.keys():
        x = [[char, reps] for char, reps in repetitions[key].items()]
        x.sort(key=itemgetter(1), reverse=True)
        password += x[0][0]

    return password

def b(inp):
    repetitions = {}
    for line in inp:
        for i_char, char in enumerate(line):
            if i_char not in repetitions:
                repetitions[i_char] = {char: 1}
            elif char not in repetitions[i_char]:
                repetitions[i_char][char] = 1
            else:
                repetitions[i_char][char] += 1
    password = ''
    for key in repetitions.keys():
        x = [[char, reps] for char, reps in repetitions[key].items()]
        x.sort(key=itemgetter(1))
        password += x[0][0]

    return password

def test_a():
    assert a(get_input()) == 'qoclwvah'

def test_b():
    assert b(get_input()) == 'ryrgviuv'

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
