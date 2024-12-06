import argparse
from copy import deepcopy
import sys
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

class Guard:
    def __init__(self, row, col, rowmax, colmax):
        self.row = row
        self.col = col
        self.dir = 'N'
        self.rowmax = rowmax
        self.colmax = colmax
        self.visited = {}
        self.going_in_circles = False

    def is_inside_area(self):
        if 0 <= self.row < self.rowmax:
            if 0 <= self.col < self.colmax:
                return True
        return False
    def record_position(self):
        if self.row not in self.visited:
            self.visited[self.row] = {}
        if self.col not in self.visited[self.row]:
            self.visited[self.row][self.col] = set()

        if self.dir in self.visited[self.row][self.col]:
            self.going_in_circles = True

        self.visited[self.row][self.col].add(self.dir)

    def take_step_or_turn(self, obstacles):
        if self.dir == 'N':
            if self.row - 1 in obstacles and self.col in obstacles[self.row - 1]:
                self.dir = 'E'
            else:
                self.row -= 1
        if self.dir == 'E':
            if self.row in obstacles and self.col + 1 in obstacles[self.row]:
                self.dir = 'S'
            else:
                self.col += 1
        if self.dir == 'S':
            if self.row + 1 in obstacles and self.col in obstacles[self.row + 1]:
                self.dir = 'W'
            else:
                self.row += 1
        if self.dir == 'W':
            if self.row in obstacles and self.col - 1 in obstacles[self.row]:
                self.dir = 'N'
            else:
                self.col -= 1
    def nr_of_visited_areas(self):
        summ = 0
        for cols in self.visited.values():
            summ += len(cols)
        return summ


def a(inp):
    obstacles = {}
    guard = None
    for i_row, line in enumerate(inp):
        for j_col, char in enumerate(line):
            if char == '#':
                if i_row not in obstacles:
                    obstacles[i_row] = {}
                obstacles[i_row][j_col] = True
            if char == '^':
                guard = Guard(i_row, j_col, rowmax=len(inp), colmax=len(inp[0]))
    if guard is None:
        sys.exit(1)

    while(guard.is_inside_area()):
        guard.record_position()
        guard.take_step_or_turn(obstacles)
    return guard.nr_of_visited_areas()


def b(inp):
    obstacles = {}
    start_row, start_col = None, None
    for i_row, line in enumerate(inp):
        for j_col, char in enumerate(line):
            if char == '#':
                if i_row not in obstacles:
                    obstacles[i_row] = {}
                obstacles[i_row][j_col] = True
            if char == '^':
                start_row = i_row
                start_col = j_col
    if start_row is None or start_col is None:
        sys.exit(1)

    summ = 0
    for i_row_obstruction in range(len(inp)):
        for j_col_obstruction in range(len(inp[0])):
            if i_row_obstruction in obstacles and j_col_obstruction in obstacles[i_row_obstruction]:
                continue
            if i_row_obstruction == start_row and j_col_obstruction == start_col:
                continue
            obstacle_clone = deepcopy(obstacles)

            if i_row_obstruction not in obstacle_clone:
                obstacle_clone[i_row_obstruction] = {}
            obstacle_clone[i_row_obstruction][j_col_obstruction] = True

            guard = Guard(start_row, start_col, rowmax=len(inp), colmax=len(inp[0]))
            while(guard.is_inside_area()):
                guard.record_position()
                guard.take_step_or_turn(obstacle_clone)
                if guard.going_in_circles:
                    summ += 1
                    break

    return summ

def test_a():
    assert a(get_input()) == 5318

def test_b():
    assert b(get_input()) == 1831

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
