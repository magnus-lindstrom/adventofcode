import pathlib


def get_test_input():
    return '''p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>'''.split('\n')

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a():
    inp = get_input()
    min_acc = 10000000
    min_vel = 10000000
    min_pos = 10000000
    min_acc_index = 0
    for i_line, line in enumerate(inp):

        words = line.split(', ')

        # get position of particle
        start_i = words[0].index('<') + 1
        end_i = words[0].index('>')
        positions = words[0][start_i:end_i]
        starting_pos = 0
        for pos in positions.split(','):
            starting_pos += abs(int(pos))

        # get velocity of particle
        start_i = words[1].index('<') + 1
        end_i = words[1].index('>')
        velocities = words[1][start_i:end_i]
        starting_vel = 0
        for vel in velocities.split(','):
            starting_vel += abs(int(vel))

        # get acceleration of particle
        start_i = words[2].index('<') + 1
        end_i = words[2].index('>')
        accs = words[2][start_i:end_i]
        particle_acc = 0
        for acc in accs.split(','):
            particle_acc += abs(int(acc))

        #accelerations[i_line] = 0
        if particle_acc < min_acc:
            min_acc = particle_acc
            min_vel = starting_vel
            min_pos = starting_pos
            min_acc_index = i_line
        elif particle_acc == min_acc and starting_vel < min_vel:
            min_vel = starting_vel
            min_pos = starting_pos
            min_acc_index = i_line
        elif particle_acc == min_acc and starting_vel == min_vel and starting_pos < min_pos:
            min_pos = starting_pos
            min_acc_index = i_line

    return min_acc_index

class Particle:
    def __init__(self, string):
        words = string.split(', ')

        # get position of particle
        start_i = words[0].index('<') + 1
        end_i = words[0].index('>')
        positions = words[0][start_i:end_i]
        self.x = int(positions.split(',')[0])
        self.y = int(positions.split(',')[1])
        self.z = int(positions.split(',')[2])

        # get velocity of particle
        start_i = words[1].index('<') + 1
        end_i = words[1].index('>')
        velocities = words[1][start_i:end_i]
        self.vx = int(velocities.split(',')[0])
        self.vy = int(velocities.split(',')[1])
        self.vz = int(velocities.split(',')[2])

        # get acceleration of particle
        start_i = words[2].index('<') + 1
        end_i = words[2].index('>')
        accs = words[2][start_i:end_i]
        self.ax = int(accs.split(',')[0])
        self.ay = int(accs.split(',')[1])
        self.az = int(accs.split(',')[2])

    def move(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz


def get_distance_matrix(particles):
    distances = []
    for i_p1, p1 in enumerate(particles):
        distances.append([])
        for j_p2, p2 in enumerate(particles):
            if j_p2 <= i_p1:
                distances[i_p1].append(0)
            else:
                dist = abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)
                distances[i_p1].append(dist)
    return distances

def b():
    inp = get_input()
    particles = []
    for line in inp:
        particles.append(Particle(line))

    while True:
        to_remove = set()
        for i_particle, particle_1 in enumerate(particles):
            for j_particle, particle_2 in enumerate(particles):
                if j_particle <= i_particle:
                    continue

                if (particle_1.x == particle_2.x
                        and particle_1.y == particle_2.y
                        and particle_1.z == particle_2.z
                        ):
                    to_remove.add(i_particle)
                    to_remove.add(j_particle)
        if to_remove:
            particles = [p for i, p in enumerate(particles) if i not in to_remove]

        distances = get_distance_matrix(particles)
        for particle in particles:
            particle.move()
        new_distances = get_distance_matrix(particles)
        got_closer = False
        for i in range(len(particles)):
            for j in range(len(particles)):
                if j <= i:
                    continue
                if new_distances[i][j] < distances[i][j]:
                    got_closer = True
        if not got_closer:
            return len(particles)

def test_a():
    assert a() == 161

def test_b():
    assert b() == 438

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
