import argparse
from operator import itemgetter
import pathlib
from collections import defaultdict


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    sum = 0
    for line in inp:
        words = line[:-7].split('-')
        counts = []
        char_pos = {}
        for word in words[:-1]:
            for char in word:
                if char not in char_pos:
                    char_pos[char] = len(char_pos)
                    counts.append([char, 1])
                else:
                    counts[char_pos[char]][1] += 1

        counts.sort(key=itemgetter(0))
        counts.sort(key=itemgetter(1), reverse=True)
        real_checksum = ''.join([str(c[0]) for c in counts[:5]])

        checksum = line[-6:-1]
        if checksum == real_checksum:
            sum += int(words[-1])

    return sum

def b(inp):
    period = ord('z') - ord('a') + 1
    for line in inp:
        words = line[:-7].split('-')
        sentence = ''
        for word in words[:-1]:
            for char in word:
                x = ord(char) - ord('a')
                x = (x + int(words[-1])) % period
                x += ord('a')
                sentence += chr(x)
            sentence += ' '
        if sentence[:-1] == 'northpole object storage':
            return words[-1]

def test_a():
    assert a(get_input()) == 173787

def test_b():
    assert b(get_input()) == '548'

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
