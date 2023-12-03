import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    last_played = 0
    regs = {}
    for line in inp:
        words = line.split()
        if words[1] not in regs.keys():
            regs[words[1]] = 0

    i_line = 0
    while True:
        offset = 1
        words = inp[i_line].split()
        if words[0] == 'snd':
            last_played = regs[words[1]]
        elif words[0] == 'set':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] = int(words[2])
            else:
                regs[words[1]] = regs[words[2]]
        elif words[0] == 'add':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] += int(words[2])
            else:
                regs[words[1]] += regs[words[2]]
        elif words[0] == 'mul':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] *= int(words[2])
            else:
                regs[words[1]] *= regs[words[2]]
        elif words[0] == 'mod':
            if words[2].removeprefix('-').isdigit():
                regs[words[1]] %= int(words[2])
            else:
                regs[words[1]] %= regs[words[2]]
        elif words[0] == 'jgz' and regs[words[1]] > 0:
            if words[2].removeprefix('-').isdigit():
                offset = int(words[2])
            else:
                offset = regs[words[2]]
        elif words[0] == 'rcv' and regs[words[1]] > 0:
            return last_played
        i_line += offset

class Program:
    def __init__(self, commands, p_init_val):
        self.id = p_init_val
        self.i_command = 0
        self.commands = commands
        self.regs = {}
        self.send_value = None
        self.message_queue = []
        self.turns_waiting_to_rcv = 0
        self.sends = 0
        for line in commands:
            words = line.split()
            if words[1] not in self.regs.keys() and not words[1].isdigit():
                self.regs[words[1]] = 0
        self.regs['p'] = p_init_val

    def execute(self):

        command = self.commands[self.i_command]
        words = command.split()
        offset = 1
        if words[0] == 'snd':
            if words[1].removeprefix('-').isdigit():
                self.send_value = int(words[1])
            else:
                self.send_value = self.regs[words[1]]
        elif words[0] == 'set':
            if words[2].removeprefix('-').isdigit():
                self.regs[words[1]] = int(words[2])
            else:
                self.regs[words[1]] = self.regs[words[2]]
        elif words[0] == 'add':
            if words[2].removeprefix('-').isdigit():
                self.regs[words[1]] += int(words[2])
            else:
                self.regs[words[1]] += self.regs[words[2]]
        elif words[0] == 'mul':
            if words[2].removeprefix('-').isdigit():
                self.regs[words[1]] *= int(words[2])
            else:
                self.regs[words[1]] *= self.regs[words[2]]
        elif words[0] == 'mod':
            if words[2].removeprefix('-').isdigit():
                self.regs[words[1]] %= int(words[2])
            else:
                self.regs[words[1]] %= self.regs[words[2]]
        elif words[0] == 'jgz':
            if (words[1].isdigit() and int(words[1]) > 0) or self.regs[words[1]] > 0:
                if words[2].removeprefix('-').isdigit():
                    offset = int(words[2])
                else:
                    offset = self.regs[words[2]]
        elif words[0] == 'rcv':
            if self.message_queue:
                self.regs[words[1]] = self.message_queue.pop(0)
                self.turns_waiting_to_rcv = 0
            else:
                self.turns_waiting_to_rcv += 1
                offset = 0

        self.i_command += offset

    def can_send(self):
        if self.send_value is not None:
            return True
        return False

    def send(self):
        out = self.send_value
        self.send_value = None
        self.sends += 1
        return out

    def receive(self, value):
        self.message_queue.append(value)

def b():
    inp = get_input()
    program_0 = Program(inp, 0)
    program_1 = Program(inp, 1)

    while True:
        program_0.execute()
        program_1.execute()

        if program_0.can_send():
            program_1.receive(program_0.send())
        if program_1.can_send():
            program_0.receive(program_1.send())

        if program_1.turns_waiting_to_rcv > 2 and program_0.turns_waiting_to_rcv > 2:
            return program_1.sends

def test_a():
    assert a() == 8600

def test_b():
    assert b() == 7239

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
