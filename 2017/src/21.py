import pathlib


def get_test_input():
    file_name = pathlib.Path('inputs/21_test')
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def flatten_3d_pattern(pattern):
    row = '/'.join(pattern)
    return row

def make_pattern_3d(pattern):
    rows = pattern.split('/')
    return rows

def get_pattern_variations(pattern: str):
    p3 = make_pattern_3d(pattern)
    variations = []

    if len(p3) == 2:
        a = p3[0][0]
        b = p3[0][1]
        c = p3[1][0]
        d = p3[1][1]
        # n * 90deg rotation (n = 0,1,2,3)
        variations.append([a + b, c + d])
        variations.append([c + a, d + b])
        variations.append([d + c, b + a])
        variations.append([b + d, a + c])

        # flip + n * 90deg rotation (n = 0,1,2,3)
        variations.append([b + a, d + c])
        variations.append([d + b, c + a])
        variations.append([c + d, a + b])
        variations.append([a + c, b + d])

    elif len(p3) == 3:
        a = p3[0][0]
        b = p3[0][1]
        c = p3[0][2]
        d = p3[1][0]
        e = p3[1][1]
        f = p3[1][2]
        g = p3[2][0]
        h = p3[2][1]
        i = p3[2][2]

        # n * 90deg rotation (n = 0,1,2,3)
        variations.append([a+b+c, d+e+f, g+h+i])
        variations.append([g+d+a, h+e+b, i+f+c])
        variations.append([i+h+g, f+e+d, c+b+a])
        variations.append([c+f+i, b+e+h, a+d+g])

        # flip + n * 90deg rotation (n = 0,1,2,3)
        variations.append([c+b+a, f+e+d, i+h+g])
        variations.append([i+f+c, h+e+b, g+d+a])
        variations.append([g+h+i, d+e+f, a+b+c])
        variations.append([a+d+g, b+e+h, c+f+i])

    return [flatten_3d_pattern(e) for e in variations]

def pp(pattern: str):
    # Pretty print

    p = make_pattern_3d(pattern)
    for row in p:
        print(row)
    print()

def expand_image(image, rules):
    image_3d = make_pattern_3d(image)

    new_image_3d = None

    if len(image_3d) % 2 == 0:
        new_image_3d = [''] * int(len(image_3d) * 3 / 2)
        for i_row in range(0, len(image_3d), 2):
            for j_col in range(0, len(image_3d), 2):
                two_by_two_image_3d = [
                    image_3d[i_row][j_col:j_col+2],
                    image_3d[i_row+1][j_col:j_col+2]
                ]
                two_by_two_image = flatten_3d_pattern(two_by_two_image_3d)
                three_by_three_image = rules[two_by_two_image]
                three_by_three_image_3d = make_pattern_3d(three_by_three_image)
                new_image_3d[int(i_row*3/2)+0] += three_by_three_image_3d[0]
                new_image_3d[int(i_row*3/2)+1] += three_by_three_image_3d[1]
                new_image_3d[int(i_row*3/2)+2] += three_by_three_image_3d[2]
    elif len(image_3d) % 3 == 0:
        new_image_3d = [''] * int(len(image_3d) * 4 / 3)
        for i_row in range(0, len(image_3d), 3):
            for j_col in range(0, len(image_3d), 3):
                three_by_three_image_3d = [
                    image_3d[i_row][j_col:j_col+3],
                    image_3d[i_row+1][j_col:j_col+3],
                    image_3d[i_row+2][j_col:j_col+3]
                ]
                three_by_three_image = flatten_3d_pattern(three_by_three_image_3d)
                four_by_four_image = rules[three_by_three_image]
                four_by_four_image_3d = make_pattern_3d(four_by_four_image)
                new_image_3d[int(i_row*4/3)+0] += four_by_four_image_3d[0]
                new_image_3d[int(i_row*4/3)+1] += four_by_four_image_3d[1]
                new_image_3d[int(i_row*4/3)+2] += four_by_four_image_3d[2]
                new_image_3d[int(i_row*4/3)+3] += four_by_four_image_3d[3]

    return flatten_3d_pattern(new_image_3d)

def a():
    image = '.#./..#/###'

    inp = get_input()
    n_iters = 5

    rules = {}
    for line in inp:
        lhs, _, rhs = line.split()
        variations = get_pattern_variations(lhs)
        for v in variations:
            rules[v] = rhs
        rules[lhs] = rhs


    for _ in range(n_iters):
        image = expand_image(image, rules)

    return sum([1 for char in image if char == '#'])

def b():
    image = '.#./..#/###'

    inp = get_input()
    n_iters = 18


    rules = {}
    for line in inp:
        lhs, _, rhs = line.split()
        variations = get_pattern_variations(lhs)
        for v in variations:
            rules[v] = rhs
        rules[lhs] = rhs


    for _ in range(n_iters):
        image = expand_image(image, rules)

    return sum([1 for char in image if char == '#'])

def test_a():
    assert a() == 110

def test_b():
    assert b() == 1277716

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
