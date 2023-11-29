import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_dist_from_steps(steps):
    inp = steps
    # inp = 'se,sw,se,sw,sw'.split(',')
    # inp = 'ne,ne,s,s'.split(',')
    # print(inp)

    n_steps = inp.count('n')
    ne_steps = inp.count('ne')
    nw_steps = inp.count('nw')
    s_steps = inp.count('s')
    se_steps = inp.count('se')
    sw_steps = inp.count('sw')

    # nullify the opposite directions first
    if n_steps > 0 and s_steps > 0:
        minn = min(n_steps, s_steps)
        n_steps -= minn
        s_steps -= minn

    if ne_steps > 0 and sw_steps > 0:
        minn = min(ne_steps, sw_steps)
        ne_steps -= minn
        sw_steps -= minn

    if se_steps > 0 and nw_steps > 0:
        minn = min(se_steps, nw_steps)
        se_steps -= minn
        nw_steps -= minn


    # then only count e.g. se and sw steps as one for every (1, 1) in those
    # directions
    steps = 0
    if nw_steps > 0 and ne_steps > 0:
        minn = min(nw_steps, ne_steps)
        nw_steps -= minn
        ne_steps -= minn
        steps += minn
    if ne_steps > 0 and se_steps > 0:
        minn = min(ne_steps, se_steps)
        ne_steps -= minn
        se_steps -= minn
        steps += minn
    if se_steps > 0 and sw_steps > 0:
        minn = min(se_steps, sw_steps)
        se_steps -= minn
        sw_steps -= minn
        steps += minn
    if sw_steps > 0 and ne_steps > 0:
        minn = min(sw_steps, ne_steps)
        sw_steps -= minn
        ne_steps -= minn
        steps += minn

    return steps + sum([n_steps, ne_steps, se_steps, s_steps, sw_steps, nw_steps])

def a():
    steps = get_input()[0].split(',')

    return get_dist_from_steps(steps)

def b():
    all_steps = get_input()[0].split(',')
    max_dist = 0
    steps_taken = []
    for step in all_steps:
        steps_taken.append(step)
        dist = get_dist_from_steps(steps_taken)
        if dist > max_dist:
            max_dist = dist

    return max_dist

def test_a():
    assert a() == 747

def test_b():
    assert b() == 1544

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
