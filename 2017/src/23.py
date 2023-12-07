import pathlib
from sys import maxsize


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    count = 0
    regs = {char: 0 for char in 'abcdefgh'}

    i_line = 0
    while 0 <= i_line < len(inp):
        offset = 1
        words = inp[i_line].split()
        if words[0] == 'set':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] = int(words[2])
            else:
                regs[words[1]] = regs[words[2]]
        elif words[0] == 'sub':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] -= int(words[2])
            else:
                regs[words[1]] -= regs[words[2]]
        elif words[0] == 'mul':
            count += 1
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] *= int(words[2])
            else:
                regs[words[1]] *= regs[words[2]]
        elif words[0] == 'jnz':
            if words[1] in regs.keys():
                if regs[words[1]] != 0:
                    offset = int(words[2])
            elif int(words[1]) != 0:
                offset = int(words[2])
        i_line += offset

    return count

def get_pp_string(regs):
    string = ''
    for k, v in regs.items():
        string += '{}: {}'.format(k, v)
        string += '\t'
    return string.strip()

def execute_line(line, regs):
    offset = 1
    words = line.split()
    if words[0] == 'set':
        if words[2].removeprefix('-').isdigit():
            regs[words[1]] = int(words[2])
        else:
            regs[words[1]] = regs[words[2]]
    elif words[0] == 'sub':
        if words[2].removeprefix('-').isdigit():
            regs[words[1]] -= int(words[2])
        else:
            regs[words[1]] -= regs[words[2]]
    elif words[0] == 'mul':
        if words[2].removeprefix('-').isdigit():
            regs[words[1]] *= int(words[2])
        else:
            regs[words[1]] *= regs[words[2]]
    elif words[0] == 'jnz':
        if words[1] in regs.keys():
            if regs[words[1]] != 0:
                offset = int(words[2])
        elif int(words[1]) != 0:
            offset = int(words[2])
    return offset, regs

def b_old():
    inp = get_input()
    regs = {char: 0 for char in 'abcdefgh'}
    regs['a'] = 1

    seen_regs = set()

    i_steps = 0
    i_line = 0
    seen_regs.add((regs.values(), i_line))
    old_b = regs['b']
    old_c = regs['c']
    old_d = regs['d']
    old_f = regs['f']
    old_h = regs['h']

    first_jump_count = 0
    while 0 <= i_line < len(inp):
        #if i_line == 11:
        #    print(i_line, get_pp_string(regs))

        offset, regs = execute_line(inp[i_line], regs)

        if old_d != regs['d']:
            if regs['d'] == 3:
                regs['d'] = regs['b'] - 1
            #print(i_line, get_pp_string(regs))
        if old_h != regs['h']:
            print(i_line, get_pp_string(regs))
            if regs['c'] - regs['b'] > 4000:
                mult = 100
                regs['b'] += mult * 34
                regs['d'] += mult * 34
                regs['e'] += mult * 34
                regs['h'] += 34
            elif regs['c'] - regs['b'] > 400:
                mult = 10
                regs['b'] += mult * 34
                regs['d'] += mult * 34
                regs['e'] += mult * 34
                regs['h'] += 34

        i_line += offset
        i_steps += 1
        old_b = regs['b']
        old_c = regs['c']
        old_d = regs['d']
        old_f = regs['f']
        old_h = regs['h']


    return regs['h']

def b():
    # I transcribed the program in from the input and reconstructed it in
    # python code instead. And then started condensing the lines until I could
    # identify a double for loop from 2 - (b-1), which is a check for if b is
    # prime. That can be implemented faster. The original transcription of the
    # program is at the bottom of the file (at least from the start of the
    # loop, I forgot to copy over the initial lines that were later removed).

    f = 0
    h = 0
    b = 79  # 0
    b *= 100  # 4
    b += 100000  # 5
    c = b  # 6
    c += 17000 # 7
    while True:
        f = 1  # 8

        # if b is a prime, set f = 0
        for x in range(2, b):
            if b % x == 0:
                f = 0
                break

        if f == 0:  # 24
            h += 1  # 25
        if b == c:  # 28
            return h
        b += 17

def test_a():
    assert a() == 5929

def test_b():
    assert b() == 907

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())


#    while True:
#        b = 79  # 0
#        c = b  # 1
#        b *= 100  # 4
#        b += 100000  # 5
#        c = b  # 6
#        c += 17000 # 7
#        while True:
#            f = 1  # 8
#            d = 2  # 9
#            while g != 0:
#                print(g)
#
#                e = 2  # 10
#                while g != 0:
#
#                    g = d  # 11
#                    g *= e  # 12
#                    g -= b # 13
#                    if g == 0:  # 14
#                        f = 0  # 15
#                    e += 1  # 16
#                    g = e  # 17
#                    g -= b  # 18
#
#                d += 1  # 20
#                g = d  # 21
#                g -= b  # 22
#            # 23
#
#            if f == 0:  # 24
#                h += 1  # 25
#            g = b  # 26
#            g -= c  # 27
#            if g == 0:  # 28
#                return h
#
#            b += 17
