import math


def reverse_list_section(listt, section_size, current_pos):
    list_size = len(listt)
    for i in range(math.ceil(section_size / 2)):
        tmp = listt[(current_pos + i) % list_size]
        listt[(current_pos + i) % list_size] = listt[
            (current_pos + section_size - i - 1) % list_size
        ]

        listt[(current_pos + section_size - i - 1) % list_size] = tmp
    return listt

def get_knot_hash_of_string(string):
    input_lengts = [ord(char) for char in string]
    input_lengts.extend([17, 31, 73, 47, 23])
    listt = [i for i in range(256)]

    list_size = len(listt)
    skip_size = 0
    current_pos = 0

    for _ in range(64):
        for inp_len in input_lengts:
            listt = reverse_list_section(listt, inp_len, current_pos)

            current_pos += inp_len + skip_size
            current_pos = current_pos % list_size
            skip_size += 1

    dense_hashes = []
    for i_block in range(16):
        dense_hash = listt[i_block * 16]
        for e in listt[(1 + (i_block * 16)):(1 + (i_block * 16) + 15)]:
            dense_hash = dense_hash ^ e
        dense_hashes.append(dense_hash)

    knot_hash = ""
    for dense_hash in dense_hashes:
        hashh = hex(dense_hash).removeprefix('0x')
        if len(hashh) == 1:
            hashh = '0' + hashh
        knot_hash += hashh

    return knot_hash
