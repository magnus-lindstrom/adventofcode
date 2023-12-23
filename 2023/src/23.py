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
    #for row in range(len(inp)):
    #    for col in range(len(inp[0])):
    #        if (row, col) in walls:
    #            print('#', end='')
    #        else:
    #            print('.', end='')
    #    print()
    #print()


    final_tile = (len(inp) - 1, len(inp) - 2)
    going_to_directions = ['west', 'east', 'north', 'south']
    coming_from_directions = ['east', 'west', 'south', 'north']

    # row, col, last_junction, junctions_visited, came_from, steps taken since last junction, is_one_way
    state_queue = []
    junctions_visited = set()
    junctions_visited.add((0, 1))
    state_queue.append((1, 1, (0, 1), 'north', 1))
    connections = {}
    connections[(0, 1)] = {}

    while state_queue:
        row, col, last_junction, came_from, steps_since_junction = state_queue.pop()  # from the back

        new_tiles = [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]
        possible_paths = []
        for i_path, (new_tile, going_to) in enumerate(zip(new_tiles, going_to_directions)):
            if not came_from == going_to:
                if not new_tile in walls:
                    possible_paths.append(i_path)

        if len(possible_paths) == 1:
            if new_tiles[possible_paths[0]] == final_tile:
                connections[last_junction][final_tile] = steps_since_junction + 1

            else:  # is not goal tile
                new_state = [
                    new_tiles[possible_paths[0]][0],
                    new_tiles[possible_paths[0]][1],
                    last_junction,
                    coming_from_directions[possible_paths[0]],
                    steps_since_junction + 1,
                ]
                state_queue.append(new_state)
        elif len(possible_paths) > 1:
            this_junction = (row, col)
            connections[last_junction][this_junction] = steps_since_junction

            if this_junction in junctions_visited:
                continue
            else:
                junctions_visited.add(this_junction)

            connections[this_junction] = {}
            connections[this_junction][last_junction] = steps_since_junction

            for ip in possible_paths:
                new_state = [
                    new_tiles[ip][0],
                    new_tiles[ip][1],
                    this_junction,
                    coming_from_directions[ip],
                    1,
                ]
                state_queue.append(new_state)

    state_queue = []
    # current_junction, previous_junctions, steps_taken
    state_queue.append([(0, 1), [], 0])
    route = None
    max_steps = 0

    while state_queue:
        current_junction, previous_junctions, steps_taken = state_queue.pop()
        for possible_junction, steps in connections[current_junction].items():
            if possible_junction not in previous_junctions:
                if possible_junction == final_tile:
                    final_steps = steps_taken + steps
                    if final_steps > max_steps:
                        max_steps = final_steps
                        route = previous_junctions.copy()

                else:
                    new_previous_junctions = previous_junctions.copy()
                    new_previous_junctions.append(current_junction)
                    new_state = [possible_junction, new_previous_junctions, steps_taken + steps]
                    state_queue.append(new_state)

    return max_steps

def test_a():
    assert a(get_input()) == 2394

def test_b():
    assert b(get_input()) == 6554

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))
    __import__('cProfile').run('test_b()')
