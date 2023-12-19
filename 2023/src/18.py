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

def a(inp):

    # Using shoelace theorem
    vertices = []

    x, y = 0, 0
    area, circumference = 0, 0

    for line in inp:
        words = line.split()
        direction = words[0]
        length = int(words[1])
        circumference += length

        vertices.append((x, y))
        if direction == 'R':
            x += length
        elif direction == 'L':
            x -= length
        elif direction == 'U':
            y += length
        elif direction == 'D':
            y -= length

    for i_vert in range(len(vertices)):
        area += (vertices[i_vert][0] * vertices[(i_vert + 1) % len(vertices)][1]
                 - vertices[(i_vert + 1) % len(vertices)][0] * vertices[i_vert][1])

    area = abs(area) // 2
    area += circumference // 2 + 1  # modification to original formula

    return area

def b(inp):

    vertices = []
    dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    x, y = 0, 0
    area, circumference = 0, 0

    for line in inp:
        words = line.split()
        direction = dir_map[words[2][-2]]
        length = int(words[2][2:-2], 16)
        circumference += length

        vertices.append((x, y))
        if direction == 'R':
            x += length
        elif direction == 'L':
            x -= length
        elif direction == 'U':
            y += length
        elif direction == 'D':
            y -= length

    for i_vert in range(len(vertices)):
        area += (vertices[i_vert][0] * vertices[(i_vert + 1) % len(vertices)][1]
                 - vertices[(i_vert + 1) % len(vertices)][0] * vertices[i_vert][1])

    area = abs(area) // 2
    area += circumference // 2 + 1  # modification to original formula

    return area

def test_a():
    assert a(get_input()) == 68115

def test_b():
    assert b(get_input()) == 71262565063800

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))
