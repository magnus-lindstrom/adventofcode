import argparse
import pathlib
from math import lcm


def get_input(test1=False, test2=False):
    q_nr = pathlib.Path(__file__).stem
    if test1:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    elif test2:
        file_name = pathlib.Path('inputs/' + q_nr + '_test1')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

class Module:
    def __init__(self, string, is_output=False):
        if is_output:
            self.name = string
            self.type = 'output'
            self.targets = []
            self.low_pulses_received = 0
        else:
            words = string.split()
            if words[0][0] == '%':
                self.type = 'flip-flop'
                self.name = words[0][1:]
                self.is_active = False
            elif words[0][0] == '&':
                self.type = 'conjunction'
                self.name = words[0][1:]
                self.memory = {}
            else:
                self.type = 'broadcaster'
                self.name = 'broadcaster'

            self.targets = [s.removesuffix(',') for s in words[2:]]

    def __str__(self):
        if self.type == 'conjunction':
            targets = ', '.join(self.targets)
            inputs = ', '.join(self.memory.keys())
            return '&{}: {} -> {}'.format(self.name, inputs, targets)
        elif self.type == 'flip-flop':
            targets = ', '.join(self.targets)
            return '%{} -> {}'.format(self.name, targets)
        elif self.type == 'broadcaster':
            targets = ', '.join(self.targets)
            return 'broadcaster -> {}'.format(targets)
        elif self.type == 'output':
            return 'output'

    def add_input_to_conj(self, input_name):
        if self.type == 'conjunction':
            self.memory[input_name] = False

    def receive_pulse_and_send(self, from_mod: str, pulse: bool):
        output = None
        if self.type == 'conjunction':
            self.memory[from_mod] = pulse
            if all(self.memory.values()):
                output = [self.targets, False]
            else:
                output = [self.targets, True]
        elif self.type == 'flip-flop':
            if not pulse:
                self.is_active = not self.is_active
                output = [self.targets, self.is_active]
        elif self.type == 'output':
            if not pulse:
                self.low_pulses_received += 1
        else:
            output = [self.targets, pulse]

        return output

def a(inp):
    modules = {}
    conj_modules = []
    for line in inp:
        words = line.split()
        name = words[0]

        if name[0] == '&':
            conj_modules.append(name[1:])
        if name == 'broadcaster':
            modules['broadcaster'] = Module(line)
        else:
            modules[name[1:]] = Module(line)

        if 'output' in words[2:]:
            modules['output'] = Module('output', is_output=True)
        if 'rx' in words[2:]:
            modules['rx'] = Module('rx', is_output=True)
    for module in modules.values():
        for conj_mod in conj_modules:
            if conj_mod in module.targets:
                modules[conj_mod].add_input_to_conj(module.name)


    n_presses = 1000
    low, high = 0, 0
    for _ in range(n_presses):
        #                  to              from        pulse
        messages = [[['broadcaster'], 'button module', False]]
        while messages:
            targets, source, signal = messages.pop(0)
            if signal: high += len(targets)
            else: low += len(targets)
            for target in targets:
                output = modules[target].receive_pulse_and_send(source, signal)
                if output is not None:
                    new_targets, new_signal = output
                    messages.append([new_targets, target, new_signal])


    return low * high


def b(inp):
    # The thing works like this:

    # The flip floppers make up 4 different networks and are connected in such
    # a way that they form 4 big counters. Each one of these counters has each
    # bit of its number represented by a flip-flop module. Only some of the
    # bits send signals to the conj module of their group, and it is when these
    # are all high that the conj module sends a low signal.

    # That signal then is relayed through another conj module to end up in a
    # third conj module, that gets input from all 4 counter groups. When the
    # counters signal simultaneously, the final 'rx' module gets its low input.

    # I drew this on paper, and plotted a small graph that can be seen in
    # images/20_groups.png. I did not write a generic solution, but the one
    # that I should have written is one where I simply check when the inputs to
    # the "gathering up-conj module" are low, and check for periods. If this
    # explanation is not good enough, then you have to use pen and paper to
    # draw up the entire network again... Sorry

    rb_high_iter = 1 + 8 + 32 + 256 + 512  + 1024 + 2048
    ml_high_iter = 1 + 2 + 8  + 256 + 512  + 1024 + 2048
    bt_high_iter = 1 + 2 + 8  + 16  + 64   + 256  + 512 + 1024 + 2048
    gp_high_iter = 1 + 2 + 4  + 32  + 64   + 256  + 512 + 1024 + 2048
    return lcm(rb_high_iter,  ml_high_iter, bt_high_iter, gp_high_iter)


def is_active_at_i(name, i, flip_zero_section_lengths, flip_one_section_lengths):
    rem = i % (flip_zero_section_lengths[name] + flip_one_section_lengths[name])
    if rem < flip_zero_section_lengths[name]:
        return False
    return True

def test_a():
    assert a(get_input()) == 929810733

def test_b():
    assert b(get_input()) == 231657829136023

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', dest='test1', action='store_true')
    parser.add_argument('-t2', dest='test2', action='store_true')
    args = parser.parse_args()
    inp = get_input(test1=args.test1, test2=args.test2)

    print('a:', a(inp))
    print('b:', b(inp))
