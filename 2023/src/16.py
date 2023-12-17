import argparse
import pathlib
import sys

# forgive me father, for I must sin
sys.setrecursionlimit(10000)


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]


def energize_tiles(memo, tiles, energized, heading, row, col, max_row, max_col):
    if (heading, row, col) in memo:
        return energized, memo

    if not (0 <= row < max_row) or not (0 <= col < max_col):
        return energized, memo

    energized.add((row, col))
    memo.add((heading, row, col))

    if heading == 'right':
        if tiles[(row, col)] == '|':
            energized, memo = energize_tiles(memo, tiles, energized, 'up', row-1, col, max_row, max_col)
            energized, memo = energize_tiles(memo, tiles, energized, 'down', row+1, col, max_row, max_col)
        elif tiles[(row, col)] == '/':
            energized, memo = energize_tiles(memo, tiles, energized, 'up', row-1, col, max_row, max_col)
        elif tiles[(row, col)] == '\\':
            energized, memo = energize_tiles(memo, tiles, energized, 'down', row+1, col, max_row, max_col)
        else:
            energized, memo = energize_tiles(memo, tiles, energized, 'right', row, col+1, max_row, max_col)
    elif heading == 'left':
        if tiles[(row, col)] == '|':
            energized, memo = energize_tiles(memo, tiles, energized, 'up', row-1, col, max_row, max_col)
            energized, memo = energize_tiles(memo, tiles, energized, 'down', row+1, col, max_row, max_col)
        elif tiles[(row, col)] == '/':
            energized, memo = energize_tiles(memo, tiles, energized, 'down', row+1, col, max_row, max_col)
        elif tiles[(row, col)] == '\\':
            energized, memo = energize_tiles(memo, tiles, energized, 'up', row-1, col, max_row, max_col)
        else:
            energized, memo = energize_tiles(memo, tiles, energized, 'left', row, col-1, max_row, max_col)
    elif heading == 'up':
        if tiles[(row, col)] == '-':
            energized, memo = energize_tiles(memo, tiles, energized, 'right', row, col+1, max_row, max_col)
            energized, memo = energize_tiles(memo, tiles, energized, 'left', row, col-1, max_row, max_col)
        elif tiles[(row, col)] == '/':
            energized, memo = energize_tiles(memo, tiles, energized, 'right', row, col+1, max_row, max_col)
        elif tiles[(row, col)] == '\\':
            energized, memo = energize_tiles(memo, tiles, energized, 'left', row, col-1, max_row, max_col)
        else:
            energized, memo = energize_tiles(memo, tiles, energized, 'up', row-1, col, max_row, max_col)
    elif heading == 'down':
        if tiles[(row, col)] == '-':
            energized, memo = energize_tiles(memo, tiles, energized, 'right', row, col+1, max_row, max_col)
            energized, memo = energize_tiles(memo, tiles, energized, 'left', row, col-1, max_row, max_col)
        elif tiles[(row, col)] == '/':
            energized, memo = energize_tiles(memo, tiles, energized, 'left', row, col-1, max_row, max_col)
        elif tiles[(row, col)] == '\\':
            energized, memo = energize_tiles(memo, tiles, energized, 'right', row, col+1, max_row, max_col)
        else:
            energized, memo = energize_tiles(memo, tiles, energized, 'down', row+1, col, max_row, max_col)

    return energized, memo


def a(inp):

    tiles = {}
    for i_row, line in enumerate(inp):
        for i_col, char in enumerate(line):
            tiles[(i_row, i_col)] = char

    energized = set()
    memo = set()

    energized, memo = energize_tiles(memo, tiles, energized, 'right', 0, 0, len(inp), len(inp[0]))
    return len(energized)

def b(inp):

    tiles = {}
    for i_row, line in enumerate(inp):
        for i_col, char in enumerate(line):
            tiles[(i_row, i_col)] = char

    max_energized = 0

    for row in range(len(inp)):
        energized, _ = energize_tiles(set(), tiles, set(), 'right', row, 0, len(inp), len(inp[0]))
        if len(energized) > max_energized:
            max_energized = len(energized)
        energized, _ = energize_tiles(set(), tiles, set(), 'left', row, len(inp[0])-1, len(inp), len(inp[0]))
        if len(energized) > max_energized:
            max_energized = len(energized)
    for col in range(len(inp[0])):
        energized, _ = energize_tiles(set(), tiles, set(), 'down', 0, col, len(inp), len(inp[0]))
        if len(energized) > max_energized:
            max_energized = len(energized)
        energized, _ = energize_tiles(set(), tiles, set(), 'up', len(inp)-1, col, len(inp), len(inp[0]))
        if len(energized) > max_energized:
            max_energized = len(energized)
    return max_energized

def test_a():
    inp = get_input()
    assert a(inp) == 7477

def test_b():
    inp = get_input()
    assert b(inp) == 7853

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))
