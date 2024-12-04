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

def get_next_pos(i, j, dirr):
    if dirr == 'N':
        return i - 1, j
    elif dirr == 'NE':
        return i - 1, j + 1
    elif dirr == 'NW':
        return i - 1, j - 1
    elif dirr == 'S':
        return i + 1, j
    elif dirr == 'SE':
        return i + 1, j + 1
    elif dirr == 'SW':
        return i + 1, j - 1
    elif dirr == 'E':
        return i, j + 1
    elif dirr == 'W':
        return i, j - 1
    else:
        print('something wrong')
        print(dirr)
        return -100, -100

def words_start_here(n_words, grid, i_row, j_col, direction=None):

    current_char = grid[i_row][j_col]

    if current_char == 'X':
        for i_next, j_next, dirr in [
                (i_row - 1, j_col - 1, 'NW'),(i_row - 1, j_col, 'N'),(i_row - 1, j_col + 1, 'NE'),
                (i_row, j_col - 1, 'W'),(i_row, j_col + 1, 'E'),
                (i_row + 1, j_col - 1, 'SW'),(i_row + 1, j_col, 'S'),(i_row + 1, j_col + 1, 'SE')
        ]:
            if 0 <= i_next < len(grid) and 0 <= j_next < len(grid[0]):
                if grid[i_next][j_next] == 'M':
                    n_words += words_start_here(n_words, grid, i_next, j_next, direction=dirr)
        return n_words

    i_next, j_next = get_next_pos(i_row, j_col, direction)
    if not (0 <= i_next < len(grid) and 0 <= j_next < len(grid[0])):
        return 0

    if current_char == 'M' and grid[i_next][j_next] == 'A':
        return words_start_here(n_words, grid, i_next, j_next, direction=direction)

    if current_char == 'A' and grid[i_next][j_next] == 'S':
        return 1

    return 0

def a(inp):
    grid = []
    summ = 0
    for line in inp:
        grid.append([])
        for char in line:
            grid[-1].append(char)

    for i_row, line in enumerate(grid):
        for j_col, char in enumerate(line):
            if grid[i_row][j_col] == 'X':
                summ += words_start_here(0, grid, i_row, j_col)

    return summ

def word_starts_here(grid, i_row, j_col, direction, prev_char=None):

    # does a SAM or MAS start at the given position? (at the start of the recursion)
    # (bad name of the function, I know. It is supposed to reflect the action of the
    # function at every step of the recursion, yes, yes, I'm tired)

    current_char = grid[i_row][j_col]

    i_next, j_next = get_next_pos(i_row, j_col, direction)
    if not (0 <= i_next < len(grid) and 0 <= j_next < len(grid[0])):
        return False

    if prev_char == 'M':
        if current_char == 'A' and grid[i_next][j_next] == 'S':
            return True

    if prev_char == 'S':
        if current_char == 'A' and grid[i_next][j_next] == 'M':
            return True

    if prev_char is None:
        if current_char in ['M', 'S']:
            return word_starts_here(grid, i_next, j_next, direction, prev_char=current_char)

    return False

def b(inp):
    grid = []
    summ = 0
    for line in inp:
        grid.append([])
        for char in line:
            grid[-1].append(char)

    for i_row, line in enumerate(grid):
        for j_col, char in enumerate(line):
            if grid[i_row][j_col] in ['M', 'S']:
                if word_starts_here(grid, i_row, j_col, 'SE'):
                    if grid[i_row][j_col + 2] in ['M', 'S']:
                        if word_starts_here(grid, i_row, j_col + 2, 'SW'):
                            summ += 1

    return summ

def test_a():
    assert a(get_input()) == 2618

def test_b():
    assert b(get_input()) == 2011

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
