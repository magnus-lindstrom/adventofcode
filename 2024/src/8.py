import argparse
from math import gcd
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
    antennas = {}
    for i_row, line in enumerate(inp):
        for j_col, char in enumerate(line):
            if char == '.': continue

            if char not in antennas:
                antennas[char] = []
            antennas[char].append((i_row, j_col))

    resonating_spots = set()
    for _, locations in antennas.items():
        for i_loc_a, loc_a in enumerate(locations):
            for loc_b in locations[i_loc_a + 1:]:
                row_diff = loc_a[0] - loc_b[0]
                col_diff = loc_a[1] - loc_b[1]
                res_spot_1 = (loc_a[0] + row_diff, loc_a[1] + col_diff)
                res_spot_2 = (loc_b[0] - row_diff, loc_b[1] - col_diff)
                if 0 <= res_spot_1[0] < len(inp) and 0 <= res_spot_1[1] < len(inp[0]):
                    resonating_spots.add(res_spot_1)
                if 0 <= res_spot_2[0] < len(inp) and 0 <= res_spot_2[1] < len(inp[0]):
                    resonating_spots.add(res_spot_2)
    return len(resonating_spots)

def b(inp):
    antennas = {}
    for i_row, line in enumerate(inp):
        for j_col, char in enumerate(line):
            if char == '.': continue

            if char not in antennas:
                antennas[char] = []
            antennas[char].append((i_row, j_col))

    resonating_spots = set()
    for _, locations in antennas.items():
        for i_loc_a, loc_a in enumerate(locations):
            for loc_b in locations[i_loc_a + 1:]:
                row_diff = loc_a[0] - loc_b[0]
                col_diff = loc_a[1] - loc_b[1]
                div = gcd(abs(row_diff), abs(col_diff))
                for i in range(1000):
                    i_row = loc_a[0] + i * (row_diff//div)
                    j_col = loc_a[1] + i * (col_diff//div)
                    if not 0 <= i_row < len(inp) or not 0 <= j_col < len(inp[0]):
                        break
                    resonating_spots.add((i_row, j_col))
                for i in range(1, 1000):
                    i_row = loc_a[0] - i * (row_diff//div)
                    j_col = loc_a[1] - i * (col_diff//div)
                    if not 0 <= i_row < len(inp) or not 0 <= j_col < len(inp[0]):
                        break
                    resonating_spots.add((i_row, j_col))

    return len(resonating_spots)

def test_a():
    assert a(get_input()) == 376

def test_b():
    assert b(get_input()) == 1352

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
