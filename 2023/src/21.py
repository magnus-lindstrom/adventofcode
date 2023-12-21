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

def a(inp, is_test=False):
    if is_test:
        n_steps = 6
    else:
        n_steps = 64

    garden_plots = set()
    rocks = set()
    possibilities = set()
    for i_line, line in enumerate(inp):
        for i_col, char in enumerate(line):
            if char == '#':
                rocks.add((i_line, i_col))
            else:
                garden_plots.add((i_line, i_col))
            if char == 'S':
                possibilities.add((i_line, i_col))

    for _ in range(n_steps):
        new_possibilities = set()
        for row, col in possibilities:
            if row-1 >= 0 and (row-1, col) not in rocks:
                new_possibilities.add((row-1, col))
            if row+1 < len(inp) and (row+1, col) not in rocks:
                new_possibilities.add((row+1, col))
            if col-1 >= 0 and (row, col-1) not in rocks:
                new_possibilities.add((row, col-1))
            if col+1 < len(inp[0]) and (row, col+1) not in rocks:
                new_possibilities.add((row, col+1))
        possibilities = new_possibilities

    return len(possibilities)

def b(inp):
    n_steps = 26501365
    n_steps_is_even = (n_steps % 2 == 0)
    side_length = len(inp)

    rocks = set()
    has_been = set()
    starting_pos = (0, 0)
    for i_line, line in enumerate(inp):
        for i_col, char in enumerate(line):
            if char == '#':
                rocks.add((i_line, i_col))
            if char == 'S':
                starting_pos = (i_line, i_col)

    # will be skipping forward when a pattern emerges in how many possibilities
    # are added. leftover_steps will define the first starting point of those
    # skips. Skips take place in groups of 2*side_length steps ( *2 because we
    # add possibilities only on even or odd number of steps, which makes
    # neighbouring side_length steps not follow a pattern)
    leftover_steps = n_steps % (2 * side_length)

    prev_possibilities = 0
    possibilities = 0
    possibility_diffs = [0]
    second_order_diffs = [0]

    state_queue = []
    state_queue.append((starting_pos[0], starting_pos[1], 0))

    current_step = 0
    next_step_is_even = False  # since the first step is 0, which is even
    while True:
        row, col, steps = state_queue.pop(0)

        # when we pick the first state that has a higher step, we increase
        # current_step
        if steps != current_step:
            current_step = steps
            next_step_is_even = not next_step_is_even

            # if at a possible skipping step, check if 2nd order diffs are
            # regular
            if (current_step - leftover_steps) % (2 * side_length) == 0:
                possibility_diffs.append(possibilities - prev_possibilities)
                second_order_diffs.append(possibility_diffs[-1] - possibility_diffs[-2])
                prev_possibilities = possibilities

                if second_order_diffs[-1] == second_order_diffs[-2]:
                    poss_prim = possibility_diffs[-1]
                    poss_bis = second_order_diffs[-1]
                    nr_skips = (n_steps - current_step) // (2 * side_length)
                    for _ in range(nr_skips):
                        poss_prim += poss_bis
                        possibilities += poss_prim
                    return possibilities

        for new_row, new_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if ((new_row % side_length, new_col % side_length) not in rocks
                    and (new_row, new_col) not in has_been
                    ):
                state_queue.append((new_row, new_col, steps+1))
                has_been.add((new_row, new_col))
                if next_step_is_even and n_steps_is_even:
                    possibilities += 1
                elif not next_step_is_even and not n_steps_is_even: possibilities += 1

def test_a():
    assert a(get_input()) == 3671

def test_b():
    assert b(get_input()) == 609708004316870

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp, is_test=args.test))
    print('b:', b(inp))
