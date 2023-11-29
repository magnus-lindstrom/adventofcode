import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    registers = {}
    for line in inp:
        words = line.split(' ')
        if words[0] not in registers.keys():
            registers[words[0]] = 0
        if words[4] not in registers.keys():
            registers[words[4]] = 0

        if words[5] == '>':
            if registers[words[4]] > int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '<':
            if registers[words[4]] < int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '>=':
            if registers[words[4]] >= int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '<=':
            if registers[words[4]] <= int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '==':
            if registers[words[4]] == int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '!=':
            if registers[words[4]] != int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

    return max(registers.values())

def b():
    inp = get_input()
    registers = {}
    maxx = 0
    for line in inp:
        words = line.split(' ')
        if words[0] not in registers.keys():
            registers[words[0]] = 0
        if words[4] not in registers.keys():
            registers[words[4]] = 0

        if words[5] == '>':
            if registers[words[4]] > int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '<':
            if registers[words[4]] < int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '>=':
            if registers[words[4]] >= int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '<=':
            if registers[words[4]] <= int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '==':
            if registers[words[4]] == int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if words[5] == '!=':
            if registers[words[4]] != int(words[6]):
                if words[1] == 'inc':
                    registers[words[0]] += int(words[2])
                elif words[1] == 'dec':
                    registers[words[0]] -= int(words[2])

        if registers[words[0]] > maxx:
            maxx = registers[words[0]]

    return maxx

def test_a():
    assert a() == 5752

def test_b():
    assert b() == 6366

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
