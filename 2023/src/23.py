import argparse
import pathlib
from collections import defaultdict

import drawing


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    walls = set()
    slopes = {}
    for i_line, line in enumerate(inp):
        for i_char, char in enumerate(line):
            if char == '#':
                walls.add((i_line, i_char))
            elif char in ['>', '<', 'v', '^']:
                slopes[(i_line, i_char)] = char


    final_tile = (len(inp) - 1, len(inp) - 2)
    going_to_directions = ['west', 'east', 'north', 'south']
    coming_from_directions = ['east', 'west', 'south', 'north']

    # row, col, last_junction, junctions_visited, came_from, steps taken since last junction, is_one_way
    state_queue = []
    junctions_visited = set()
    junctions_visited.add((0, 1))
    state_queue.append((1, 1, (0, 1), junctions_visited, 'north', 1, False))
    connections = {}
    connections[(0, 1)] = {}

    while state_queue:
        row, col, last_junction, junctions_visited, came_from, steps_since_junction, is_one_way = state_queue.pop()  # from the back

        new_tiles = [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]
        possible_paths = []
        would_be_one_way = []
        for i_path, (new_tile, going_to) in enumerate(zip(new_tiles, going_to_directions)):
            if not came_from == going_to:
                if not new_tile in walls:
                    if new_tile in slopes.keys():
                        if going_to == 'east' and slopes[new_tile] == '>':
                            would_be_one_way.append(True)
                            possible_paths.append(i_path)
                        elif going_to == 'west' and slopes[new_tile] == '<':
                            would_be_one_way.append(True)
                            possible_paths.append(i_path)
                        elif going_to == 'north' and slopes[new_tile] == '^':
                            would_be_one_way.append(True)
                            possible_paths.append(i_path)
                        elif going_to == 'south' and slopes[new_tile] == 'v':
                            would_be_one_way.append(True)
                            possible_paths.append(i_path)
                    else:
                        would_be_one_way.append(False)
                        possible_paths.append(i_path)
        if len(possible_paths) == 1:
            if new_tiles[possible_paths[0]] == final_tile:
                connections[last_junction][final_tile] = steps_since_junction + 1

            else:  # is not goal tile
                new_state = [
                    new_tiles[possible_paths[0]][0],
                    new_tiles[possible_paths[0]][1],
                    last_junction,
                    junctions_visited,
                    coming_from_directions[possible_paths[0]],
                    steps_since_junction + 1,
                    is_one_way or would_be_one_way[0]
                ]
                state_queue.append(new_state)
        elif len(possible_paths) > 1:
            this_junction = (row, col)
            if this_junction in junctions_visited:
                continue
            new_junctions_visited = junctions_visited.copy()
            new_junctions_visited.add(this_junction)
            connections[last_junction][this_junction] = steps_since_junction

            if not is_one_way:
                connections = {this_junction: steps_since_junction}
            else:
                connections[this_junction] = {}
            for ip, one_way in zip(possible_paths, would_be_one_way):
                new_state = [
                    new_tiles[ip][0],
                    new_tiles[ip][1],
                    this_junction,
                    junctions_visited,
                    coming_from_directions[ip],
                    1,
                    one_way
                ]
                state_queue.append(new_state)

    state_queue = []
    # current_junction, previous_junctions, steps_taken
    state_queue.append([(0, 1), [], 0])
    max_steps = 0

    while state_queue:
        current_junction, previous_junctions, steps_taken = state_queue.pop()
        for possible_junction, steps in connections[current_junction].items():
            if possible_junction not in previous_junctions:
                if possible_junction == final_tile:
                    final_steps = steps_taken + steps
                    if final_steps > max_steps:
                        max_steps = final_steps

                else:
                    new_previous_junctions = previous_junctions.copy()
                    new_previous_junctions.append(current_junction)
                    new_state = [possible_junction, new_previous_junctions, steps_taken + steps]
                    state_queue.append(new_state)

    return max_steps

def b(inp):
    walls = set()
    for i_line, line in enumerate(inp):
        for i_char, char in enumerate(line):
            if char == '#':
                walls.add((i_line, i_char))

    final_tile = (len(inp) - 1, len(inp) - 2)
    final_tile_id = -1
    going_to_directions = ['west', 'east', 'north', 'south']
    coming_from_directions = ['east', 'west', 'south', 'north']

    # in index i, you find the connections between junction i and other indexes
    # ix given in [(i1, steps), (i2, steps)..]
    connections = []
    connections.append([])
    junction_to_id = {(0, 1): 0}

    state_queue = []
    # row, col, last_junction_id, came_from, steps taken since last junction
    state_queue.append((1, 1, 0, 'north', 1))

    while state_queue:
        row, col, last_junction_id, came_from, steps_since_junction = state_queue.pop()  # from the back

        new_tiles = [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]
        possible_paths = []
        for i_path, (new_tile, going_to) in enumerate(zip(new_tiles, going_to_directions)):
            if not came_from == going_to:
                if not new_tile in walls:
                    possible_paths.append(i_path)

        if len(possible_paths) == 1:
            if new_tiles[possible_paths[0]] == final_tile:
                if final_tile not in junction_to_id:
                    final_tile_id = len(junction_to_id)
                    junction_to_id[new_tiles[possible_paths[0]]] = final_tile_id
                    connections.append([(
                        last_junction_id, steps_since_junction + 1
                    )])

                connections[last_junction_id].append((
                    final_tile_id, steps_since_junction + 1
                ))

            else:
                new_state = [
                    new_tiles[possible_paths[0]][0],
                    new_tiles[possible_paths[0]][1],
                    last_junction_id,
                    coming_from_directions[possible_paths[0]],
                    steps_since_junction + 1,
                ]
                state_queue.append(new_state)
        elif len(possible_paths) > 1:
            this_junction = (row, col)
            if this_junction in junction_to_id:
                # if the coordinates of a junction is in junction_to_id, we have visited it
                # add a connection from the last junction to this (the
                # connection from this to the last junction is taken care of in
                # another state, since we have apparently already been to this
                # junction)
                connections[last_junction_id].append((
                    junction_to_id[this_junction], steps_since_junction
                ))
                continue
            else:
                this_junction_id = len(junction_to_id)
                junction_to_id[this_junction] = this_junction_id
                connections[last_junction_id].append((
                    this_junction_id, steps_since_junction
                ))

            connections.append([(last_junction_id, steps_since_junction)])

            for ip in possible_paths:
                new_state = [
                    new_tiles[ip][0],
                    new_tiles[ip][1],
                    this_junction_id,
                    coming_from_directions[ip],
                    1,
                ]
                state_queue.append(new_state)
    print(connections)

    been = {j: False for j in range(len(junction_to_id))}

    return max_steps_rec(0, been, 0, connections, final_tile_id)

def max_steps_rec(junction, been, steps_taken, connections, final_tile):
    if junction == final_tile:
        return steps_taken

    max_steps = 0
    for possible_junction, steps in connections[junction]:
        if not been[possible_junction]:
            been[possible_junction] = True
            new_steps = max_steps_rec(
                possible_junction, been, steps_taken + steps, connections,
                final_tile
            )
            been[possible_junction] = False
            if new_steps > max_steps:
                max_steps = new_steps

    return max_steps

def visualise(inp):
    d = drawing.Drawer()
    #d.check_window_dimensions(inp)
    #return
    walls = set()
    for i_line, line in enumerate(inp):
        for i_char, char in enumerate(line):
            if char == '#':
                walls.add((i_line, i_char))
                d.bulk_str_add('#')
            else:
                d.bulk_str_add(' ')
        d.bulk_str_add('\n')

    d.bulk_draw(sleep_sec=1)

    final_tile = (len(inp) - 1, len(inp) - 2)
    final_tile_id = -1
    going_to_directions = ['west', 'east', 'north', 'south']
    coming_from_directions = ['east', 'west', 'south', 'north']

    # in index i, you find the connections between junction i and other indexes
    # ix given in [(i1, steps), (i2, steps)..]
    connections = []
    connections.append([])
    junction_to_id = {(0, 1): 0}
    path_between_nodes = {}

    state_queue = []
    # row, col, last_junction_id, came_from, steps_taken_since_last_junction, path_taken
    state_queue.append((1, 1, 0, 'north', 1, [(0, 1), (1, 1)]))

    while state_queue:
        row, col, last_junction_id, came_from, steps_since_junction, path_taken = state_queue.pop()

        new_tiles = [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]
        possible_paths = []
        for i_path, (new_tile, going_to) in enumerate(zip(new_tiles, going_to_directions)):
            if not came_from == going_to:
                if not new_tile in walls:
                    possible_paths.append(i_path)

        if len(possible_paths) == 1:
            if new_tiles[possible_paths[0]] == final_tile:
                if final_tile not in junction_to_id:
                    final_tile_id = len(junction_to_id)
                    junction_to_id[new_tiles[possible_paths[0]]] = final_tile_id
                    connections.append([(
                        last_junction_id, steps_since_junction + 1
                    )])

                connections[last_junction_id].append((
                    final_tile_id, steps_since_junction + 1
                ))
                path_between_nodes[last_junction_id] = {final_tile_id: path_taken}

            else:
                new_path_taken = path_taken.copy()
                new_path_taken.append((new_tiles[possible_paths[0]][0], new_tiles[possible_paths[0]][1]))
                new_state = [
                    new_tiles[possible_paths[0]][0],
                    new_tiles[possible_paths[0]][1],
                    last_junction_id,
                    coming_from_directions[possible_paths[0]],
                    steps_since_junction + 1,
                    new_path_taken
                ]
                state_queue.append(new_state)
        elif len(possible_paths) > 1:
            this_junction = (row, col)
            if this_junction in junction_to_id:
                # if the coordinates of a junction is in junction_to_id, we have visited it
                # add a connection from the last junction to this (the
                # connection from this to the last junction is taken care of in
                # another state, since we have apparently already been to this
                # junction)
                connections[last_junction_id].append((
                    junction_to_id[this_junction], steps_since_junction
                ))

                path_between_nodes[last_junction_id][junction_to_id[this_junction]] = path_taken
                continue
            else:
                this_junction_id = len(junction_to_id)
                junction_to_id[this_junction] = this_junction_id
                connections[last_junction_id].append((
                    this_junction_id, steps_since_junction
                ))
                path_between_nodes[last_junction_id] = {junction_to_id[this_junction]: path_taken}
                path_between_nodes[this_junction_id] = {}

            connections.append([(last_junction_id, steps_since_junction)])

            for ip in possible_paths:
                new_state = [
                    new_tiles[ip][0],
                    new_tiles[ip][1],
                    this_junction_id,
                    coming_from_directions[ip],
                    1,
                    [(new_tiles[ip][0], new_tiles[ip][1])],
                ]
                state_queue.append(new_state)

    for x, y in junction_to_id.keys():
        d.char_list_push('X', x, y)
    d.char_list_draw(sleep_sec=0.5)

    been = {j: False for j in range(len(junction_to_id))}

    max_steps, nodes_traversed = max_steps_rec_for_drawing(0, been, 0, connections, final_tile_id)
    d.draw_str('Longest path is {} steps.'. format(max_steps), row=len(inp) + 4)
    for i_junk in range(len(nodes_traversed[:-1])):
        node1 = nodes_traversed[i_junk]
        node2 = nodes_traversed[i_junk + 1]
        for node in path_between_nodes[node1][node2]:
            d.char_list_push('O', node[0], node[1])
    d.char_list_draw(sleep_sec_total=5)
    d.wait_for_keypress()


def max_steps_rec_for_drawing(junction, been, steps_taken, connections, final_tile):

    if junction == final_tile:
        return steps_taken, [junction]

    max_steps = 0
    max_step_nodes = []
    for possible_junction, steps in connections[junction]:
        if not been[possible_junction]:
            been[possible_junction] = True
            new_steps, nodes_traversed = max_steps_rec_for_drawing(
                possible_junction, been, steps_taken + steps, connections,
                final_tile
            )
            been[possible_junction] = False
            if new_steps > max_steps:
                max_step_nodes = nodes_traversed.copy()
                max_step_nodes.insert(0, junction)
                max_steps = new_steps

    return max_steps, max_step_nodes


def test_a():
    assert a(get_input()) == 2394

def test_b():
    assert b(get_input()) == 6554

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    parser.add_argument('-p', '--profile', dest='profile', action='store_true')
    parser.add_argument('-v', '--visualise', dest='visualise', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    if args.profile:
        print('\n### Profiling part 1 ###\n')
        __import__('cProfile').run('a(inp)')
        print('### Profiling part 2 ###\n')
        __import__('cProfile').run('b(inp)')
    elif args.visualise:
        visualise(inp)
    else:
        print('a:', a(inp))
        print('b:', b(inp))
