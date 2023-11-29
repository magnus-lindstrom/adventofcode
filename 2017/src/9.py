import pathlib

ISTEST = False


def get_input():
    if ISTEST:
        return ['{{<!!>},{<!!>},{<!!>},{<!!>}}']

    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()[0]
    is_inside_garbage = False
    current_group_level = 0
    score = 0
    skip_next_char = False

    for char in inp:
        if is_inside_garbage:
            if skip_next_char:
                skip_next_char = False
            else:
                if char == '!':
                    skip_next_char = True
                elif char == '>':
                    is_inside_garbage = False
        else:
            if char == '{':
                current_group_level += 1
            elif char == '}':
                score += current_group_level
                current_group_level -= 1
            elif char == '<':
                is_inside_garbage = True

    return score

def b():
    inp = get_input()[0]
    is_inside_garbage = False
    non_canceled_garbage_chars = 0
    skip_next_char = False

    for char in inp:
        if is_inside_garbage:
            if skip_next_char:
                skip_next_char = False
            else:
                if char == '!':
                    skip_next_char = True
                elif char == '>':
                    is_inside_garbage = False
                else:
                    non_canceled_garbage_chars += 1
        else:
            if char == '<':
                is_inside_garbage = True

    return non_canceled_garbage_chars

def test_a():
    assert a() == 9251

def test_b():
    assert b() == 4322

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
