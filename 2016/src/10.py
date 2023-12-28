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

class Bot:
    def __init__(self, nr, important_comparison):
        self.nr = nr
        self.low = -1
        self.high = -1
        self.high_goes_to = ('', '')
        self.low_goes_to = ('', '')
        self.important_comparison = important_comparison
        self.did_important_comparison = False

    def assign_value(self, value):
        if self.low == -1 and self.high == -1:
            self.low = value
        elif self.low == -1:
            if value < self.high:
                self.low = value
            else:
                self.low = self.high
                self.high = value
        elif self.high == -1:
            if value > self.low:
                self.high = value
            else:
                self.high = self.low
                self.low = value

    def set_recipients(self, low_recipient, high_recipient):
        self.low_goes_to = low_recipient
        self.high_goes_to = high_recipient

    def pop_values(self):
        if self.low in self.important_comparison and self.high in self.important_comparison:
            self.did_important_comparison = True

        low = self.low
        high = self.high
        self.low = -1
        self.high = -1
        return low, high

    def has_two_values(self):
        if self.low != -1 and self.high != -1:
            return True
        return False

    def __str__(self):
        if self.low != -1 and self.high != -1:
            return '{}: [{}, {}] low -> {} {}, high -> {} {}'.format(
                self.nr, self.low, self.high, self.low_goes_to[0],
                self.low_goes_to[1], self.high_goes_to[0],
                self.high_goes_to[1]
            )
        elif self.low != -1:
            return '{}: [{}] low -> {} {}, high -> {} {}'.format(
                self.nr, self.low, self.low_goes_to[0], self.low_goes_to[1],
                self.high_goes_to[0], self.high_goes_to[1]
            )
        elif self.high != -1:
            return '{}: [{}] low -> {} {}, high -> {} {}'.format(
                self.nr, self.high, self.low_goes_to[0], self.low_goes_to[1],
                self.high_goes_to[0], self.high_goes_to[1]
            )
        else:
            return '{}: [] low -> {} {}, high -> {} {}'.format(
                self.nr, self.low_goes_to[0], self.low_goes_to[1],
                self.high_goes_to[0], self.high_goes_to[1]
            )

def a(inp, is_test):
    if is_test:
        important_comparison = [5, 2]
    else:
        important_comparison = [61, 17]
    bots = {}
    bots_to_do_things = []
    for line in inp:
        words = line.split()
        if words[0] == 'value':
            if words[5] not in bots:
                bots[words[5]] = Bot(words[5], important_comparison)
            bots[words[5]].assign_value(int(words[1]))

            if bots[words[5]].has_two_values():
                bots_to_do_things.append(words[5])

        elif words[0] == 'bot':
            if words[1] not in bots:
                bots[words[1]] = Bot(words[1], important_comparison)
            bots[words[1]].set_recipients((words[5], words[6]), (words[10], words[11]))

    while bots_to_do_things:
        bot_to_do_things = bots_to_do_things.pop(0)

        low_recipient = bots[bot_to_do_things].low_goes_to
        high_recipient = bots[bot_to_do_things].high_goes_to
        low, high = bots[bot_to_do_things].pop_values()
        if low_recipient[0] == 'bot':
            bots[low_recipient[1]].assign_value(low)
            if bots[low_recipient[1]].has_two_values():
                bots_to_do_things.append(low_recipient[1])
        if high_recipient[0] == 'bot':
            bots[high_recipient[1]].assign_value(high)
            if bots[high_recipient[1]].has_two_values():
                bots_to_do_things.append(high_recipient[1])
        if bots[bot_to_do_things].did_important_comparison:
            return bot_to_do_things
    return 0

def b(inp, is_test):
    if is_test:
        important_comparison = [5, 2]
    else:
        important_comparison = [61, 17]
    bots = {}
    outputs = {}
    bots_to_do_things = []
    for line in inp:
        words = line.split()
        if words[0] == 'value':
            if words[5] not in bots:
                bots[words[5]] = Bot(words[5], important_comparison)
            bots[words[5]].assign_value(int(words[1]))

            if bots[words[5]].has_two_values():
                bots_to_do_things.append(words[5])

        elif words[0] == 'bot':
            if words[1] not in bots:
                bots[words[1]] = Bot(words[1], important_comparison)
            bots[words[1]].set_recipients((words[5], words[6]), (words[10], words[11]))

    while bots_to_do_things:
        bot_to_do_things = bots_to_do_things.pop(0)

        low_recipient = bots[bot_to_do_things].low_goes_to
        high_recipient = bots[bot_to_do_things].high_goes_to
        low, high = bots[bot_to_do_things].pop_values()
        if low_recipient[0] == 'bot':
            bots[low_recipient[1]].assign_value(low)
            if bots[low_recipient[1]].has_two_values():
                bots_to_do_things.append(low_recipient[1])
        else:
            outputs[low_recipient[1]] = low
        if high_recipient[0] == 'bot':
            bots[high_recipient[1]].assign_value(high)
            if bots[high_recipient[1]].has_two_values():
                bots_to_do_things.append(high_recipient[1])
        else:
            outputs[high_recipient[1]] = high

    return outputs['0'] * outputs['1'] * outputs['2']

def test_a():
    assert a(get_input(), is_test=False) == '101'

def test_b():
    assert b(get_input(), is_test=False) == 37789

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
        print('a:', a(inp, args.test))
        print('b:', b(inp, args.test))
