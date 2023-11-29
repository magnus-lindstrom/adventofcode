import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    scan_depth_to_range = {}
    for line in inp:
        words = line.split()
        depth = int(words[0].removesuffix(':'))
        rangee = int(words[1])
        scan_depth_to_range[depth] = rangee

    scan_dep_to_pos = {}
    scanner_going_down = {}
    for scan_depth in scan_depth_to_range.keys():
        scan_dep_to_pos[scan_depth] = 1
        scanner_going_down[scan_depth] = True

    packet_depth = -1
    severity = 0
    while packet_depth < max(scan_depth_to_range.keys()):
        packet_depth += 1

        # add severity (if called for) if a scanner is located at current depth
        if packet_depth in scan_depth_to_range.keys():
            if scan_dep_to_pos[packet_depth] == 1:
                severity += packet_depth * scan_depth_to_range[packet_depth]

        for scan_depth in scan_dep_to_pos.keys():
            if scanner_going_down[scan_depth]:
                scan_dep_to_pos[scan_depth] += 1
            else:
                scan_dep_to_pos[scan_depth] -= 1

            if (scan_dep_to_pos[scan_depth] == 1
                or scan_dep_to_pos[scan_depth] == scan_depth_to_range[scan_depth]):

                scanner_going_down[scan_depth] = not scanner_going_down[scan_depth]


    return severity

def b():
    inp = get_input()
    scanner_depths = []
    scanner_ranges = []

    for line in inp:
        words = line.split()
        scanner_depths.append(int(words[0].removesuffix(':')))
        scanner_ranges.append(int(words[1]))

    delay = -1
    not_there_yet = True
    while not_there_yet:
        delay += 1
        not_there_yet = False

        for depth, rangee in zip(scanner_depths, scanner_ranges):
            # you are at the depth of the scanner at t = depth + delay
            # scanners are at their top position at
            # t = 0, 2(range-1), 4(range-1), 6(range-1)
            # Thus, make sure that delay + depth % 2(range-1) is not 0 for any
            # scanner's depth or range
            if (delay + depth) % (2 * (rangee - 1)) == 0:
                not_there_yet = True
                break

    return delay



def test_a():
    assert a() == 1960

def test_b():
    assert b() == 3903378

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
