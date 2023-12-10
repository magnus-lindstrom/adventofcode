import pathlib


def get_input():
    file_name = pathlib.Path('inputs/10')
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

class Position:
    def __init__(self, mapp):
        self.map = mapp
        self.direction = None
        self.is_done = False
        self.have_been = set()
        for i_line, line in enumerate(self.map):
            for i_char, char in enumerate(line):
                if char == 'S':
                    self.row = i_line
                    self.col = i_char
                    self.s_row = i_line
                    self.s_col = i_char
        self.define_s()

    def add_outside_point(self, outside_tiles, outside_side):
            if outside_side == 'west':
                if (self.row, self.col-1) not in self.have_been:
                    if 0 <= self.row < len(self.map) and 0 <= self.col-1 < len(self.map[0]):
                        outside_tiles.add((self.row, self.col-1))
            elif outside_side == 'east':
                if (self.row, self.col+1) not in self.have_been:
                    if 0 <= self.row < len(self.map) and 0 <= self.col+1 < len(self.map[0]):
                        outside_tiles.add((self.row, self.col+1))
            elif outside_side == 'north':
                if (self.row-1, self.col) not in self.have_been:
                    if 0 <= self.row-1 < len(self.map) and 0 <= self.col < len(self.map[0]):
                        outside_tiles.add((self.row-1, self.col))
            elif outside_side == 'south':
                if (self.row+1, self.col) not in self.have_been:
                    if 0 <= self.row+1 < len(self.map) and 0 <= self.col < len(self.map[0]):
                        outside_tiles.add((self.row+1, self.col))

            return outside_tiles

    def mark_outside(self, start_point, start_dir, outside_side):
        self.row = start_point[0]
        self.col = start_point[1]
        self.direction = start_dir
        outside_tiles = set()

        while True:
            outside_tiles = self.add_outside_point(outside_tiles, outside_side)

            if self.direction == 'north':
                self.row -= 1
                outside_tiles = self.add_outside_point(outside_tiles, outside_side)
                if self.map[self.row][self.col] == '|':
                    pass
                elif self.map[self.row][self.col] == '7':
                    self.direction = 'west'
                    if outside_side == 'west':
                        outside_side = 'south'
                    elif outside_side == 'east':
                        outside_side = 'north'
                elif self.map[self.row][self.col] == 'F':
                    self.direction = 'east'
                    if outside_side == 'west':
                        outside_side = 'north'
                    elif outside_side == 'east':
                        outside_side = 'south'
            elif self.direction == 'south':
                self.row += 1
                outside_tiles = self.add_outside_point(outside_tiles, outside_side)
                if self.map[self.row][self.col] == '|':
                    pass
                elif self.map[self.row][self.col] == 'J':
                    self.direction = 'west'
                    if outside_side == 'west':
                        outside_side = 'north'
                    elif outside_side == 'east':
                        outside_side = 'south'
                elif self.map[self.row][self.col] == 'L':
                    self.direction = 'east'
                    if outside_side == 'west':
                        outside_side = 'south'
                    elif outside_side == 'east':
                        outside_side = 'north'
            elif self.direction == 'east':
                self.col += 1
                outside_tiles = self.add_outside_point(outside_tiles, outside_side)
                if self.map[self.row][self.col] == '-':
                    pass
                elif self.map[self.row][self.col] == 'J':
                    self.direction = 'north'
                    if outside_side == 'north':
                        outside_side = 'west'
                    elif outside_side == 'south':
                        outside_side = 'east'
                elif self.map[self.row][self.col] == '7':
                    self.direction = 'south'
                    if outside_side == 'north':
                        outside_side = 'east'
                    elif outside_side == 'south':
                        outside_side = 'west'
            elif self.direction == 'west':
                self.col -= 1
                outside_tiles = self.add_outside_point(outside_tiles, outside_side)
                if self.map[self.row][self.col] == '-':
                    pass
                elif self.map[self.row][self.col] == 'L':
                    self.direction = 'north'
                    if outside_side == 'north':
                        outside_side = 'east'
                    elif outside_side == 'south':
                        outside_side = 'west'
                elif self.map[self.row][self.col] == 'F':
                    self.direction = 'south'
                    if outside_side == 'north':
                        outside_side = 'west'
                    elif outside_side == 'south':
                        outside_side = 'east'

            if (self.row, self.col) == start_point:
                break
        return outside_tiles


    def define_s(self):
        if (self.map[self.row-1][self.col] in ['|', 'F', '7']
                and self.map[self.row+1][self.col] in ['|', 'J', 'L']):
            self.s_should_be = '|'
        elif (self.map[self.row-1][self.col] in ['|', 'F', '7']
              and self.map[self.row][self.col+1] in ['-', 'J', '7']):
            self.s_should_be = 'L'
        elif (self.map[self.row-1][self.col] in ['|', 'F', '7']
              and self.map[self.row][self.col-1] in ['-', 'F', 'L']):
            self.s_should_be = 'J'
        elif (self.map[self.row][self.col+1] in ['-', 'J', '7']
              and self.map[self.row+1][self.col] in ['|', 'J', 'L']):
            self.s_should_be = 'F'
        elif (self.map[self.row][self.col-1] in ['-', 'F', 'L']
              and self.map[self.row+1][self.col] in ['|', 'J', 'L']):
            self.s_should_be = '7'
        elif (self.map[self.row][self.col-1] in ['-', 'F', 'L']
              and self.map[self.row][self.col+1] in ['-', 'J', '7']):
            self.s_should_be = '-'

    def replace_s(self):
        self.map[self.s_row] = self.map[self.s_row].replace('S', self.s_should_be)

    def take_step(self):
        if self.direction is None:
            if self.row + 1 < len(self.map) and self.map[self.row + 1][self.col] == '|':
                self.direction = 'south'
                self.row += 1
            elif self.row + 1 < len(self.map) and self.map[self.row + 1][self.col] == 'L':
                self.direction = 'east'
                self.row += 1
            elif self.row + 1 < len(self.map) and self.map[self.row + 1][self.col] == 'J':
                self.direction = 'west'
                self.row += 1
            elif self.row - 1 >= 0 and self.map[self.row - 1][self.col] == '|':
                self.direction = 'north'
                self.row -= 1
            elif self.row - 1 >= 0 and self.map[self.row - 1][self.col] == '7':
                self.direction = 'west'
                self.row -= 1
            elif self.row - 1 >= 0 and self.map[self.row - 1][self.col] == 'F':
                self.direction = 'east'
                self.row -= 1
            elif self.col + 1 < len(self.map[0]) and self.map[self.row][self.col + 1] == '-':
                self.direction = 'east'
                self.col += 1
            elif self.col + 1 < len(self.map[0]) and self.map[self.row][self.col + 1] == 'J':
                self.direction = 'north'
                self.col += 1
            elif self.col + 1 < len(self.map[0]) and self.map[self.row][self.col + 1] == '7':
                self.direction = 'south'
                self.col += 1
            elif self.col - 1 >= 0 and self.map[self.row][self.col - 1] == '-':
                self.direction = 'west'
                self.col -= 1
            elif self.col - 1 >= 0 and self.map[self.row][self.col - 1] == 'L':
                self.direction = 'north'
                self.col -= 1
            elif self.col - 1 >= 0 and self.map[self.row][self.col - 1] == 'F':
                self.direction = 'south'
                self.col -= 1

        else:
            if self.direction == 'north':
                if self.map[self.row - 1][self.col] == '|':
                    pass
                elif self.map[self.row - 1][self.col] == '7':
                    self.direction = 'west'
                elif self.map[self.row - 1][self.col] == 'F':
                    self.direction = 'east'
                elif self.map[self.row - 1][self.col] == 'S':
                    self.is_done = True
                self.row -= 1
            elif self.direction == 'south':
                if self.map[self.row + 1][self.col] == '|':
                    pass
                elif self.map[self.row + 1][self.col] == 'J':
                    self.direction = 'west'
                elif self.map[self.row + 1][self.col] == 'L':
                    self.direction = 'east'
                elif self.map[self.row + 1][self.col] == 'S':
                    self.is_done = True
                self.row += 1
            elif self.direction == 'east':
                if self.map[self.row][self.col + 1] == '-':
                    pass
                elif self.map[self.row][self.col + 1] == 'J':
                    self.direction = 'north'
                elif self.map[self.row][self.col + 1] == '7':
                    self.direction = 'south'
                elif self.map[self.row][self.col + 1] == 'S':
                    self.is_done = True
                self.col += 1
            elif self.direction == 'west':
                if self.map[self.row][self.col - 1] == '-':
                    pass
                elif self.map[self.row][self.col - 1] == 'L':
                    self.direction = 'north'
                elif self.map[self.row][self.col - 1] == 'F':
                    self.direction = 'south'
                elif self.map[self.row][self.col - 1] == 'S':
                    self.is_done = True
                self.col -= 1
        self.have_been.add((self.row, self.col))

def a():
    inp = get_input()
    position = Position(inp)

    n_steps = 0
    while not position.is_done:
        position.take_step()
        n_steps += 1
    return int(n_steps / 2)

def find_outside_points(tile, main_loop, accounted_for, sizes):
    row = tile[0]
    col = tile[1]
    new_tiles = set()
    for new_tile in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
        if (new_tile not in accounted_for and new_tile not in main_loop
                and 0 <= new_tile[0] < sizes[0]
                and 0 <= new_tile[1] < sizes[1]):
            new_tiles.add(new_tile)
    return new_tiles

def b():
    inp = get_input()

    position = Position(inp)

    while not position.is_done:
        position.take_step()

    main_loop = position.have_been
    position.replace_s()

    # find start point of the loop to run through
    found_start = False
    outside_side = 'west'
    start_point = None
    start_dir = None
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if (i, j) in main_loop:
                start_point = (i, j)
                if inp[i][j] == '|':
                    start_dir = 'north'
                elif inp[i][j] == 'F':
                    start_dir = 'south'
                elif inp[i][j] == 'L':
                    start_dir = 'north'
                found_start = True
                break
        if found_start:
            break

    # find all tiles that are on the outside-side of the loop, use them as
    # starting point for a flood-fill later on
    outside_tiles = position.mark_outside(start_point, start_dir, outside_side)

    accounted_for = set()
    tiles_to_check = outside_tiles.copy()
    while tiles_to_check:
        tile = tiles_to_check.pop()
        accounted_for.add(tile)
        new_tiles = find_outside_points(tile, main_loop, accounted_for, (len(inp), len(inp[0])))
        for tile in new_tiles:
            tiles_to_check.add(tile)

    # total tiles - tiles of loop - tiles that are on the outside
    return (len(inp) * len(inp[0])) - len(main_loop) - len(accounted_for)

def test_a():
    assert a() == 6886

def test_b():
    assert b() == 371

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
