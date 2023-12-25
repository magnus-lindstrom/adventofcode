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

class Position:
    def __init__(self):
        self.keys = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.indices = [1, 1]

    def move(self, char):
        if char == 'U':
            self.indices[0] = max(0, self.indices[0] - 1)
        elif char == 'D':
            self.indices[0] = min(2, self.indices[0] + 1)
        elif char == 'R':
            self.indices[1] = min(2, self.indices[1] + 1)
        elif char == 'L':
            self.indices[1] = max(0, self.indices[1] - 1)

    def get_key(self):
        return str(self.keys[self.indices[0]][self.indices[1]])

class PositionB:
    def __init__(self):
        self.keys = [[0, 0, 1, 0, 0], [0, 2, 3, 4, 0], [5, 6, 7, 8, 9],
                     [0, 'A', 'B', 'C', 0], [0, 0, 'D', 0, 0]]
        self.indices = [2, 0]

    def move(self, char):
        if char == 'U':
            if self.indices in [[0, 2], [1, 1], [1, 3], [2, 0], [2, 4]]:
                pass
            else:
                self.indices[0] -= 1
        elif char == 'D':
            if self.indices in [[4, 2], [3, 1], [3, 3], [2, 0], [2, 4]]:
                pass
            else:
                self.indices[0] += 1
        elif char == 'R':
            if self.indices in [[0, 2], [1, 3], [2, 4], [3, 3], [4, 2]]:
                pass
            else:
                self.indices[1] += 1
        elif char == 'L':
            if self.indices in [[0, 2], [1, 1], [2, 0], [3, 1], [4, 2]]:
                pass
            else:
                self.indices[1] -= 1

    def get_key(self):
        return str(self.keys[self.indices[0]][self.indices[1]])

def a(inp):
    pos = Position()
    number = ''
    for line in inp:
        for char in line:
            pos.move(char)

        number += pos.get_key()
    return number

def b(inp):
    pos = PositionB()
    number = ''
    for line in inp:
        for char in line:
            pos.move(char)
            print(char, pos.indices)

        number += pos.get_key()
    return number

def test_a():
    assert a(get_input()) == '14894'

def test_b():
    assert b(get_input()) == '26B96'

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
