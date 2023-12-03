import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()[0]
    moves = inp.split(',')
    programs = [chr(a) for a in range(ord('a'), ord('p')+1)]
    n_programs = len(programs)
    for move in moves:
        if move[0] == 's':
            n = int(move[1:])
            programs = programs[-n:] + programs
            programs = programs[:n_programs]
        elif move[0] == 'x':
            nrs = move[1:].split('/')
            tmp = programs[int(nrs[0])]
            programs[int(nrs[0])] = programs[int(nrs[1])]
            programs[int(nrs[1])] = tmp
        else:
            letters = move[1:].split('/')
            index_0 = programs.index(letters[0])
            index_1 = programs.index(letters[1])
            programs[index_0] = letters[1]
            programs[index_1] = letters[0]

    return ''.join(programs)

def b():
    inp = get_input()[0]
    programs = [chr(a) for a in range(ord('a'), ord('p')+1)]
    moves = inp.split(',')
    iterations = 1000000000
    original_programs = programs.copy()
    n_programs = len(programs)
    i = 1
    while i <= iterations:
        for move in moves:
            if move[0] == 's':
                n = int(move[1:])
                programs = programs[-n:] + programs
                programs = programs[:n_programs]
            elif move[0] == 'x':
                nrs = move[1:].split('/')
                tmp = programs[int(nrs[0])]
                programs[int(nrs[0])] = programs[int(nrs[1])]
                programs[int(nrs[1])] = tmp
            else:
                letters = move[1:].split('/')
                index_0 = programs.index(letters[0])
                index_1 = programs.index(letters[1])
                programs[index_0] = letters[1]
                programs[index_1] = letters[0]
        if programs == original_programs:
            period = i
            i = iterations - (iterations % period)
        i += 1

    return ''.join(programs)

def test_a():
    assert a() == 'olgejankfhbmpidc'

def test_b():
    assert b() == 'gfabehpdojkcimnl'

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
