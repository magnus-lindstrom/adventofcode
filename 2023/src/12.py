import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_ways_of_placing_remaining_runs(solutions, runs_list,
                                       is_perhaps_broken_spring,
                                       is_broken_spring, i_run, i_char_start):

    if (i_run, i_char_start) in solutions.keys():
        return solutions[(i_run, i_char_start)], solutions

    # Endpoint of recursion. If there are no more '#' that we have to account
    # for, then this is a solution and we return 1.
    if i_run == len(runs_list):
        if not any(is_broken_spring[i_char_start:]):
            return 1, solutions
        else:
            return 0, solutions

    i_char = i_char_start
    n_valid_combs = 0
    while i_char <= len(is_broken_spring) - runs_list[i_run]:

        if (all(is_perhaps_broken_spring[i_char:i_char+runs_list[i_run]])
                and (
                    i_char+runs_list[i_run] == len(is_broken_spring)  # no more characters
                    or not is_broken_spring[i_char+runs_list[i_run]]  # next char is not a '#'
                )
        ):
            combs, solutions = get_ways_of_placing_remaining_runs(
                solutions, runs_list, is_perhaps_broken_spring,
                is_broken_spring, i_run + 1, i_char + runs_list[i_run] + 1
            )
            n_valid_combs += combs

        if is_broken_spring[i_char]:
            # this char is a '#', do not pass this char. That would skip a
            # broken spring which must be included in a run
            break

        i_char += 1

    solutions[(i_run, i_char_start)] = n_valid_combs

    return n_valid_combs, solutions

def solution(mult):
    inp = get_input()
    n_valid_combs = 0

    for line in inp:
        words = line.split()
        springs = (words[0] + '?') * mult
        springs = springs[:-1]
        is_perhaps_broken_spring = [True if e in ['#', '?'] else False for e in springs]
        is_broken_string = [True if e == '#' else False for e in springs]
        runs_list = [int(e) for e in words[1].split(',')] * mult

        combs, _ = get_ways_of_placing_remaining_runs(
            {}, runs_list, is_perhaps_broken_spring, is_broken_string, 0, 0
        )
        n_valid_combs += combs

    return n_valid_combs

def a():
    return solution(1)

def b():
    return solution(5)

def test_a():
    assert a() == 7090

def test_b():
    assert b() == 6792010726878

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
