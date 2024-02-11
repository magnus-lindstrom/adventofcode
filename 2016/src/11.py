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

def floor(floor_str):
    if floor_str == 'first':
        return 1
    elif floor_str == 'second':
        return 2
    elif floor_str == 'third':
        return 3
    elif floor_str == 'fourth':
        return 4
    else:
        print(floor_str)
        raise Exception

class Building:
    def __init__(self, inp):

        self.elevator = 1
        # map with 'element': ['microchip floor', 'generator floor']
        self.equipment = {}
        for line in inp:
            i_word = 6
            words = line.split()
            while i_word < len(words):
                element: str = words[i_word-1].split('-')[0]
                word: str = words[i_word].strip('.,')
                if word == 'generator':
                    if element not in self.equipment:
                        self.equipment[element] = [0, 0]
                    self.equipment[element][1] = floor(words[1])
                elif word == 'microchip':
                    if element not in self.equipment:
                        self.equipment[element] = [0, 0]
                    self.equipment[element][0] = floor(words[1])
                i_word += 1

def print_building(building):
    for floor in [4, 3, 2, 1]:
        print('F{} '.format(floor), end='')
        if building.elevator == floor:
            print('E   ', end='')
        else:
            print('.   ', end='')
        for element, fls in building.equipment.items():
            if fls[1] == floor:
                print('{}G '.format(element[:2].upper()), end='')
            else:
                print('.   ', end='')

            if fls[0] == floor:
                print('{}M '.format(element[:2].upper()), end='')
            else:
                print('.   ', end='')
        print()

def a(inp, is_test):
    if is_test:
        pass

    building = Building(inp)
    print_building(building)

    return 0

def b(inp, is_test):
    if is_test:
        pass

    return 0

def test_a():
    assert a(get_input(), is_test=False) == 0

def test_b():
    assert b(get_input(), is_test=False) == 0

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
        print('a:', a(inp, is_test=args.test))
        print('b:', b(inp, is_test=args.test))
