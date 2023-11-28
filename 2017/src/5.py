import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    instructions = [int(i) for i in get_input()]
    length = len(instructions)

    i = 0
    jump_counter = 0
    while True:
        jump = instructions[i]
        instructions[i] += 1
        i += jump
        jump_counter += 1
        if i < 0 or i >= length:
            return jump_counter

def b():
    instructions = [int(i) for i in get_input()]
    length = len(instructions)

    i = 0
    jump_counter = 0
    while True:
        jump = instructions[i]
        if instructions[i] >= 3:
            instructions[i] -= 1
        else:
            instructions[i] += 1

        i += jump
        jump_counter += 1
        if i < 0 or i >= length:
            return jump_counter

def test_a():
    assert a() == 375042

def test_b():
    assert b() == 28707598

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
