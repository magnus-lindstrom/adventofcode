import math
import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    times = [int(e) for e in inp[0].split()[1:]]
    distances = [int(e) for e in inp[1].split()[1:]]
    output = 1

    for time, dist in zip(times, distances):
        ways = 0
        for seconds_holding in range(time):
            speed = seconds_holding
            time_left = time - seconds_holding
            if time_left * speed > dist:
                ways += 1
        output *= ways

    return output

def b():
    inp = get_input()
    time = int(''.join(inp[0].split()[1:]))
    distance = int(''.join(inp[1].split()[1:]))

    # wait1 is the first waiting time that we win
    # wait2 is the last
    # wait2 - wait1 + 1 gives the number of integer waiting times that we win
    wait1 = math.ceil(time/2 - math.sqrt(pow((time/2),2) - distance))
    wait2 = math.floor(time/2 + math.sqrt(pow((time/2),2) - distance))
    return wait2 - wait1 + 1

def test_a():
    assert a() == 2756160

def test_b():
    assert b() == 34788142

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
