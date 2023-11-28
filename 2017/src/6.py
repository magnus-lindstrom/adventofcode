import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    banks = [int(i) for i in get_input()[0].split('\t')]
    length = len(banks)
    seen_states = {' '.join([str(b) for b in banks])}

    redists = 0
    old_state_has_been_seen_again = False
    while not old_state_has_been_seen_again:
        redists += 1
        maxx = max(banks)
        max_index = banks.index(maxx)
        banks[max_index] = 0

        for i in range(maxx):
            banks[(max_index + 1 + i) % length] += 1

        state = ' '.join([str(b) for b in banks])
        if state in seen_states:
            old_state_has_been_seen_again = True
        else:
            seen_states.add(state)
    return redists

def b():
    banks = [int(i) for i in get_input()[0].split('\t')]
    length = len(banks)
    seen_states = {' '.join([str(b) for b in banks])}

    redists = 0
    redists_in_loop = 0
    old_state_has_been_seen_again = False
    first_reoccurring_state = None
    while True:
        redists += 1
        maxx = max(banks)
        max_index = banks.index(maxx)
        banks[max_index] = 0

        for i in range(maxx):
            banks[(max_index + 1 + i) % length] += 1

        state = ' '.join([str(b) for b in banks])

        if old_state_has_been_seen_again:
            redists_in_loop += 1
            if state == first_reoccurring_state:
                return redists_in_loop
        elif state in seen_states:
            old_state_has_been_seen_again = True
            first_reoccurring_state = state
        else:
            seen_states.add(state)

def test_a():
    assert a() == 14029

def test_b():
    assert b() == 2765

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
