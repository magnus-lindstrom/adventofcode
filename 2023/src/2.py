import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    cubes = {'red': 12, 'green': 13, 'blue': 14}
    summ = 0
    for line in inp:
        is_possible = True
        game_id = int(line.split()[1].removesuffix(':'))
        pulls = line[1:].split(';')
        for pull in pulls:
            words = pull.split()
            for i in range(1, len(words), 2):
                if words[i].removesuffix(',') == 'red':
                    if int(words[i-1].removesuffix(',')) > cubes['red']:
                        is_possible = False
                if words[i].removesuffix(',') == 'blue':
                    if int(words[i-1].removesuffix(',')) > cubes['blue']:
                        is_possible = False
                if words[i].removesuffix(',') == 'green':
                    if int(words[i-1].removesuffix(',')) > cubes['green']:
                        is_possible = False
        if is_possible:
            summ += game_id
    return summ

def b():
    inp = get_input()
    power = 0
    for line in inp:
        minimum_nrs = {'red': 0, 'green': 0, 'blue': 0}
        pulls = line.split(':')[1].split(';')
        for pull in pulls:
            words = pull.split()
            for i in range(1, len(words), 2):
                reds = int(words[i-1].removesuffix(','))
                blues = int(words[i-1].removesuffix(','))
                greens = int(words[i-1].removesuffix(','))
                if words[i].removesuffix(',') == 'red':
                    if reds > minimum_nrs['red']:
                        minimum_nrs['red'] = reds
                if words[i].removesuffix(',') == 'blue':
                    if blues > minimum_nrs['blue']:
                        minimum_nrs['blue'] = blues
                if words[i].removesuffix(',') == 'green':
                    if greens > minimum_nrs['green']:
                        minimum_nrs['green'] = greens

        power += minimum_nrs['red'] * minimum_nrs['green'] * minimum_nrs['blue']
    return power

def test_a():
    assert a() == 2176

def test_b():
    assert b() == 63700

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
