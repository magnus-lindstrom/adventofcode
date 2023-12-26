import argparse
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def has_abba(string):
    for i_char in range(len(string) - 3):
        c1 = string[i_char]
        c2 = string[i_char+1]
        c3 = string[i_char+2]
        c4 = string[i_char+3]
        if c1 == c4 and c2 == c3 and c1 != c2:
            return True
    return False

def get_abas(string):
    abas = []
    for i_char in range(len(string) - 2):
        c1 = string[i_char]
        c2 = string[i_char+1]
        c3 = string[i_char+2]
        if c1 == c3 and c1 != c2:
            abas.append(c1+c2+c3)
    return abas

def has_bab(string, aba):
    bab = aba[1] + aba[0] + aba[1]
    for i_char in range(len(string) - 2):
        s = string[i_char:i_char + 3]
        if s == bab:
            return True
    return False

def a(inp):

    supporters = 0
    for line in inp:
        supports_tls = False
        open_brackets = [i for i in range(len(line)) if line[i]  == '[']
        close_brackets = [i for i in range(len(line)) if line[i]  == ']']

        if has_abba(line[:open_brackets[0]]):
            supports_tls = True
        for i in range(len(open_brackets) - 1):
            if has_abba(line[close_brackets[i]+1:open_brackets[i+1]]):
                supports_tls = True

        if has_abba(line[close_brackets[-1]+1:]):
            supports_tls = True

        for i in range(len(open_brackets)):
            if has_abba(line[open_brackets[i]+1:close_brackets[i]]):
                supports_tls = False

        if supports_tls:
            supporters += 1

    return supporters

def b(inp):
    supporters = 0
    for line in inp:
        supports_ssl = False
        open_brackets = [i for i in range(len(line)) if line[i]  == '[']
        close_brackets = [i for i in range(len(line)) if line[i]  == ']']

        abas = get_abas(line[:open_brackets[0]])
        for i in range(len(open_brackets) - 1):
            for aba in get_abas(line[close_brackets[i]+1:open_brackets[i+1]]):
                abas.append(aba)
        for aba in get_abas(line[close_brackets[-1]+1:]):
            abas.append(aba)
        abas = set(abas)

        for aba in abas:
            for i in range(len(open_brackets)):
                if has_bab(line[open_brackets[i]+1:close_brackets[i]], aba):
                    supports_ssl = True

        if supports_ssl:
            supporters += 1

    return supporters

def test_a():
    assert a(get_input()) == 110

def test_b():
    assert b(get_input()) == 242

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    parser.add_argument('-p', '--profile', dest='profile', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    if args.profile:
        print('\n### Profiling part 1 ###\n')
        __import__('cProfile').run('a(inp)')
        print('### Profiling part 2 ###\n')
        __import__('cProfile').run('b(inp)')
    else:
        print('a:', a(inp))
        print('b:', b(inp))
