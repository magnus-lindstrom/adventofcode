import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    summ = 0

    for i_line, line in enumerate(inp):
        i_char = 0
        while i_char < len(line):
            if line[i_char].isdigit():
                nr = ''
                is_part_nr = False
                for j_char in range(i_char, len(line)):
                    if line[j_char].isdigit():
                        nr += line[j_char]
                    else:
                        i_char = j_char
                        break
                    for ii in [i_line-1, i_line, i_line+1]:
                        for jj in [j_char-1, j_char, j_char+1]:
                            if ((ii == i_line and jj == j_char)
                                or not 0 <= ii < len(inp)
                                or not 0 <= jj < len(line)
                            ):
                                continue
                            if inp[ii][jj] != '.' and not inp[ii][jj].isdigit():
                                is_part_nr = True
                if is_part_nr:
                    summ += int(nr)
            i_char += 1

    return summ

def b():
    inp = get_input()
    summ = 0
    gear_nrs = {}

    for i_line, line in enumerate(inp):
        i_char = 0
        while i_char < len(line):
            if line[i_char].isdigit():
                nr = ''
                found_gears = set()
                for j_char in range(i_char, len(line)):
                    if line[j_char].isdigit():
                        nr += line[j_char]
                    else:
                        i_char = j_char
                        break
                    for ii in [i_line-1, i_line, i_line+1]:
                        for jj in [j_char-1, j_char, j_char+1]:
                            if ((ii == i_line and jj == j_char)
                                or ii < 0 or ii >= len(inp)
                                or jj < 0 or jj >= len(line)
                            ):
                                continue
                            if inp[ii][jj] != '.' and not inp[ii][jj].isdigit():
                                found_gears.add((ii,jj))
                for gear in found_gears:
                    if gear not in gear_nrs.keys():
                        gear_nrs[gear] = []
                    gear_nrs[gear].append(int(nr))
            i_char += 1

    for gear in gear_nrs.keys():
        if len(gear_nrs[gear]) == 2:
            summ += gear_nrs[gear][0] * gear_nrs[gear][1]
    return summ

def test_a():
    assert a() == 512794

def test_b():
    assert b() == 67779080

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
