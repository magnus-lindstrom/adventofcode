import argparse
import cProfile
import pathlib
from copy import deepcopy


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a(inp):
    bricks = []
    brick_space = {}
    for i_line, line in enumerate(inp):
        end1, end2 = line.split('~')
        coords1 = end1.split(',')
        coords2 = end2.split(',')
        bricks.append([int(coords1[0]), int(coords2[0]), int(coords1[1]),
                       int(coords2[1]), int(coords1[2]), int(coords2[2])])
        for x in range(int(coords1[0]), int(coords2[0]) + 1):
            for y in range(int(coords1[1]), int(coords2[1]) + 1):
                brick_space[(x, y, 0)] = -1
                for z in range(int(coords1[2]), int(coords2[2]) + 1):
                    brick_space[(x, y, z)] = i_line

    still_falling = True
    while still_falling:
        still_falling = False
        for i_brick in range(len(bricks)):
            drop_distance = bricks[i_brick][4] - 1  # to the ground
            for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
                for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                    if (x, y, bricks[i_brick][4] - 1) in brick_space:
                        drop_distance = 0
                        break
                    else:
                        for z in range(bricks[i_brick][4] - 2, 0, -1):
                            if (x, y, z) in brick_space:
                                col_drop_distance = bricks[i_brick][4] - z - 1
                                if col_drop_distance < drop_distance:
                                    drop_distance = col_drop_distance
                                break
            if drop_distance > 0:
                still_falling = True
                for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
                    for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                        for z in range(bricks[i_brick][4], bricks[i_brick][5] + 1):
                            brick_nr = brick_space.pop((x, y, z))
                            brick_space[(x, y, z - drop_distance)] = brick_nr
                bricks[i_brick][4] -= drop_distance
                bricks[i_brick][5] -= drop_distance

    # all can be disintegrated until they're found to be an only support
    can_be_disintegrated = [True] * len(bricks)
    for i_brick in range(len(bricks)):
        z = bricks[i_brick][4] - 1
        supported_by = []
        for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
            for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                brick_coords = (x,y,z)
                if brick_coords in brick_space:
                    supporting_brink = brick_space[brick_coords]
                    if supporting_brink not in [-1, i_brick]:
                        supported_by.append(supporting_brink)
        if len(set(supported_by)) == 1:
            can_be_disintegrated[supported_by[0]] = False

    return sum(can_be_disintegrated)

def b(inp):
    bricks = []
    brick_space = {}
    for i_line, line in enumerate(inp):
        end1, end2 = line.split('~')
        coords1 = end1.split(',')
        coords2 = end2.split(',')
        bricks.append([int(coords1[0]), int(coords2[0]), int(coords1[1]),
                       int(coords2[1]), int(coords1[2]), int(coords2[2])])
        for x in range(int(coords1[0]), int(coords2[0]) + 1):
            for y in range(int(coords1[1]), int(coords2[1]) + 1):
                brick_space[(x, y, 0)] = -1
                for z in range(int(coords1[2]), int(coords2[2]) + 1):
                    brick_space[(x, y, z)] = i_line

    still_falling = True
    while still_falling:
        still_falling = False
        for i_brick in range(len(bricks)):
            drop_distance = bricks[i_brick][4] - 1  # to the ground
            for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
                for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                    if (x, y, bricks[i_brick][4] - 1) in brick_space:
                        drop_distance = 0
                        break
                    else:
                        for z in range(bricks[i_brick][4] - 2, 0, -1):
                            if (x, y, z) in brick_space:
                                col_drop_distance = bricks[i_brick][4] - z - 1
                                if col_drop_distance < drop_distance:
                                    drop_distance = col_drop_distance
                                break
            if drop_distance > 0:
                still_falling = True
                for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
                    for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                        for z in range(bricks[i_brick][4], bricks[i_brick][5] + 1):
                            brick_nr = brick_space.pop((x, y, z))
                            brick_space[(x, y, z - drop_distance)] = brick_nr
                bricks[i_brick][4] -= drop_distance
                bricks[i_brick][5] -= drop_distance

    bricks_rest_on = []
    for i_brick in range(len(bricks)):
        z = bricks[i_brick][4] - 1

        brick_rests_on = []
        for x in range(bricks[i_brick][0], bricks[i_brick][1] + 1):
            for y in range(bricks[i_brick][2], bricks[i_brick][3] + 1):
                brick_coords = (x,y,z)
                if brick_coords in brick_space:
                    supporting_brink = brick_space[brick_coords]
                    if supporting_brink != i_brick:
                        if i_brick not in brick_rests_on:
                            brick_rests_on.append(supporting_brink)
        bricks_rest_on.append(brick_rests_on)

    would_collapse = 0
    for i_brick in range(len(bricks)):
        has_fallen = set()
        bricks_rest_on_tmp = deepcopy(bricks_rest_on)
        bottom_bricks_to_go_through = [i_brick]
        while bottom_bricks_to_go_through:
            bottom_brick = bottom_bricks_to_go_through.pop()
            for j_brick in range(len(bricks)):
                if j_brick == bottom_brick: continue
                if j_brick in has_fallen: continue
                if bottom_brick in bricks_rest_on_tmp[j_brick]:
                    bricks_rest_on_tmp[j_brick] = [e for e in bricks_rest_on_tmp[j_brick] if e != bottom_brick]
                    if len(bricks_rest_on_tmp[j_brick]) == 0:
                        bottom_bricks_to_go_through.append(j_brick)
                        has_fallen.add(j_brick)
                        would_collapse += 1

    return would_collapse

def test_a():
    assert a(get_input()) == 432

def test_b():
    assert b(get_input()) == 63166

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))

    #cProfile.run('test_b()')
