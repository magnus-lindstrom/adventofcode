import os
import pathlib
import sys

# ugly importing that has to be done because of pytest, i hate it
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from utils import get_knot_hash_of_string, reverse_list_section


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    input_lengts = [int(e) for e in get_input()[0].split(',')]
    listt = [i for i in range(256)]

    list_size = len(listt)
    skip_size = 0
    current_pos = 0

    for inp_len in input_lengts:
        listt = reverse_list_section(listt, inp_len, current_pos)
        current_pos += inp_len + skip_size
        current_pos = current_pos % list_size
        skip_size += 1

    return listt[0] * listt[1]

def b():
    string = get_input()[0]

    return get_knot_hash_of_string(string)

def test_a():
    assert a() == 13760

def test_b():
    assert b() == '2da93395f1a6bb3472203252e3b17fe5'

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
