import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def print_rocks(round_rocks, rectangular_rocks, min_row, max_row, min_col, max_col):
    for row in range(max_row, min_row-1, -1):
        for col in range(min_col, max_col+1):
            if (row, col) in round_rocks:
                print('O', end='')
            elif (row, col) in rectangular_rocks:
                print('#', end='')
            else:
                print('.', end='')
        print()

def a():
    inp = get_input()
    inp.reverse()

    min_col = 1
    max_col = len(inp[0])
    min_row = 1
    max_row = len(inp)

    rectangular_rocks = set()
    round_rocks = set()
    for i_row, row in enumerate(inp):
        for j_col, char in enumerate(row):
            if char == '#':
                rectangular_rocks.add((i_row+1, j_col+1))
            elif char == 'O':
                round_rocks.add((i_row+1, j_col+1))

    for col in range(min_col, max_col+1):
        row_to_roll_to = max_row
        for row in range(max_row, min_row-1, -1):
            if (row, col) in rectangular_rocks:
                row_to_roll_to = row - 1
            elif (row, col) in round_rocks:
                if row_to_roll_to > row:
                    round_rocks.add((row_to_roll_to, col))
                    round_rocks.remove((row, col))
                    row_to_roll_to -= 1
                else:
                    row_to_roll_to = row - 1

    load = 0
    for (row, _) in round_rocks:
        load += row

    return load

def roll_cycle(round_rocks, rectangular_rocks, min_row, max_row, min_col, max_col):
    # roll north
    for col in range(min_col, max_col+1):
        row_to_roll_to = max_row
        for row in range(max_row, min_row-1, -1):
            if (row, col) in rectangular_rocks:
                row_to_roll_to = row - 1
            elif (row, col) in round_rocks:
                if row_to_roll_to > row:
                    round_rocks.add((row_to_roll_to, col))
                    round_rocks.remove((row, col))
                    row_to_roll_to -= 1
                else:
                    row_to_roll_to = row - 1

    # roll west
    for row in range(min_row, max_row+1):
        col_to_roll_to = min_col
        for col in range(min_col, max_col+1):
            if (row, col) in rectangular_rocks:
                col_to_roll_to = col + 1
            elif (row, col) in round_rocks:
                if col_to_roll_to < col:
                    round_rocks.add((row, col_to_roll_to))
                    round_rocks.remove((row, col))
                    col_to_roll_to += 1
                else:
                    col_to_roll_to = col + 1

    # roll south
    for col in range(min_col, max_col+1):
        row_to_roll_to = min_row
        for row in range(min_row, max_row+1):
            if (row, col) in rectangular_rocks:
                row_to_roll_to = row + 1
            elif (row, col) in round_rocks:
                if row_to_roll_to < row:
                    round_rocks.add((row_to_roll_to, col))
                    round_rocks.remove((row, col))
                    row_to_roll_to += 1
                else:
                    row_to_roll_to = row + 1

    # roll east
    for row in range(min_row, max_row+1):
        col_to_roll_to = max_col
        for col in range(max_col, min_col-1, -1):
            if (row, col) in rectangular_rocks:
                col_to_roll_to = col - 1
            elif (row, col) in round_rocks:
                if col_to_roll_to > col:
                    round_rocks.add((row, col_to_roll_to))
                    round_rocks.remove((row, col))
                    col_to_roll_to -= 1
                else:
                    col_to_roll_to = col - 1

    return round_rocks

def tup_from_set(sett):
    return tuple([tup for tup in sett])

def b():
    inp = get_input()
    inp.reverse()
    iterations = 1000000000

    min_col = 1
    max_col = len(inp[0])
    min_row = 1
    max_row = len(inp)

    rectangular_rocks = set()
    round_rocks = set()
    for i_row, row in enumerate(inp):
        for j_col, char in enumerate(row):
            if char == '#':
                rectangular_rocks.add((i_row+1, j_col+1))
            elif char == 'O':
                round_rocks.add((i_row+1, j_col+1))

    rock_formation_to_iter = {}
    rock_formation_to_iter[tup_from_set(round_rocks)] = 0

    i = 1
    i_left = 0
    while i <= iterations:
        round_rocks = roll_cycle(round_rocks, rectangular_rocks, min_row, max_row, min_col, max_col)
        if tup_from_set(round_rocks) in rock_formation_to_iter.keys():
            offset = i - rock_formation_to_iter[tup_from_set(round_rocks)]
            i_left = (iterations - rock_formation_to_iter[tup_from_set(round_rocks)]) % offset
            break
        else:
            rock_formation_to_iter[tup_from_set(round_rocks)] = i
        i += 1

    i = 0
    while i < i_left:
        round_rocks = roll_cycle(round_rocks, rectangular_rocks, min_row, max_row, min_col, max_col)
        i += 1

    load = 0
    for (row, _) in round_rocks:
        load += row

    return load

def test_a():
    assert a() == 108857

def test_b():
    assert b() == 95273

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
