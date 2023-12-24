import argparse
import pathlib

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
