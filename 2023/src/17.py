import argparse
import bisect
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def insert_state(state_list, old_state, direction, heat_loss, poses_checked, is_ultra=False):
    pose, dist = old_state

    if is_ultra:
        if (direction != pose[2] and pose[3] < 4) or (direction == pose[2] and pose[3] == 10):
            return state_list, poses_checked
    else:
        if direction == pose[2] and pose[3] == 3:
            return state_list, poses_checked

    if direction == pose[2]:
        straight_dist_travelled = pose[3] + 1
    else:
        straight_dist_travelled = 1

    if direction == 'east':
        new_pose = (pose[0], pose[1] + 1, 'east', straight_dist_travelled)
    elif direction == 'west':
        new_pose = (pose[0], pose[1] - 1, 'west', straight_dist_travelled)
    elif direction == 'north':
        new_pose = (pose[0] - 1, pose[1], 'north', straight_dist_travelled)
    else:
        new_pose = (pose[0] + 1, pose[1], 'south', straight_dist_travelled)

    if not (0 <= new_pose[0] < len(heat_loss)) or not (0 <= new_pose[1] < len(heat_loss[0])):
        return state_list, poses_checked

    if new_pose in poses_checked:
        return state_list, poses_checked

    new_dist = dist + heat_loss[new_pose[0]][new_pose[1]]
    new_state = (new_pose, new_dist)
    bisect.insort(state_list, new_state, key=lambda e: e[1])

    poses_checked.add(new_pose)

    return state_list, poses_checked

def a(inp):
    heat_loss = []
    for row in range(len(inp)):
        heat_loss.append([])
        for col in range(len(inp[0])):
            heat_loss[row].append(int(inp[row][col]))

    states_to_check = []
    # 0: current pose (x, y, dir, straight_steps_taken)
    # 1: distance_travelled
    states_to_check.append([(0, 0, 'east', 0), 0])
    states_to_check.append([(0, 0, 'south', 0), 0])
    poses_checked = set()

    while states_to_check:
        state = states_to_check.pop(0)
        if (state[0][0], state[0][1]) == (len(inp)-1, len(inp[0])-1):
            return state[1]

        if state[0][2] == 'east':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
        elif state[0][2] == 'north':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
        elif state[0][2] == 'west':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
        elif state[0][2] == 'south':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked
            )

    return 0

def b(inp):
    heat_loss = []
    for row in range(len(inp)):
        heat_loss.append([])
        for col in range(len(inp[0])):
            heat_loss[row].append(int(inp[row][col]))

    states_to_check = []
    # 0: current pose (x, y, dir, straight_steps_taken)
    # 1: distance_travelled
    states_to_check.append([(0, 0, 'east', 0), 0])
    states_to_check.append([(0, 0, 'south', 0), 0])
    poses_checked = set()

    while states_to_check:
        state = states_to_check.pop(0)
        if (state[0][0], state[0][1]) == (len(inp)-1, len(inp[0])-1):
            if state[0][3] < 4:
                continue
            else:
                return state[1]

        if state[0][2] == 'east':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked, is_ultra=True
            )
        elif state[0][2] == 'north':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked, is_ultra=True
            )
        elif state[0][2] == 'west':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'north', heat_loss, poses_checked, is_ultra=True
            )
        elif state[0][2] == 'south':
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'east', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'south', heat_loss, poses_checked, is_ultra=True
            )
            states_to_check, poses_checked = insert_state(
                states_to_check, state, 'west', heat_loss, poses_checked, is_ultra=True
            )

def test_a():
    assert a(get_input()) == 851

def test_b():
    assert b(get_input()) == 982

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))
