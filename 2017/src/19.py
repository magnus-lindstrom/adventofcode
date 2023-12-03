import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line for line in f.readlines()]

def a():
    mat = get_input()
    i_row = 0
    j_col = 0
    seen_letters = []
    heading = 'down'
    for j, char in enumerate(mat[0]):
        if char == '|':
            j_col = j

    while True:
        if heading == 'down':
            if mat[i_row][j_col] in ['|', '-']:
                i_row += 1
            elif mat[i_row][j_col] == '+':
                if j_col + 1 < len(mat[i_row]) and mat[i_row][j_col + 1] != ' ':
                    j_col += 1
                    heading = 'right'
                elif j_col - 1 >= 0 and mat[i_row][j_col - 1] != ' ':
                    j_col -= 1
                    heading = 'left'
            elif mat[i_row][j_col] == ' ':
                return ''.join(seen_letters)
            else:
                seen_letters.append(mat[i_row][j_col])
                i_row += 1

        elif heading == 'right':
            if mat[i_row][j_col] in ['|', '-']:
                j_col += 1
            elif mat[i_row][j_col] == '+':
                if i_row - 1 >= 0 and mat[i_row - 1][j_col] != ' ':
                    i_row -= 1
                    heading = 'up'
                elif i_row + 1 < len(mat) and mat[i_row + 1][j_col] != ' ':
                    i_row += 1
                    heading = 'down'
            elif mat[i_row][j_col] == ' ':
                return ''.join(seen_letters)
            else:
                seen_letters.append(mat[i_row][j_col])
                j_col += 1

        elif heading == 'up':
            if mat[i_row][j_col] in ['|', '-']:
                i_row -= 1
            elif mat[i_row][j_col] == '+':
                if j_col + 1 < len(mat[i_row]) and mat[i_row][j_col + 1] != ' ':
                    j_col += 1
                    heading = 'right'
                elif j_col - 1 >= 0 and mat[i_row][j_col - 1] != ' ':
                    j_col -= 1
                    heading = 'left'
            elif mat[i_row][j_col] == ' ':
                return ''.join(seen_letters)
            else:
                seen_letters.append(mat[i_row][j_col])
                i_row -= 1

        elif heading == 'left':
            if mat[i_row][j_col] in ['|', '-']:
                j_col -= 1
            elif mat[i_row][j_col] == '+':
                if i_row - 1 >= 0 and mat[i_row - 1][j_col] != ' ':
                    i_row -= 1
                    heading = 'up'
                elif i_row + 1 < len(mat) and mat[i_row + 1][j_col] != ' ':
                    i_row += 1
                    heading = 'down'
            elif mat[i_row][j_col] == ' ':
                return ''.join(seen_letters)
            else:
                seen_letters.append(mat[i_row][j_col])
                j_col -= 1

def b():
    mat = get_input()
    i_row = 0
    j_col = 0
    heading = 'down'
    for j, char in enumerate(mat[0]):
        if char == '|':
            j_col = j
    steps = 0

    while True:
        steps += 1
        if heading == 'down':
            if mat[i_row][j_col] in ['|', '-']:
                i_row += 1
            elif mat[i_row][j_col] == '+':
                if j_col + 1 < len(mat[i_row]) and mat[i_row][j_col + 1] != ' ':
                    j_col += 1
                    heading = 'right'
                elif j_col - 1 >= 0 and mat[i_row][j_col - 1] != ' ':
                    j_col -= 1
                    heading = 'left'
            elif mat[i_row][j_col] == ' ':
                return steps - 1  # last char is a ' ' and doesn't count
            else:
                i_row += 1

        elif heading == 'right':
            if mat[i_row][j_col] in ['|', '-']:
                j_col += 1
            elif mat[i_row][j_col] == '+':
                if i_row - 1 >= 0 and mat[i_row - 1][j_col] != ' ':
                    i_row -= 1
                    heading = 'up'
                elif i_row + 1 < len(mat) and mat[i_row + 1][j_col] != ' ':
                    i_row += 1
                    heading = 'down'
            elif mat[i_row][j_col] == ' ':
                return steps - 1  # last char is a ' ' and doesn't count
            else:
                j_col += 1

        elif heading == 'up':
            if mat[i_row][j_col] in ['|', '-']:
                i_row -= 1
            elif mat[i_row][j_col] == '+':
                if j_col + 1 < len(mat[i_row]) and mat[i_row][j_col + 1] != ' ':
                    j_col += 1
                    heading = 'right'
                elif j_col - 1 >= 0 and mat[i_row][j_col - 1] != ' ':
                    j_col -= 1
                    heading = 'left'
            elif mat[i_row][j_col] == ' ':
                return steps - 1  # last char is a ' ' and doesn't count
            else:
                i_row -= 1

        elif heading == 'left':
            if mat[i_row][j_col] in ['|', '-']:
                j_col -= 1
            elif mat[i_row][j_col] == '+':
                if i_row - 1 >= 0 and mat[i_row - 1][j_col] != ' ':
                    i_row -= 1
                    heading = 'up'
                elif i_row + 1 < len(mat) and mat[i_row + 1][j_col] != ' ':
                    i_row += 1
                    heading = 'down'
            elif mat[i_row][j_col] == ' ':
                return steps - 1  # last char is a ' ' and doesn't count
            else:
                j_col -= 1

def test_a():
    assert a() == 'GINOWKYXH'

def test_b():
    assert b() == 16636

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
