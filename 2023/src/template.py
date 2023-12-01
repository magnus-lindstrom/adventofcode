import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    return 0

def b():
    inp = get_input()
    return 0

def test_a():
    assert a() == 0

def test_b():
    assert b() == 0

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
