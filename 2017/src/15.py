import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    a_nr = int(inp[0].split()[-1])
    b_nr = int(inp[1].split()[-1])

    reps = int(4e7)

    a_factor = 16807
    b_factor = 48271
    divisor = 2147483647

    count = 0

    for _ in range(reps):
        a_nr *= a_factor
        a_nr = a_nr % divisor
        a_bin = bin(a_nr)[2:].zfill(16)

        b_nr *= b_factor
        b_nr = b_nr % divisor
        b_bin = bin(b_nr)[2:].zfill(16)

        if a_bin[-16:] == b_bin[-16:]:
            count += 1

    return count

def b():
    inp = get_input()
    a_nr = int(inp[0].split()[-1])
    b_nr = int(inp[1].split()[-1])

    reps = int(5e6)

    a_factor = 16807
    b_factor = 48271
    divisor = 2147483647

    a_multiples = 4
    b_multiples = 8

    a_proposals = []
    b_proposals = []

    count = 0

    i = 0
    while True:
        a_nr *= a_factor
        a_nr = a_nr % divisor

        b_nr *= b_factor
        b_nr = b_nr % divisor

        if a_nr % a_multiples == 0:
            a_proposals.append(a_nr)
        if b_nr % b_multiples == 0:
            b_proposals.append(b_nr)

        if len(a_proposals) >= reps and len(b_proposals) >= reps:
            break

    for i in range(min([len(a_proposals), len(b_proposals)])):
        a_bin = bin(a_proposals[i])[2:].zfill(16)
        b_bin = bin(b_proposals[i])[2:].zfill(16)
        if a_bin[-16:] == b_bin[-16:]:
            count += 1

    return count

def test_a():
    assert a() == 592

def test_b():
    assert b() == 320

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
