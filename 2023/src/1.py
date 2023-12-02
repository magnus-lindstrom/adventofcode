import pathlib


def get_input():

    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    summ = 0
    for line in inp:
        nr = ''
        for char in line:
            if char.isdigit():
                nr += char
        nr = nr[0] + nr[-1]
        summ += int(nr)

    return summ

def b():
    inp = get_input()
    summ = 0
    for line in inp:
        nr = ''
        for ichar, char in enumerate(line):
            if char.isdigit():
                nr += char

            elif (ichar+3) <= len(line) and line[ichar:ichar+3] == 'one':
                nr += '1'
            elif (ichar+3) <= len(line) and line[ichar:ichar+3] == 'two':
                nr += '2'
            elif (ichar+5) <= len(line) and line[ichar:ichar+5] == 'three':
                nr += '3'
            elif (ichar+4) <= len(line) and line[ichar:ichar+4] == 'four':
                nr += '4'
            elif (ichar+4) <= len(line) and line[ichar:ichar+4] == 'five':
                nr += '5'
            elif (ichar+3) <= len(line) and line[ichar:ichar+3] == 'six':
                nr += '6'
            elif (ichar+5) <= len(line) and line[ichar:ichar+5] == 'seven':
                nr += '7'
            elif (ichar+5) <= len(line) and line[ichar:ichar+5] == 'eight':
                nr += '8'
            elif (ichar+4) <= len(line) and line[ichar:ichar+4] == 'nine':
                nr += '9'
        nr = nr[0] + nr[-1]
        summ += int(nr)


    return summ

def test_a():
    assert a() == 55712

def test_b():
    assert b() == 55413

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
