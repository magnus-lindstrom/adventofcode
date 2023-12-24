import argparse
import pathlib
from sys import maxsize

from sympy import Eq
from sympy.abc import c, d, e, f, g, h, k, l, m
from sympy.solvers import solve


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

def b_first(inp):
    pos = []
    vel = []
    for line in inp:
        words = line.split()
        x, y, z = int(words[0][:-1]), int(words[1][:-1]), int(words[2])
        vx, vy, vz = int(words[4][:-1]), int(words[5][:-1]), int(words[6])
        pos.append([x, y, z])
        vel.append([vx, vy, vz])

    # which 2 hails start closest to one another?
    min_dist = maxsize
    min_pair = (0, 0)
    for i, (x1, y1, z1) in enumerate(pos):
        for j, (x2, y2, z2) in enumerate(pos):
            if j <= i:
                continue
            dist = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            if dist < min_dist:
                min_dist = dist
                min_pair = (i, j)
                print('new min:', min_dist, min_pair)

    start_hail_index = min_pair[0]
    second_hail_index = min_pair[1]
    time_til_first_hail_hit = 0
    while True:
        time_til_first_hail_hit += 1
        print(time_til_first_hail_hit)

        # position of first hail when it is hit at t
        x1_first_hail_hit = pos[start_hail_index][0] + time_til_first_hail_hit * vel[start_hail_index][0]
        y1_first_hail_hit = pos[start_hail_index][1] + time_til_first_hail_hit * vel[start_hail_index][1]
        z1_first_hail_hit = pos[start_hail_index][2] + time_til_first_hail_hit * vel[start_hail_index][2]

        # time is always counted from when rock is thrown
        for time_til_second_hail_hit in range(1, 10000000):
            if time_til_second_hail_hit == time_til_first_hail_hit:
                continue

            # position of second hail when it is hit at t = 1 + t_to_first_hit
            x2_second_hail_hit = pos[second_hail_index][0] + (time_til_second_hail_hit * vel[second_hail_index][0])
            y2_second_hail_hit = pos[second_hail_index][1] + (time_til_second_hail_hit * vel[second_hail_index][1])
            z2_second_hail_hit = pos[second_hail_index][2] + (time_til_second_hail_hit * vel[second_hail_index][2])

            # require integer solutions
            if ((x2_second_hail_hit - x1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0
                    or (y2_second_hail_hit - y1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0
                    or (z2_second_hail_hit - z1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0):
                continue
            vx1 = (x2_second_hail_hit - x1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)
            vy1 = (y2_second_hail_hit - y1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)
            vz1 = (z2_second_hail_hit - z1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)

            # pos of rock when thrown
            x1 = x1_first_hail_hit - time_til_first_hail_hit * vx1
            y1 = y1_first_hail_hit - time_til_first_hail_hit * vy1
            z1 = z1_first_hail_hit - time_til_first_hail_hit * vz1


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

                #print(top, bottom)
                t = top // bottom
                #if start_hail_index == 4 and second_hail_index == 1 and t_from_first_to_second_hail == 2:
                    #print('hail {} should be hit at t = {} because'.format(i, t))
                    #print('x1: {}, y1: {}, z1: {}'.format(x1, y1, z1))
                    #print('vx1: {}, vy1: {}, vz1: {}'.format(vx1, vy1, vz1))
                    #print('x2: {}, y2: {}, z2: {}'.format(x2, y2, z2))
                    #print('vx2: {}, vy2: {}, vz2: {}'.format(vx2, vy2, vz2))
                if (not (x1 + t * vx1 == x2 + t * vx2)
                        or (not y1 + t * vy1 == y2 + t * vy2)
                        or (not z1 + t * vz1 == z2 + t * vz2)):
                    was_successful = False
                    break

            if was_successful:
                # one more step back in time, so that the first ball is hit at t=1
                return x1 + y1 + z1

def b_faster(inp):
    pos = []
    vel = []
    for line in inp:
        words = line.split()
        x, y, z = int(words[0][:-1]), int(words[1][:-1]), int(words[2])
        vx, vy, vz = int(words[4][:-1]), int(words[5][:-1]), int(words[6])
        pos.append([x, y, z])
        vel.append([vx, vy, vz])

    # which 2 hails start closest to one another?
    min_dist = maxsize
    min_pair = (0, 0)
    for i, (x1, y1, z1) in enumerate(pos):
        for j, (x2, y2, z2) in enumerate(pos):
            if j <= i:
                continue
            dist = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            if dist < min_dist:
                min_dist = dist
                min_pair = (i, j)
                print('new min:', min_dist, min_pair)

    start_hail_index = min_pair[0]
    second_hail_index = min_pair[1]
    time_til_first_hail_hit = 0
    while True:
        time_til_first_hail_hit += 1
        print(time_til_first_hail_hit)

        # position of first hail when it is hit at t
        x1_first_hail_hit = pos[start_hail_index][0] + time_til_first_hail_hit * vel[start_hail_index][0]
        y1_first_hail_hit = pos[start_hail_index][1] + time_til_first_hail_hit * vel[start_hail_index][1]
        z1_first_hail_hit = pos[start_hail_index][2] + time_til_first_hail_hit * vel[start_hail_index][2]

        # time is always counted from when rock is thrown
        for time_til_second_hail_hit in range(1, 10000000):
            if time_til_second_hail_hit == time_til_first_hail_hit:
                continue

            # position of second hail when it is hit at t = 1 + t_to_first_hit
            x2_second_hail_hit = pos[second_hail_index][0] + (time_til_second_hail_hit * vel[second_hail_index][0])
            y2_second_hail_hit = pos[second_hail_index][1] + (time_til_second_hail_hit * vel[second_hail_index][1])
            z2_second_hail_hit = pos[second_hail_index][2] + (time_til_second_hail_hit * vel[second_hail_index][2])

            # require integer solutions
            if ((x2_second_hail_hit - x1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0
                    or (y2_second_hail_hit - y1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0
                    or (z2_second_hail_hit - z1_first_hail_hit) % (time_til_second_hail_hit - time_til_first_hail_hit) != 0):
                # when would be the next integer solution?
                continue

            vx1 = (x2_second_hail_hit - x1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)
            vy1 = (y2_second_hail_hit - y1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)
            vz1 = (z2_second_hail_hit - z1_first_hail_hit) // (time_til_second_hail_hit - time_til_first_hail_hit)

            # pos of rock when thrown
            x1 = x1_first_hail_hit - time_til_first_hail_hit * vx1
            y1 = y1_first_hail_hit - time_til_first_hail_hit * vy1
            z1 = z1_first_hail_hit - time_til_first_hail_hit * vz1


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

                #print(top, bottom)
                t = top // bottom
                #if start_hail_index == 4 and second_hail_index == 1 and t_from_first_to_second_hail == 2:
                    #print('hail {} should be hit at t = {} because'.format(i, t))
                    #print('x1: {}, y1: {}, z1: {}'.format(x1, y1, z1))
                    #print('vx1: {}, vy1: {}, vz1: {}'.format(vx1, vy1, vz1))
                    #print('x2: {}, y2: {}, z2: {}'.format(x2, y2, z2))
                    #print('vx2: {}, vy2: {}, vz2: {}'.format(vx2, vy2, vz2))
                if (not (x1 + t * vx1 == x2 + t * vx2)
                        or (not y1 + t * vy1 == y2 + t * vy2)
                        or (not z1 + t * vz1 == z2 + t * vz2)):
                    was_successful = False
                    break

            if was_successful:
                # one more step back in time, so that the first ball is hit at t=1
                return x1 + y1 + z1

def b(inp):
    pos = []
    vel = []
    for line in inp:
        words = line.split()
        x, y, z = int(words[0][:-1]), int(words[1][:-1]), int(words[2])
        vx, vy, vz = int(words[4][:-1]), int(words[5][:-1]), int(words[6])
        pos.append([x, y, z])
        vel.append([vx, vy, vz])

    x1, x2, x3 = pos[0][0], pos[1][0], pos[2][0]
    y1, y2, y3 = pos[0][1], pos[1][1], pos[2][1]
    z1, z2, z3 = pos[0][2], pos[1][2], pos[2][2]
    vx1, vx2, vx3 = vel[0][0], vel[1][0], vel[2][0]
    vy1, vy2, vy3 = vel[0][1], vel[1][1], vel[2][1]
    vz1, vz2, vz3 = vel[0][2], vel[1][2], vel[2][2]

    # t1 is when the rock hits the first particle, t2 the second, t3 the third
    # xk, yk, zk are the initial positions of the rock
    # vxk, vyk, vzk is the speed of the rock
    # This creates a system of 9 equations with 9 unknown. Solve algebraically
    # using a solver..

    # t1 = c
    # t2 = d
    # t3 = m
    # xk = e
    # yk = f
    # zk = g
    # vxk = h
    # vyk = k
    # vzk = l
    eq1 = Eq(x1 + c * vx1, e + c * h)
    eq2 = Eq(y1 + c * vy1, f + c * k)
    eq3 = Eq(z1 + c * vz1, g + c * l)

    eq4 = Eq(x2 + d * vx2, e + d * h)
    eq5 = Eq(y2 + d * vy2, f + d * k)
    eq6 = Eq(z2 + d * vz2, g + d * l)

    eq7 = Eq(x3 + m * vx3, e + m * h)
    eq8 = Eq(y3 + m * vy3, f + m * k)
    eq9 = Eq(z3 + m * vz3, g + m * l)

    sol = solve(
        [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9],
        c, e, f, g, h, k, l, d, m,
        dict=True
    )
    xk = sol[0][e]
    yk = sol[0][f]
    zk = sol[0][g]

    return xk + yk + zk

def test_a():
    assert a(get_input()) == 15107

def test_b():
    assert b(get_input()) == 856642398547748

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
