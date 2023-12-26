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

class Display:
    def __init__(self):
        self.pixels = []
        for _ in range(6):
            self.pixels.append([0] * 50)
    def turn_on(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                self.pixels[row][col] = 1

    def rotate_row(self, row_nr, steps):
        original_row = self.pixels[row_nr].copy()
        for ind, value in enumerate(original_row):
            new_ind = (ind + steps) % 50
            self.pixels[row_nr][new_ind] = value

    def rotate_col(self, col_nr, steps):
        original_col = [row[col_nr] for row in self.pixels]
        for ind, value in enumerate(original_col):
            new_ind = (ind + steps) % 6
            self.pixels[new_ind][col_nr] = value

    def nr_lit_pixels(self):
        return sum([sum(self.pixels[i]) for i in range(6)])

    def __str__(self):
        string = ''
        for row in self.pixels:
            for nr in row:
                if nr == 1:
                    string += '#'
                else:
                    string += ' '
            string += '\n'
        return string


def a(inp):
    display = Display()
    for line in inp:
        words = line.split()
        if words[0] == 'rect':
            cols, rows = words[1].split('x')
            display.turn_on(int(rows), int(cols))
        elif words[0] == 'rotate':
            nr = int(words[2].split('=')[1])
            amount = int(words[4])
            if words[1] == 'row':
                display.rotate_row(nr, amount)
            elif words[1] == 'column':
                display.rotate_col(nr, amount)

    return display.nr_lit_pixels()

def b(inp):
    display = Display()
    for line in inp:
        words = line.split()
        if words[0] == 'rect':
            cols, rows = words[1].split('x')
            display.turn_on(int(rows), int(cols))
        elif words[0] == 'rotate':
            nr = int(words[2].split('=')[1])
            amount = int(words[4])
            if words[1] == 'row':
                display.rotate_row(nr, amount)
            elif words[1] == 'column':
                display.rotate_col(nr, amount)

    return display.__str__()

def test_a():
    assert a(get_input()) == 110

def test_b():
    assert b(get_input()) == '####   ## #  # ###  #  #  ##  ###  #    #   #  ## \n   #    # #  # #  # # #  #  # #  # #    #   #   # \n  #     # #### #  # ##   #    #  # #     # #    # \n #      # #  # ###  # #  #    ###  #      #     # \n#    #  # #  # # #  # #  #  # #    #      #  #  # \n####  ##  #  # #  # #  #  ##  #    ####   #   ##  \n'

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
