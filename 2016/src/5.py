import argparse
from hashlib import md5
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
    word = inp[0]
    i = 0
    password = ''
    while True:
        out = md5((word + str(i)).encode())
        if out.hexdigest()[:5] == '00000':
            password += out.hexdigest()[5]
            if len(password) == 8:
                return password
        i += 1

    return 0

def b(inp):
    word = inp[0]
    i = 0
    password = [' '] * 8
    while True:
        out = md5((word + str(i)).encode())
        if out.hexdigest()[:5] == '00000':
            position = out.hexdigest()[5]
            if position in '01234567':
                letter = out.hexdigest()[6]
                if password[int(position)] == ' ':
                    password[int(position)] = letter
                    if ' ' not in password:
                        return ''.join(password)
        i += 1

    return 0

def test_a():
    assert a(get_input()) == '801b56a7'

def test_b():
    assert b(get_input()) == '424a0197'

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
