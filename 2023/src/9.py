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

def get_prev_val_rec(seq):
    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    if all([diffs[0] == diffs[i] for i in range(len(diffs))]):
        return seq[0] - diffs[0]
    else:
        return seq[0] - get_prev_val_rec(diffs)

def get_next_val_rec(seq):
    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    if all([diffs[0] == diffs[i] for i in range(len(diffs))]):
        return seq[-1] + diffs[0]
    else:
        return seq[-1] + get_next_val_rec(diffs)

def a():
    inp = get_input()
    summ = 0

    for line in inp:
        sequence = [int(e) for e in line.split()]
        next_val = get_next_val_rec(sequence)
        summ += next_val

    return summ

def b():
    inp = get_input()
    summ = 0

    for line in inp:
        sequence = [int(e) for e in line.split()]
        next_val = get_prev_val_rec(sequence)
        summ += next_val

    return summ

def test_a():
    assert a() == 1842168671

def test_b():
    assert b() == 903

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
