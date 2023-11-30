import os
import pathlib
import sys

# ugly importing that has to be done because of pytest, i hate it
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from utils import get_knot_hash_of_string


def get_test_input():
    return 'flqrgnkx'

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def bin_str_from_hex_str(hex_str):
    bin_str = ''
    for i in range(0, len(hex_str), 2):
        substring = hex_str[i:i+2]
        # 16 to say that incoming nr is in base 16
        # 8 to say that there should be 0 added to reach 8 bits
        current_bin_hash = bin(int(substring, 16))[2:].zfill(8)
        bin_str += current_bin_hash
    return bin_str

def get_bin_hashes():
    str_base = get_input()[0]
    bin_hashes = []

    for nr in range(128):
        knot_hash = get_knot_hash_of_string('{}-{}'.format(str_base, nr))
        bin_hashes.append(bin_str_from_hex_str(knot_hash))

    return bin_hashes

def account_for_group(bin_hashes, spots_accounted_for: set[tuple[int, int]], i_row, j_col):

    spots_accounted_for.add((i_row, j_col))

    if i_row - 1 >= 0:
        if bin_hashes[i_row - 1][j_col] == '1' and (not (i_row - 1, j_col) in spots_accounted_for):
            spots_accounted_for = account_for_group(
                bin_hashes, spots_accounted_for, i_row - 1, j_col
            )
    if i_row + 1 < len(bin_hashes):
        if bin_hashes[i_row + 1][j_col] == '1' and (not (i_row + 1, j_col) in spots_accounted_for):
            spots_accounted_for = account_for_group(
                bin_hashes, spots_accounted_for, i_row + 1, j_col
            )

    if j_col - 1 >= 0:
        if bin_hashes[i_row][j_col - 1] == '1' and (not (i_row, j_col - 1) in spots_accounted_for):
            spots_accounted_for = account_for_group(
                bin_hashes, spots_accounted_for, i_row, j_col - 1
            )
    if j_col + 1 < len(bin_hashes):
        if bin_hashes[i_row][j_col + 1] == '1' and (not (i_row, j_col + 1) in spots_accounted_for):
            spots_accounted_for = account_for_group(
                bin_hashes, spots_accounted_for, i_row, j_col + 1
            )

    return spots_accounted_for

def a():
    bin_hashes = get_bin_hashes()

    nr_squares_used = 0
    for hashh in bin_hashes:
        for char in hashh:
            nr_squares_used += int(char)

    return nr_squares_used

def b():
    bin_hashes = get_bin_hashes()

    # (0,0) is top left corner, (0,1) is to the right of that
    spots_accounted_for: set[tuple[int, int]] = set()
    nr_groups = 0
    for i_row, bin_hash in enumerate(bin_hashes):
        for j_col, char in enumerate(bin_hash):
            if char == '1' and (not (i_row, j_col) in spots_accounted_for):
                spots_accounted_for = account_for_group(bin_hashes, spots_accounted_for, i_row, j_col)
                nr_groups += 1

    return nr_groups

def test_a():
    assert a() == 8148

def test_b():
    assert b() == 1180

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
