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

def insert_state_a(state_list, old_state, direction, heat_loss, poses_checked):
    #print('before:', state_list)
    pos, prev_positions, straight_tiles_travelled, dist = old_state

    if direction == pos[2] and straight_tiles_travelled == 3:
        return state_list, poses_checked

    if direction == 'east':
        new_pos = (pos[0], pos[1] + 1, 'east')
    elif direction == 'west':
        new_pos = (pos[0], pos[1] - 1, 'west')
    elif direction == 'north':
        new_pos = (pos[0] - 1, pos[1], 'north')
    else:
        new_pos = (pos[0] + 1, pos[1], 'south')

    if not (0 <= new_pos[0] < len(heat_loss)) or not (0 <= new_pos[1] < len(heat_loss[0])):
        return state_list, poses_checked

    if direction == pos[2]:
        new_straight_line_tiles = straight_tiles_travelled + 1
    else:
        new_straight_line_tiles = 1

    new_pose = new_pos + (new_straight_line_tiles,)
    if new_pose in poses_checked:
        return state_list, poses_checked

    new_prev_pos = prev_positions.copy()
    new_prev_pos.append((pos[0], pos[1]))
    new_dist = dist + heat_loss[new_pos[0]][new_pos[1]]
    new_state = (new_pos, new_prev_pos, new_straight_line_tiles, new_dist)
    bisect.insort(state_list, new_state, key=lambda e: e[3])

    poses_checked.add(new_pose)
    #print('after :', state_list)

    return state_list, poses_checked

def insert_state_b(state_list, old_state, direction, heat_loss, poses_checked):
    pose, prev_positions, dist = old_state

    if (direction != pose[2] and pose[3] < 4) or (direction == pose[2] and pose[3] >= 10):
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

    new_prev_pos = prev_positions.copy()
    new_prev_pos.append(new_pose)
    new_dist = dist + heat_loss[new_pose[0]][new_pose[1]]
    new_state = (new_pose, new_prev_pos, new_dist)
    bisect.insort(state_list, new_state, key=lambda e: e[2])

    poses_checked.add(new_pose)

    return state_list, poses_checked

def a(inp):
    heat_loss = []
    for row in range(len(inp)):
        heat_loss.append([])
        for col in range(len(inp[0])):
            heat_loss[row].append(int(inp[row][col]))

    states_to_check = []
    # 0: current pose, 1: visited_positions, 2: tiles_travelled_in_straight_line, 3: distance_travelled
    states_to_check.append([(0, 0, 'east'), [], 0, 0])
    states_to_check.append([(0, 0, 'south'), [], 0, 0])
    poses_checked = set()  # tuple with 0 -> 2 being pos, and 3 being straight_tiles_travelled
    poses_checked.add((0, 0, 'east', 0))

    while states_to_check:
        state = states_to_check.pop(0)
        if (state[0][0], state[0][1]) == (len(inp)-1, len(inp[0])-1):
            return state[3]

        if state[0][2] == 'east':
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
        elif state[0][2] == 'north':
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
        elif state[0][2] == 'west':
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
        elif state[0][2] == 'south':
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_a(
                states_to_check, state, 'west', heat_loss, poses_checked
            )

    return 0

def pprint(state, heat_loss):
    for row in range(len(heat_loss)):
        string = ''
        for col in range(len(heat_loss[0])):
            been_here = False
            for pos in state[1]:
                if pos[0] == row and pos[1] == col:
                    if pos[2] == 'north': string += '^'
                    elif pos[2] == 'south': string += 'v'
                    elif pos[2] == 'east': string += '>'
                    elif pos[2] == 'west': string += '<'
                    been_here = True
            if not been_here:
                string += str(heat_loss[row][col])
        print(string)

def b(inp):
    heat_loss = []
    for row in range(len(inp)):
        heat_loss.append([])
        for col in range(len(inp[0])):
            heat_loss[row].append(int(inp[row][col]))

    states_to_check = []
    # 0: current pose (x, y, dir, straight_steps_taken), 1: visited_positions
    # 3: distance_travelled
    states_to_check.append([(0, 0, 'east', 0), [], 0])
    states_to_check.append([(0, 0, 'south', 0), [], 0])
    poses_checked = set()  # tuple with all poses considered

    while states_to_check:
        state = states_to_check.pop(0)
        if (state[0][0], state[0][1]) == (len(inp)-1, len(inp[0])-1):
            if state[2] < 4:
                continue
            else:
                return state[2]

        if state[0][2] == 'east':
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
        elif state[0][2] == 'north':
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
        elif state[0][2] == 'west':
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'west', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'north', heat_loss, poses_checked
            )
        elif state[0][2] == 'south':
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'east', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'south', heat_loss, poses_checked
            )
            states_to_check, poses_checked = insert_state_b(
                states_to_check, state, 'west', heat_loss, poses_checked
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
