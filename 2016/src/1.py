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
        self.heading = 'north'
        self.row = 0
        self.col = 0
        self.visited = set()
        self.visited.add((0, 0))
        self.first_revisit = None

    def move(self, steps):
        for _ in range(steps):
            if self.heading == 'north':
                self.row -= 1
            elif self.heading == 'south':
                self.row += 1
            elif self.heading == 'east':
                self.col += 1
            elif self.heading == 'west':
                self.col -= 1
            if (self.row, self.col) in self.visited and self.first_revisit is None:
                self.first_revisit = (self.row, self.col)
            self.visited.add((self.row, self.col))

    def turn(self, direction):
        if direction == 'R':
            if self.heading == 'north':
                self.heading = 'east'
            elif self.heading == 'south':
                self.heading = 'west'
            elif self.heading == 'east':
                self.heading = 'south'
            elif self.heading == 'west':
                self.heading = 'north'
        elif direction == 'L':
            if self.heading == 'north':
                self.heading = 'west'
            elif self.heading == 'south':
                self.heading = 'east'
            elif self.heading == 'east':
                self.heading = 'north'
            elif self.heading == 'west':
                self.heading = 'south'

def a(inp):
    pos = Position()
    for chars in inp[0].split(', '):
        direction = chars[0]
        steps = int(chars[1:])
        pos.turn(direction)
        pos.move(steps)

    return abs(pos.row) + abs(pos.col)

def b(inp):
    pos = Position()
    for chars in inp[0].split(', '):
        direction = chars[0]
        steps = int(chars[1:])
        pos.turn(direction)
        pos.move(steps)

    return abs(pos.first_revisit[0]) + abs(pos.first_revisit[1])

def test_a():
    assert a(get_input()) == 250

def test_b():
    assert b(get_input()) == 151

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
