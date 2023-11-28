import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    lines = get_input()
    summ = 0
    for line in lines:
        numbers = [int(nr) for nr in line.split('\t')]
        summ += max(numbers) - min(numbers)
    return summ

def b():
    lines = get_input()
    summ = 0
    for line in lines:
        line_done = False
        numbers = [int(nr) for nr in line.split('\t')]
        for inr in range(len(numbers)):
            for jnr in range(inr+1, len(numbers)):
                minn = min(numbers[inr], numbers[jnr])
                maxx = max(numbers[inr], numbers[jnr])
                if maxx % minn == 0:
                    summ += int(maxx / minn)
                    line_done = True
                    break
            if line_done: break
    return summ

def test_a():
    assert a() == 42299

def test_b():
    assert b() == 277

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
