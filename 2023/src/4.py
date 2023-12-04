import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    summ = 0
    for line in inp:
        points = 0
        words = line.split()
        winning_nrs = words[2:12]
        my_nrs = words[13:]
        for nr in my_nrs:
            if nr in winning_nrs:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        summ += points
    return summ

def b():
    inp = get_input()
    winning_nrs_end = 12
    my_nrs_start = 13

    copies = {int(e): 1 for e in range(len(inp))}
    for i_line, line in enumerate(inp):
        wins = 0
        words = line.split()
        winning_nrs = words[2:winning_nrs_end]
        my_nrs = words[my_nrs_start:]
        for nr in my_nrs:
            if nr in winning_nrs:
                wins += 1

        for i in range(wins):
            if i_line+i+1 < len(inp):
                copies[i_line+i+1] += copies[i_line]

    return sum(copies.values())

def test_a():
    assert a() == 25004

def test_b():
    assert b() == 14427616

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
