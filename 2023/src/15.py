import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_hash(string):
    hashh = 0
    for char in string:
        hashh += ord(char)
        hashh *= 17
        hashh %= 256
    return hashh

def a():
    inp = get_input()
    summ = 0
    for substr in inp[0].split(','):
        summ += get_hash(substr)
    return summ

def b():
    inp = get_input()
    lenses_by_boxes = []
    focal_lengths_by_boxes = []
    # do not use 'a = [[]] * 256' as that creates the SAME list in all places
    for _ in range(256):
        lenses_by_boxes.append([])
        focal_lengths_by_boxes.append([])

    for operation in inp[0].split(','):
        if '-' in operation:
            label = operation.removesuffix('-')
            box_nr = get_hash(label)
            if label in lenses_by_boxes[box_nr]:
                ind = lenses_by_boxes[box_nr].index(label)
                lenses_by_boxes[box_nr].pop(ind)
                focal_lengths_by_boxes[box_nr].pop(ind)
        else:
            label, focal_length = operation.split('=')
            box_nr = get_hash(label)
            focal_length = int(focal_length)
            if label in lenses_by_boxes[box_nr]:
                ind = lenses_by_boxes[box_nr].index(label)
                focal_lengths_by_boxes[box_nr][ind] = focal_length
            else:
                lenses_by_boxes[box_nr].append(label)
                focal_lengths_by_boxes[box_nr].append(focal_length)

    focusing_power = 0
    for i_box in range(256):
        if not lenses_by_boxes[i_box]:
            continue
        for i_lens, focal_length in enumerate(focal_lengths_by_boxes[i_box]):
            focusing_power += (i_box + 1) * (i_lens + 1) * focal_length

    return focusing_power

def test_a():
    assert a() == 508498

def test_b():
    assert b() == 279116

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
