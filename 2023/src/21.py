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

    for i_step in range(n_steps):
        new_possibilities = set()
        for row, col in possibilities:
            #print((row-1, col) in rocks)
            if row-1 >= 0 and (row-1, col) not in rocks:
                new_possibilities.add((row-1, col))
            if row+1 < len(inp) and (row+1, col) not in rocks:
                new_possibilities.add((row+1, col))
            if col-1 >= 0 and (row, col-1) not in rocks:
                new_possibilities.add((row, col-1))
            if col+1 < len(inp[0]) and (row, col+1) not in rocks:
                new_possibilities.add((row, col+1))
        possibilities = new_possibilities

    #print(rocks)
    #print(possibilities)

    return len(possibilities)

def b(inp):

    n_steps = 5000
    n_steps_is_even = (n_steps % 2 == 0)
    rows, cols = len(inp), len(inp[0])

    garden_plots = set()
    rocks = set()
    this_step = set()
    one_step_back = set()
    two_steps_back = set()
    state_queue = []
    for i_line, line in enumerate(inp):
        for i_col, char in enumerate(line):
            if char == '#':
                rocks.add((i_line, i_col))
            else:
                garden_plots.add((i_line, i_col))
            if char == 'S':
                state_queue.append((i_line, i_col, 0))
                this_step.add((i_line, i_col))


    # to account for start step
    if n_steps_is_even: possibilities = 1
    else: possibilities = 0
    old_possibilities = 0

    steps = 0
    current_step = 0
    is_even = True
    seen_ratios = set()
    while True:
        #print(state_queue)
        row, col, steps = state_queue.pop(0)
        if steps != current_step:
            current_step = steps
            two_steps_back = one_step_back
            one_step_back = this_step
            this_step = set()
            is_even = not is_even
            #if current_step % 1000 == 0:
                #print(n_steps, ',', current_step)
            if current_step % (2 * len(inp)) == 0:
                ratio = (possibilities - old_possibilities) / 4 / current_step
                if ratio in seen_ratios:
                    print('DING', ratio)
                else:
                    print(ratio)
                    seen_ratios.add(ratio)
                old_possibilities = possibilities
            #print('step {}, is even {}'.format(current_step, is_even))

            if current_step == n_steps:
                break

        for new_row, new_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:

            if ((new_row % rows, new_col % cols) not in rocks
                    and (new_row, new_col) not in this_step
                    and (new_row, new_col) not in one_step_back
                    and (new_row, new_col) not in two_steps_back
                    ):
                state_queue.append((new_row, new_col, steps+1))
                this_step.add((new_row, new_col))
                if not is_even and n_steps_is_even:
                    #print(row-1, col)
                    possibilities += 1
                elif is_even and not n_steps_is_even: possibilities += 1

    #print(len(this_step)+ len(one_step_back)+ len(two_steps_back))
    #print(been)

    #print(rocks)
    #print(possibilities)

    return possibilities

def b_new(inp):
    # start 100 steps away from the perfect diamond, count those manually
    # (only start if no rock)
    # first count inner diamond
    n_steps = 500000
    side_length = len(inp)
    inner_diamond_steps = max([n_steps - 2 * side_length, 0])
    if inner_diamond_steps % 2 != 0:
        inner_diamond_steps -= 1
    has_been = set()

    n_steps_is_even = (n_steps % 2 == 0)

    rocks = set()
    starting_pos = (0, 0)
    for i_line, line in enumerate(inp):
        for i_col, char in enumerate(line):
            if char == '#':
                rocks.add((i_line, i_col))
            if char == 'S':
                starting_pos = (i_line, i_col)

    # how many nodes that count are in one full plot?
    is_even = True
    count_per_plot = 0
    for row in range(side_length):
        for col in range(side_length):
            if is_even == n_steps_is_even and (row, col) not in rocks:
                count_per_plot += 1
            is_even = not is_even
    print('inner diamond steps:', inner_diamond_steps, 'count_per_plot:', count_per_plot)
    print('n_steps:', n_steps)

    # how many plots fit within the inner diamond?

    if inner_diamond_steps < 2 * side_length:
        possibilities = 0
        state_queue = []
        state_queue.append((starting_pos[0], starting_pos[1], 0))

    else:
        # nr inner plots is the nr of plots that we can stack on top of eachother
        # above the current plot, without reaching the boundaries of the inner
        # diamond
        nr_inner_plots = (inner_diamond_steps - (side_length // 2)) // side_length
        nr_inner_plots -= 1
        #print(nr_inner_plots, nr_inner_plots * side_length + starting_pos[0])

        # side triangles are counted through n/2 * (n+1) but n is nr_inner_plots-1
        nr_plots_added_total = int(1 + 4 * nr_inner_plots + ((nr_inner_plots-1)/2 *(nr_inner_plots)))
        possibilities = count_per_plot * nr_plots_added_total
        print(nr_plots_added_total, possibilities)

        # now we want to set starting positions along the inner triangle, but first
        # we need to ensure that we "have been" around the edges of the counted
        # plots
        for column_plot_offset in range(-nr_inner_plots, 0):
            for row_plot_offset in [nr_inner_plots - abs(column_plot_offset),
                                    -(nr_inner_plots - abs(column_plot_offset))]:
                inner_pos = (starting_pos[0] + row_plot_offset*side_length, starting_pos[1] + column_plot_offset*side_length)
                # upper edge
                row = inner_pos[0] - (side_length // 2)
                for col in range(inner_pos[1] - (side_length // 2), inner_pos[1] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # lower edge
                row = inner_pos[0] + (side_length // 2)
                for col in range(inner_pos[1] - (side_length // 2), inner_pos[1] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # left side
                col = inner_pos[1] - (side_length // 2)
                for row in range(inner_pos[0] - (side_length // 2), inner_pos[0] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # right side
                col = inner_pos[1] + (side_length // 2)
                for row in range(inner_pos[0] - (side_length // 2), inner_pos[0] + (side_length // 2) + 1):
                    has_been.add((row, col))

        # other half of the outside
        for column_plot_offset in range(nr_inner_plots + 1):
            for row_plot_offset in [nr_inner_plots - column_plot_offset, -(nr_inner_plots - column_plot_offset)]:
                inner_pos = (starting_pos[0] + row_plot_offset*side_length, starting_pos[1] + column_plot_offset*side_length)
                # upper edge
                row = inner_pos[0] - (side_length // 2)
                for col in range(inner_pos[1] - (side_length // 2), inner_pos[1] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # lower edge
                row = inner_pos[0] + (side_length // 2)
                for col in range(inner_pos[1] - (side_length // 2), inner_pos[1] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # left side
                col = inner_pos[1] - (side_length // 2)
                for row in range(inner_pos[0] - (side_length // 2), inner_pos[0] + (side_length // 2) + 1):
                    has_been.add((row, col))
                # right side
                col = inner_pos[1] + (side_length // 2)
                for row in range(inner_pos[0] - (side_length // 2), inner_pos[0] + (side_length // 2) + 1):
                    has_been.add((row, col))

        state_queue = []
        # now, finally, set starting positions along the inner diamond
        # when defining inner diamond steps, we ensured that it is an even nr of steps
        state_queue.append((starting_pos[0], inner_diamond_steps + starting_pos[1], inner_diamond_steps))
        state_queue.append((starting_pos[0], -inner_diamond_steps + starting_pos[1], inner_diamond_steps))
        #starting_positions = []
        #starting_positions.append((starting_pos[0], inner_diamond_steps + starting_pos[1], inner_diamond_steps))
        #starting_positions.append((starting_pos[0], -inner_diamond_steps + starting_pos[1], inner_diamond_steps))
        for col in range(-inner_diamond_steps + 1, inner_diamond_steps):
            for row in [inner_diamond_steps - abs(col), -(inner_diamond_steps - abs(col))]:
                state_queue.append((row + starting_pos[0], col + starting_pos[1], inner_diamond_steps))
                #starting_positions.append((row + starting_pos[0], col + starting_pos[1], inner_diamond_steps))
    #print(state_queue)

    next_step_is_even = False
    current_step = inner_diamond_steps
    #pprint(state_queue, rocks, has_been, side_length, n_steps, inner_diamond_steps, starting_pos)
    count = 0
    while True:
        row, col, steps = state_queue.pop(0)
        if steps != current_step:
            current_step = steps
            next_step_is_even = not next_step_is_even

            if current_step == n_steps:
                break
            count += 1
            #if count == 20:
                #pprint(state_queue, rocks, has_been, side_length, n_steps, inner_diamond_steps, starting_pos)
                #return

        for new_row, new_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:

            if ((new_row % side_length, new_col % side_length) not in rocks
                    and (new_row, new_col) not in has_been
                    ):
                state_queue.append((new_row, new_col, steps+1))
                has_been.add((new_row, new_col))
                if next_step_is_even and n_steps_is_even:
                    #print(row-1, col)
                    possibilities += 1
                elif not next_step_is_even and not n_steps_is_even: possibilities += 1
    #pprint(state_queue, rocks, has_been, side_length, n_steps, inner_diamond_steps, starting_pos)

    return possibilities

def b_third(inp):
    n_steps = 26501365
    side_length = len(inp)
    has_been = set()
    if (n_steps // (2 * side_length)) < 1:
        skipping_side_lengths = 0
        leftover_steps = n_steps
    else:
        skipping_side_lengths = n_steps // (2 * side_length)
        leftover_steps = n_steps % (2 * side_length)

    n_steps_is_even = (n_steps % 2 == 0)

    rocks = set()
    starting_pos = (0, 0)
    for i_line, line in enumerate(inp):
        for i_col, char in enumerate(line):
            if char == '#':
                rocks.add((i_line, i_col))
            if char == 'S':
                starting_pos = (i_line, i_col)

    prev_possibilities = 0
    possibilities = 0
    possibility_diffs = [0, 0]
    second_diffs = [0, 0]
    state_queue = []
    state_queue.append((starting_pos[0], starting_pos[1], 0))

    next_step_is_even = False
    current_step = 0
    while True:
        row, col, steps = state_queue.pop(0)
        if steps != current_step:
            current_step = steps
            next_step_is_even = not next_step_is_even

            if current_step == n_steps:
                break
            if (current_step - leftover_steps) % (2 * side_length) == 0:
                #break
            #count += 1
            #if current_step % (2 * side_length) == 0:
                possibility_diffs.append(possibilities - prev_possibilities)
                second_diffs.append(possibility_diffs[-1] - possibility_diffs[-2])
                if second_diffs[-1] == second_diffs[-2]:
                    print('overdrive, will skip hop {} times, {} steps each time'.format(skipping_side_lengths, 2*side_length))
                    poss_prim = possibility_diffs[-1]
                    poss_bis = second_diffs[-1]
                    nr_skips = (n_steps - current_step) // (2 * side_length)
                    for _ in range(nr_skips):
                        poss_prim += poss_bis
                        possibilities += poss_prim
                    return possibilities
                prev_possibilities = possibilities

        for new_row, new_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:

            if ((new_row % side_length, new_col % side_length) not in rocks
                    and (new_row, new_col) not in has_been
                    ):
                state_queue.append((new_row, new_col, steps+1))
                has_been.add((new_row, new_col))
                if next_step_is_even and n_steps_is_even:
                    #print(row-1, col)
                    possibilities += 1
                elif not next_step_is_even and not n_steps_is_even: possibilities += 1
    #pprint(state_queue, rocks, has_been, side_length, n_steps, [], starting_pos)

    return possibilities

def pprint(state_queue, rocks, has_been, side_length, n_steps, inner_diamond_steps, starting_pos):
    for col in range(-n_steps + starting_pos[0], n_steps + starting_pos[0] + 1):
        for row in range(-n_steps + starting_pos[0], n_steps + starting_pos[0] + 1):
            trans_pos = (row % side_length, col % side_length)
            pos = (row, col)
            #if abs(col - starting_pos[1]) + abs(row - starting_pos[0]) == inner_diamond_steps:
                #print('I', end='')
            #if abs(col - starting_pos[1]) + abs(row - starting_pos[0]) == n_steps:
                #print('O', end='')
            if trans_pos in rocks:
                print('#', end='')
            elif pos in [p[:2] for p in state_queue]:
                print('P', end='')
            elif pos in has_been:
                print(' ', end='')
            else:
                print('.', end='')
        print()
    print()

def test_a():
    assert a(get_input()) == 3671

def test_b():
    assert b_third(get_input()) == 609708004316870

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp, is_test=args.test))
    print('b:', b_third(inp))
