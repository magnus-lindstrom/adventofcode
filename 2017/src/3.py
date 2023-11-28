import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        a = [line.strip() for line in f.readlines()]
    return a

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.facing_right = True
        self.facing_up = False
        self.facing_left = False
        self.facing_down = False
        self.steps_taken = 0
        self.values: dict[tuple[int, int], int] = {(0, 0): 1}

    def take_step(self):
        self.steps_taken += 1

        if self.facing_right:
            self.x += 1
            if self.x == (-self.y + 1):
                self.facing_up = True
                self.facing_right = False
            elif self.steps_taken == 1:
                self.facing_up = True
                self.facing_right = False
        elif self.facing_up:
            self.y += 1
            if self.x == self.y:
                self.facing_left = True
                self.facing_up = False
        elif self.facing_left:
            self.x -= 1
            if -self.x == self.y:
                self.facing_down = True
                self.facing_left = False
        elif self.facing_down:
            self.y -= 1
            if self.x == self.y:
                self.facing_right = True
                self.facing_down = False

    def distance_to_origin(self):
        return abs(self.x) + abs(self.y)

    def set_value(self):
        self.values[(self.x, self.y)] = 0
        # print('standing on ({}, {})'.format(self.x, self.y))
        for i in range(-1, 2):
            for j in range(-1, 2):
                # print(i, j)
                if not (i == j and i == 0):
                    # print('a')
                    if (self.x + i, self.y + j) in self.values.keys():
                        # print('added from point ({}, {})'.format(self.x + i, self.y + j))
                        self.values[(self.x, self.y)] += self.values[(self.x + i, self.y + j)]

    def get_value(self):
        return self.values[(self.x, self.y)]


    def __str__(self):
        return "({}, {})".format(self.x, self.y)


def a():
    data_square_nr = int(get_input()[0])
    # data_square_nr = 12
    position = Position()
    for _ in range(1, data_square_nr):
        position.take_step()
    return position.distance_to_origin()

def b():
    max_value = int(get_input()[0])
    #max_value = 350
    position = Position()
    while True:
        position.take_step()
        position.set_value()
        #print('value: {}'.format(position.get_value()))
        if position.get_value() > max_value:
            return position.get_value()

def test_a():
    assert a() == 480

def test_b():
    assert b() == 349975

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
