import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    max_strength = 0
    bridges = []
    for line in inp:
        bridges.append([int(e) for e in line.split('/')])

    states_to_check = []  # end_of_bridge_piece, nr_to_match, nrs_of_used_bridges

    for i_bridge, bridge in enumerate(bridges):
        if 0 in bridge:
            if bridge[0] == 0:
                states_to_check.append({'bridge': bridge.copy(), 'nr_to_match': bridge[1],
                                        'used_bridge_indexes': [i_bridge]})
            else:
                states_to_check.append({'bridge': bridge.copy(), 'nr_to_match': bridge[0],
                                        'used_bridge_indexes': [i_bridge]})

    while len(states_to_check) > 0:
        state = states_to_check.pop(0)

        found_new_piece = False
        for i_bridge, bridge in enumerate(bridges):
            if i_bridge not in state['used_bridge_indexes'] and state['nr_to_match'] in bridge:
                found_new_piece = True
                used_bridge_indexes = state['used_bridge_indexes'].copy()
                used_bridge_indexes.append(i_bridge)
                if bridge[0] == state['nr_to_match']:
                    states_to_check.append({
                        'bridge': bridge.copy(), 'nr_to_match': bridge[1],
                        'used_bridge_indexes': used_bridge_indexes
                    })
                else:
                    states_to_check.append({
                        'bridge': bridge.copy(), 'nr_to_match': bridge[0],
                        'used_bridge_indexes': used_bridge_indexes
                    })
        if not found_new_piece:
            strength = 0
            for bridge_nr in state['used_bridge_indexes']:
                strength += bridges[bridge_nr][0] + bridges[bridge_nr][1]
            if strength > max_strength:
                max_strength = strength

    return max_strength

def b():
    inp = get_input()
    max_length = 0
    max_strength = 0
    bridges = []
    for line in inp:
        bridges.append([int(e) for e in line.split('/')])

    states_to_check = []  # end_of_bridge_piece, nr_to_match, nrs_of_used_bridges

    for i_bridge, bridge in enumerate(bridges):
        if 0 in bridge:
            if bridge[0] == 0:
                states_to_check.append({'bridge': bridge.copy(), 'nr_to_match': bridge[1],
                                        'used_bridge_indexes': [i_bridge]})
            else:
                states_to_check.append({'bridge': bridge.copy(), 'nr_to_match': bridge[0],
                                        'used_bridge_indexes': [i_bridge]})

    while len(states_to_check) > 0:
        state = states_to_check.pop(0)

        found_new_piece = False
        for i_bridge, bridge in enumerate(bridges):
            if i_bridge not in state['used_bridge_indexes'] and state['nr_to_match'] in bridge:
                found_new_piece = True
                used_bridge_indexes = state['used_bridge_indexes'].copy()
                used_bridge_indexes.append(i_bridge)
                if bridge[0] == state['nr_to_match']:
                    states_to_check.append({
                        'bridge': bridge.copy(), 'nr_to_match': bridge[1],
                        'used_bridge_indexes': used_bridge_indexes
                    })
                else:
                    states_to_check.append({
                        'bridge': bridge.copy(), 'nr_to_match': bridge[0],
                        'used_bridge_indexes': used_bridge_indexes
                    })
        if not found_new_piece:
            strength = 0
            length = len(state['used_bridge_indexes'])
            for bridge_nr in state['used_bridge_indexes']:
                strength += bridges[bridge_nr][0] + bridges[bridge_nr][1]
            if length > max_length:
                max_length = length
                max_strength = strength
            elif length == max_length:
                if strength > max_strength:
                    max_strength = strength

    return max_strength


def test_a():
    assert a() == 2006

def test_b():
    assert b() == 1994

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
