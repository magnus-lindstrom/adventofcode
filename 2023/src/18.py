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
    x = 0
    y = 0
    minx, maxx, miny, maxy = 0, 0, 0, 0
    dug_tiles = {}
    if inp[0][0] in ['R', 'L']:
        dug_tiles[(x, y)] = 'horizontal'
    else:
        dug_tiles[(x, y)] = 'vertical'

    previous_vertical_went = ''
    for line in inp:
        words = line.split()
        direction = words[0]
        length = int(words[1])
        if direction == 'R':
            for _ in range(length):
                y += 1
                if y > maxy: maxy = y
                dug_tiles[(x, y)] = 'horizontal'
        elif direction == 'L':
            for _ in range(length):
                y -= 1
                if y < miny: miny = y
                dug_tiles[(x, y)] = 'horizontal'
        elif direction == 'U':
            if previous_vertical_went == 'down': dug_tiles[(x, y)] = 'vertical'
            previous_vertical_went = 'up'
            for _ in range(length):
                x -= 1
                if x < minx: minx = x
                dug_tiles[(x, y)] = 'vertical'
        elif direction == 'D':
            if previous_vertical_went == 'up': dug_tiles[(x, y)] = 'vertical'
            previous_vertical_went = 'down'
            for _ in range(length):
                x += 1
                if x > maxx: maxx = x
                dug_tiles[(x, y)] = 'vertical'

    sqm = 0
    for ix in range(minx, maxx+1):
        is_inside = False
        for iy in range(miny, maxy+1):
            if (ix, iy) in dug_tiles:
                if dug_tiles[(ix, iy)] == 'vertical' and is_inside:
                    is_inside = False
                elif dug_tiles[(ix, iy)] == 'vertical' and not is_inside:
                    is_inside = True
                sqm += 1
            elif is_inside:
                sqm += 1

    return sqm

def b(inp):
    # Chop up the area into squares and add them together

    x = 0
    y = 0
    horizontal_ranges = []
    vertical_ranges = []

    dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    for line in inp:
        words = line.split()
        direction = dir_map[words[2][-2]]
        length = int(words[2][2:-2], 16)
        if direction == 'R':
            rangee = {}
            rangee['length'] = length
            rangee['x'] = x
            horizontal_ranges.append(rangee)
            y += length
        elif direction == 'L':
            rangee = {}
            rangee['length'] = length
            rangee['x'] = x
            horizontal_ranges.append(rangee)
            y -= length
        elif direction == 'U':
            rangee = {}
            rangee['x_max'] = x
            rangee['x_min'] = x - length
            rangee['y'] = y
            vertical_ranges.append(rangee)
            x -= length
        elif direction == 'D':
            rangee = {}
            rangee['x_min'] = x
            rangee['x_max'] = x + length
            rangee['y'] = y
            vertical_ranges.append(rangee)
            x += length

    horizontal_ranges.sort(key=lambda e: e['x'])
    vertical_ranges.sort(key=lambda e: e['y'])

    sqm = 0
    previous_width = 0

    for i_hort in range(len(horizontal_ranges) - 1):
        vert_inds = []
        for i_vert, vert in enumerate(vertical_ranges):
            # just < and not <= because we don't want the tail end of previous vert to be included
            if vert['x_min'] <= horizontal_ranges[i_hort]['x'] < vert['x_max']:
                vert_inds.append(i_vert)

        width = 0
        for i_ind in range(0, len(vert_inds) - 1, 2):
            width += vertical_ranges[vert_inds[i_ind + 1]]['y'] - vertical_ranges[vert_inds[i_ind]]['y'] + 1

        # since we add parts of each intermediate layer twice
        sqm -= min([previous_width, width])
        previous_width = width

        height = horizontal_ranges[i_hort + 1]['x'] - horizontal_ranges[i_hort]['x'] + 1
        sqm += (width * height)

    return sqm

def b_shoelace(inp):
    # Alternative solution using Shoelace Formula (modified to include the
    # perimeter, which is not part of the original formula)

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
    print('b with shoelace formula:', b_shoelace(inp))
