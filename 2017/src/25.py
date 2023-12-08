import pathlib


def get_test_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr + '_test')
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    #inp = get_test_input()
    inp = [line.removesuffix(':').removesuffix('.') for line in inp]

    states = {}

    words = inp[0].split()
    starting_state = words[-1].removesuffix('.')
    words = inp[1].split()
    steps_before_checksum = int(words[5])
    i_line = 3
    while i_line < len(inp):
        state = None
        write_if_zero = None
        write_if_one = None
        move_if_zero = None
        move_if_one = None
        next_state_if_zero = None
        next_state_if_one = None

        words = inp[i_line].split()
        state = words[2]

        words = inp[i_line+1].split()
        if words[5] == '0':
            words = inp[i_line+2].split()
            write_if_zero = int(words[4])
            words = inp[i_line+3].split()
            if words[6] == 'right':
                move_if_zero = 1
            else:
                move_if_zero = -1
            words = inp[i_line+4].split()
            next_state_if_zero = words[4]

            words = inp[i_line+6].split()
            write_if_one = int(words[4])
            words = inp[i_line+7].split()
            if words[6] == 'right':
                move_if_one = 1
            else:
                move_if_one = -1
            words = inp[i_line+8].split()
            next_state_if_one = words[4]
        else:
            words = inp[i_line+2].split()
            write_if_one = int(words[4])
            words = inp[i_line+3].split()
            if words[6] == 'right':
                move_if_one = 1
            else:
                move_if_one = -1
            words = inp[i_line+4].split()
            next_state_if_one = words[4]

            words = inp[i_line+6].split()
            write_if_zero = int(words[4])
            words = inp[i_line+7].split()
            if words[6] == 'right':
                move_if_zero = 1
            else:
                move_if_zero = -1
            words = inp[i_line+8].split()
            next_state_if_zero = words[4]

        states[state] = {
            'write_if_zero': write_if_zero,
            'write_if_one': write_if_one,
            'move_if_zero': move_if_zero,
            'move_if_one': move_if_one,
            'next_state_if_zero': next_state_if_zero,
            'next_state_if_one': next_state_if_one,
        }

        i_line += 10

    current_state = starting_state
    current_slot = 0
    slots = {}
    for _ in range(steps_before_checksum):
        if current_slot not in slots.keys():
            slots[current_slot] = 0

        if slots[current_slot] == 0:
            slots[current_slot] = states[current_state]['write_if_zero']
            current_slot += states[current_state]['move_if_zero']
            current_state = states[current_state]['next_state_if_zero']
        elif slots[current_slot] == 1:
            slots[current_slot] = states[current_state]['write_if_one']
            current_slot += states[current_state]['move_if_one']
            current_state = states[current_state]['next_state_if_one']

    return sum(slots.values())

def b():
    return 'Merry Christmas!'

def test_a():
    assert a() == 633

def test_b():
    assert b() == 'Merry Christmas!'

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
