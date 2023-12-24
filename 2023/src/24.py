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
    if len(inp) < 10:
        xmin, xmax, ymin, ymax = 7, 27, 7, 27
    else:
        xmin, xmax, ymin, ymax = 200000000000000, 400000000000000, 200000000000000, 400000000000000
    hail_positions = []
    hail_velocities = []
    for line in inp:
        words = line.split()
        x, y, z = int(words[0][:-1]), int(words[1][:-1]), int(words[2])
        vx, vy, vz = int(words[4][:-1]), int(words[5][:-1]), int(words[6])
        hail_positions.append([x, y, z])
        hail_velocities.append([vx, vy, vz])

    inside = 0
    for i, ((x1, y1, _), (vx1, vy1, _)) in enumerate(zip(hail_positions, hail_velocities)):
        for j, ((x2, y2, _), (vx2, vy2, _)) in enumerate(zip(hail_positions, hail_velocities)):
            if j <= i:
                continue
            # if intersect, this must hold
            k1 = vy1 / vx1
            k2 = vy2 / vx2
            if k1 == k2:  # will not intersect
                continue

            #t1 = (y2 - y1 + (vy1 * (x1 - x2) / vx1)) / ((vy1 * vx2 / vx1) - vy2)
            t2 = (x2 - x1 + (vx1 * (y1 - y2) / vy1)) / ((vx1 * vy2 / vy1) - vx2)
            t1 = (x2 + (vx2 * t2) - x1) / vx1
            if t1 < 0 or t2 < 0:
                pass  # happened in the past one one or both
            else:
                # future
                x = x1 + t1 * vx1
                y = y1 + t1 * vy1
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    inside += 1

    return inside

def b(inp):
    pos = []
    vel = []
    for line in inp:
        words = line.split()
        x, y, z = int(words[0][:-1]), int(words[1][:-1]), int(words[2])
        vx, vy, vz = int(words[4][:-1]), int(words[5][:-1]), int(words[6])
        pos.append([x, y, z])
        vel.append([vx, vy, vz])

    # iterate over every hail as a starting point for the rock thrown
    for start_hail_index in range(len(pos)):
        if start_hail_index == 1:
            second_hail_index = 0
        else:
            second_hail_index = 1
        for t_from_first_to_second_hail in range(-1000, 1000):
            if t_from_first_to_second_hail == 0:
                continue
            # initially, the rock will be at hail 1 at t = 1

            # position of first hail when it is hit at t = 1
            x1 = pos[start_hail_index][0] + vel[start_hail_index][0]
            y1 = pos[start_hail_index][1] + vel[start_hail_index][1]
            z1 = pos[start_hail_index][2] + vel[start_hail_index][2]

            # position of second hail when it is hit at t = 1 + t_to_first_hit
            x2_at_hit = pos[second_hail_index][0] + ((1 + t_from_first_to_second_hail) * vel[second_hail_index][0])
            y2_at_hit = pos[second_hail_index][1] + ((1 + t_from_first_to_second_hail) * vel[second_hail_index][1])
            z2_at_hit = pos[second_hail_index][2] + ((1 + t_from_first_to_second_hail) * vel[second_hail_index][2])

            if start_hail_index == 4 and second_hail_index == 1 and t_from_first_to_second_hail == 2:
                print(x1, y1, z1)
                print(x2_at_hit, y2_at_hit, z2_at_hit)

            if ((x2_at_hit - x1) % t_from_first_to_second_hail != 0
                    or (y2_at_hit - y1) % t_from_first_to_second_hail != 0
                    or (z2_at_hit - z1) % t_from_first_to_second_hail != 0):
                continue
            vx1 = (x2_at_hit - x1) // t_from_first_to_second_hail
            vy1 = (y2_at_hit - y1) // t_from_first_to_second_hail
            vz1 = (z2_at_hit - z1) // t_from_first_to_second_hail

            # reset x1, y1, z1 to when the rock was actually thrown (1s back in time)
            x1 -= vx1
            y1 -= vy1
            z1 -= vz1

            print('starting speed of rock:', vx1, vy1, vz1)

            # lowest time at which a ball is hit
            min_t = 0
            # position of rock at lowest time
            min_x, min_y, min_z = x1, y1, z1

            was_successful = True
            for i, ((x2, y2, z2), (vx2, vy2, vz2)) in enumerate(zip(pos, vel)):
                if i == start_hail_index or i == second_hail_index:
                    continue

                # in this loop, the rock is particle 1 and the hail is particle 2
                # first, do they intersect?
                top = x1 - x2
                bottom = vx2 - vx1
                if bottom == 0:
                    top = y1 - y2
                    bottom = vy2 - vy1
                if bottom == 0:
                    top = z1 - z2
                    bottom = vz2 - vz1
                if bottom == 0:
                    print('something wrong')
                    continue

                print(top, bottom)
                t = top // bottom
                if start_hail_index == 4 and second_hail_index == 1 and t_from_first_to_second_hail == 2:
                    print('hail {} should be hit at t = {} because'.format(i, t))
                    print('x1: {}, y1: {}, z1: {}'.format(x1, y1, z1))
                    print('vx1: {}, vy1: {}, vz1: {}'.format(vx1, vy1, vz1))
                    print('x2: {}, y2: {}, z2: {}'.format(x2, y2, z2))
                    print('vx2: {}, vy2: {}, vz2: {}'.format(vx2, vy2, vz2))
                if (not (x1 + t * vx1 == x2 + t * vx2)
                        or (not y1 + t * vy1 == y2 + t * vy2)
                        or (not z1 + t * vz1 == z2 + t * vz2)):
                    was_successful = False
                    break

                # this rock is hit. is it the mininum t so far?
                if t < min_t:
                    min_t = t
                    min_x, min_y, min_z = x1 - (t * vx1), y1 - (t * vy1), z1 - (t * vz1)

            if was_successful:
                # one more step back in time, so that the first ball is hit at t=1
                return min_x - vx1 + min_y - vy1 + min_z - vz1

    return 0

def test_a():
    assert a(get_input()) == 0

def test_b():
    assert b(get_input()) == 0

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
        print('a:', a(inp))
        print('b:', b(inp))
