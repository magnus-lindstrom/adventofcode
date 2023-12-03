import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    step_size = int(get_input()[0])
    n_iterations = 2017
    listt = [0]
    index = 0
    for i in range(1, n_iterations+1):
        new_index = ((index + step_size) % len(listt)) + 1
        listt.insert(new_index, i)
        index = new_index

    return listt[listt.index(2017) + 1]

def b():
    # 0 always stays at position 0, so we just have to keep track of when the
    # new index is 1

    step_size = int(get_input()[0])
    n_iterations = 50000000
    list_length = 1
    val_after_0 = 0
    index = 0
    for i in range(1, n_iterations+1):
        new_index = ((index + step_size) % list_length) + 1
        if new_index == 1:
            val_after_0 = i
        list_length += 1
        index = new_index

    return val_after_0

def test_a():
    assert a() == 1025

def test_b():
    assert b() == 37803463

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
