import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr + '_test')
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_group_members_for_nr(
    connections: dict[str, set[str]], nr: str, group_members: set[str]
) -> set[str]:

    for neighbour in connections[nr]:
        if neighbour not in group_members:
            group_members.add(neighbour)
            new_members = get_group_members_for_nr(connections, neighbour, group_members)
            for m in new_members:
                group_members.add(m)

    return group_members


def a():
    inp = get_input()
    connections = {}
    for line in inp:
        words = line.split(' ')
        if words[0] not in connections.keys():
            connections[words[0]] = set()
        for word in words[2:]:
            if not words[0] == word:
                connections[words[0]].add(word.removesuffix(','))

    group_members = get_group_members_for_nr(connections, '0', set())
    return len(group_members)

def b():
    inp = get_input()
    connections = {}
    for line in inp:
        words = line.split(' ')
        if words[0] not in connections.keys():
            connections[words[0]] = set()
        for word in words[2:]:
            if not words[0] == word:
                connections[words[0]].add(word.removesuffix(','))

    n_groups = 0
    accounted_for_nrs = set()
    for nr in connections.keys():
        if nr not in accounted_for_nrs:
            group_members = get_group_members_for_nr(connections, nr, set())
            for m in group_members:
                accounted_for_nrs.add(m)
            n_groups += 1

    return n_groups

def test_a():
    assert a() == 152

def test_b():
    assert b() == 186

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
