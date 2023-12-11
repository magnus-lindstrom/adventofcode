import itertools
import pathlib
from copy import deepcopy


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def expand_galaxy(inp):
    columns_to_expand = [i for i in range(len(inp[0]))]
    rows_to_expand = [i for i in range(len(inp))]
    galaxy_coords = []
    for i_line, line in enumerate(inp):
        for ichar, char in enumerate(line):
            if char == '#':
                galaxy_coords.append([i_line, ichar])
                if ichar in columns_to_expand:
                    columns_to_expand.remove(ichar)
                if i_line in rows_to_expand:
                    rows_to_expand.remove(i_line)

    rows_to_expand.reverse()
    columns_to_expand.reverse()
    for i_row in rows_to_expand:
        inp.insert(i_row, ['.']*len(inp[0]))

    for i_col in columns_to_expand:
        for i_row in range(len(inp)):
            inp[i_row].insert(i_col, '.')
    return inp

def expand_galaxy_2(galaxies, copy_mult):
    new_galaxies = deepcopy(galaxies)
    copy_mult -= 1

    min_row = min([e[0] for e in galaxies])
    min_col = min([e[1] for e in galaxies])
    max_row = max([e[0] for e in galaxies])
    max_col = max([e[1] for e in galaxies])

    rows_expanded = 0
    for row in range(min_row, max_row+1):
        is_galaxy = False
        for i_gal in range(len(galaxies)):
            if galaxies[i_gal][0] == row:
                is_galaxy = True
                new_galaxies[i_gal][0] = galaxies[i_gal][0] + rows_expanded
        if not is_galaxy:
            rows_expanded += copy_mult

    cols_expanded = 0
    for col in range(min_col, max_col+1):
        is_galaxy = False
        for i_gal in range(len(galaxies)):
            if galaxies[i_gal][1] == col:
                is_galaxy = True
                new_galaxies[i_gal][1] = galaxies[i_gal][1] + cols_expanded
        if not is_galaxy:
            cols_expanded += copy_mult

    return new_galaxies

def main(copy_mult):
    inp = get_input()
    inp_lists = []
    for i in range(len(inp)):
        inp_lists.append([])
        for j in range(len(inp[0])):
            inp_lists[i].append(inp[i][j])
    inp = inp_lists

    galaxies = []
    for i_row in range(len(inp)):
        for i_col, char in enumerate(inp[i_row]):
            if char == '#':
                galaxies.append([i_row, i_col])

    galaxies = expand_galaxy_2(galaxies, copy_mult)

    galaxy_pairs = itertools.combinations(galaxies, 2)
    dist = 0
    for pair in galaxy_pairs:
        dist += abs(pair[0][0] - pair[1][0])
        dist += abs(pair[0][1] - pair[1][1])

    return dist

def a():
    copy_mult = 2
    return main(copy_mult)

def b():
    copy_mult = 1000000
    return main(copy_mult)

def test_a():
    assert a() == 10494813

def test_b():
    assert b() == 840988812853

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
