import math
import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    turns = inp[0]
    pos = 'AAA'
    intersections = {}
    for line in inp[2:]:
        words = line.split()
        l = words[2].removeprefix('(').removesuffix(',')
        r = words[3].removesuffix(')')
        intersections[words[0]] = (l, r)
    i_turn = 0
    steps = 0
    while pos != 'ZZZ':

        if turns[i_turn] == 'L':
            pos = intersections[pos][0]
        else:
            pos = intersections[pos][1]

        i_turn = (i_turn + 1) % len(turns)
        steps += 1

    return steps

def b():
    inp = get_input()
    turns = inp[0]
    starting_positions = []
    intersections = {}
    for line in inp[2:]:
        words = line.split()
        l = words[2].removeprefix('(').removesuffix(',')
        r = words[3].removesuffix(')')
        intersections[words[0]] = (l, r)

        if words[0][-1] == 'A':
            starting_positions.append(words[0])

    steps_taken = []
    for pos in starting_positions:
        i_turn = 0
        steps = 0
        while pos[-1] != 'Z':

            if turns[i_turn] == 'L':
                pos = intersections[pos][0]
            else:
                pos = intersections[pos][1]

            i_turn = (i_turn + 1) % len(turns)
            steps += 1
        steps_taken.append(steps)

    return math.lcm(*steps_taken)

def test_a():
    assert a() == 16043

def test_b():
    assert b() == 15726453850399

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
