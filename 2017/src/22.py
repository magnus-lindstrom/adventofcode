import pathlib


def get_test_input():
    return '''..#
#..
...'''.split('\n')

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    n_iters = 10000
    infected = set()
    for i_row, line in enumerate(inp):
        for i_char, char in enumerate(line):
            if char == '#':
                infected.add((i_row, i_char))

    row = int(len(inp)/2)
    col = int(len(inp)/2)
    direction = 'up'

    new_infections = 0

    for _ in range(n_iters):
        if (row,col) in infected:
            infected.remove((row,col))
            if direction == 'up':
                direction = 'right'
                col += 1
            elif direction == 'right':
                direction = 'down'
                row += 1
            elif direction == 'down':
                direction = 'left'
                col -= 1
            else:
                direction = 'up'
                row -= 1
        else:
            infected.add((row,col))
            new_infections += 1
            if direction == 'up':
                direction = 'left'
                col -= 1
            elif direction == 'right':
                direction = 'up'
                row -= 1
            elif direction == 'down':
                direction = 'right'
                col += 1
            else:
                direction = 'down'
                row += 1

    return new_infections

def b():
    inp = get_input()
    n_iters = 10000000
    infected = set()
    weakened = set()
    flagged = set()
    for i_row, line in enumerate(inp):
        for i_char, char in enumerate(line):
            if char == '#':
                infected.add((i_row, i_char))

    row = int(len(inp)/2)
    col = int(len(inp)/2)
    direction = 'up'

    new_infections = 0

    for _ in range(n_iters):
        if (row,col) in infected:
            infected.remove((row,col))
            flagged.add((row,col))
            if direction == 'up':
                direction = 'right'
                col += 1
            elif direction == 'right':
                direction = 'down'
                row += 1
            elif direction == 'down':
                direction = 'left'
                col -= 1
            else:
                direction = 'up'
                row -= 1
        elif (row,col) in flagged:
            flagged.remove((row,col))
            if direction == 'up':
                direction = 'down'
                row += 1
            elif direction == 'right':
                direction = 'left'
                col -= 1
            elif direction == 'down':
                direction = 'up'
                row -= 1
            else:
                direction = 'right'
                col += 1
        elif (row,col) in weakened:
            infected.add((row,col))
            weakened.remove((row,col))
            new_infections += 1
            if direction == 'up':
                row -= 1
            elif direction == 'right':
                col += 1
            elif direction == 'down':
                row += 1
            else:
                col -= 1
        else:  # is a clean node
            weakened.add((row,col))
            if direction == 'up':
                direction = 'left'
                col -= 1
            elif direction == 'right':
                direction = 'up'
                row -= 1
            elif direction == 'down':
                direction = 'right'
                col += 1
            else:
                direction = 'down'
                row += 1

    return new_infections


def test_a():
    assert a() == 5182

def test_b():
    assert b() == 2512008

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
