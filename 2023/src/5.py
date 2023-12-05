import pathlib
from sys import maxsize


def get_test_input():
    file_name = pathlib.Path('inputs/5_test')
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def a_old():
    inp = get_input()
    initial_seeds = []
    section_reading = 0
    seed_to_soil = {}
    for line in inp:
        print(line)
        if line == '':
            section_reading += 1
        elif section_reading == 0:
            initial_seeds.extend(line.split()[1:])
        else:
            words = line.split()
            if not words[0].isdigit():
                continue  # heading

            dest_range_start = int(words[0])
            source_range_start = int(words[1])
            range_length = int(words[2])
            if section_reading == 1:
                for source, dest in zip(range(source_range_start, source_range_start+range_length+1),
                                        range(dest_range_start, dest_range_start+range_length+1)):
                    print(source, dest)
    return 0

def a():
    inp = get_input()
    #inp = get_test_input()
    initial_seeds = []
    section_reading = 0
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    for line in inp:
        #print(line)
        if line == '':
            section_reading += 1
        elif section_reading == 0:
            initial_seeds.extend([int(e) for e in line.split()[1:]])
        else:
            words = line.split()
            if not words[0].isdigit():
                continue  # heading

            dest_range_start = int(words[0])
            source_range_start = int(words[1])
            range_length = int(words[2])
            if section_reading == 1:
                seed_to_soil.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 2:
                soil_to_fertilizer.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 3:
                fertilizer_to_water.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 4:
                water_to_light.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 5:
                light_to_temperature.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 6:
                temperature_to_humidity.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 7:
                humidity_to_location.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
    seed_to_soil.sort(key=lambda x: x['source_start'])
    soil_to_fertilizer.sort(key=lambda x: x['source_start'])
    fertilizer_to_water.sort(key=lambda x: x['source_start'])
    water_to_light.sort(key=lambda x: x['source_start'])
    light_to_temperature.sort(key=lambda x: x['source_start'])
    temperature_to_humidity.sort(key=lambda x: x['source_start'])
    humidity_to_location.sort(key=lambda x: x['source_start'])

    #for e in seed_to_soil:
        #print(e['source_start'])
    final_values = []

    for seed in initial_seeds:
        value = seed
        #print('new value:', value)
        for conversion in [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]:
            for rangee in conversion:
                #print(conversion)
                if rangee['source_start'] <= value < rangee['source_start'] + rangee['range_length']:
                    offset = value - rangee['source_start']
                    value = rangee['dest_start'] + offset
                    #print('value:', value)
                    break





            # for rangee in conversion:
            #     # At most one rangee will make a conversion, the rest will not
            #     if rangee['dest_start'] < rangee['source_start']:
            #         if value < rangee['dest_start']:
            #             break
            #         elif rangee['dest_start'] <= value < rangee['source_start']:
            #             value = value + rangee['range_length']
            #             break
            #         elif rangee['source_start'] <= value < rangee['source_start'] + rangee['range_length']:
            #             offset = value - rangee['source_start']
            #             value = rangee['dest_start'] + offset
            #             break
            #     if rangee['source_start'] < rangee['dest_start']:
            #         if value < rangee['source_start']:
            #             break
            #         elif rangee['source_start'] <= value < rangee['dest_start']:
            #             value = value + rangee['range_length']
            #             break
            #         elif rangee['dest_start'] <= value < rangee['dest_start'] + rangee['range_length']:
            #             offset = value - rangee['dest_start']
            #             value = rangee['source_start'] + offset
            #             break
            # print('value:', value)
        final_values.append(value)
    return min(final_values)







                    #if value < rangee['source_start']:
                        #value = value + offset
                        #break
                    #elif rangee['source_start'] <= value < rangee['source_start'] + rangee['range_length']:
                        #offset += value - rangee['source_start']
                        #value = rangee['dest_range_start'] + offset
                        #break
                    #elif rangee['source_start'] + rangee['range_length'] <= value
                    #else:
                        #offset += rangee['range_length']

def b():
    inp = get_input()
    #inp = get_test_input()
    initial_seed_ranges = []
    section_reading = 0
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    for line in inp:
        #print(line)
        if line == '':
            section_reading += 1
        elif section_reading == 0:
            nrs = line.split()[1:]
            for i in range(0, len(nrs), 2):
                initial_seed_ranges.append([int(nrs[i]), int(nrs[i+1])])
        else:
            words = line.split()
            if not words[0].isdigit():
                continue  # heading

            dest_range_start = int(words[0])
            source_range_start = int(words[1])
            range_length = int(words[2])
            if section_reading == 1:
                seed_to_soil.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 2:
                soil_to_fertilizer.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 3:
                fertilizer_to_water.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 4:
                water_to_light.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 5:
                light_to_temperature.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 6:
                temperature_to_humidity.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
            elif section_reading == 7:
                humidity_to_location.append({'dest_start': dest_range_start,
                                     'source_start': source_range_start,
                                     'range_length': range_length})
    humidity_to_location.sort(key=lambda x: x['dest_start'])

    counter = 1

    for start_range in humidity_to_location:
        for start_value in range(start_range['source_start'], start_range['source_start'] + start_range['range_length']): # correct range?
            value = start_value
            counter += 1
            if counter % 1000000 == 0:
                print(counter)
            #print('new value:', value)
            for conversion in [humidity_to_location, temperature_to_humidity, light_to_temperature, water_to_light, fertilizer_to_water, soil_to_fertilizer, seed_to_soil]:
                for rangee in conversion:
                    #print(conversion)
                    if rangee['dest_start'] <= value < rangee['dest_start'] + rangee['range_length']:
                        offset = value - rangee['dest_start']
                        value = rangee['source_start'] + offset
                        #print('value:', value)
                        break

            for seed_range in initial_seed_ranges:
                if seed_range[0] <= value < seed_range[0] + seed_range[1]:
                    return start_value

def fast_b():
    inp = get_input()
    inp = get_test_input()
    initial_seed_ranges = []
    section_reading = 0
    seed_to_soil_ranges = []
    soil_to_fertilizer_ranges = []
    fertilizer_to_water_ranges = []
    water_to_light_ranges = []
    light_to_temperature_ranges = []
    temperature_to_humidity_ranges = []
    humidity_to_location_ranges = []
    for line in inp:
        #print(line)
        if line == '':
            section_reading += 1
        elif section_reading == 0:
            nrs = line.split()[1:]
            for i in range(0, len(nrs), 2):
                initial_seed_ranges.append([int(nrs[i]), int(nrs[i+1])])
        else:
            words = line.split()
            if not words[0].isdigit():
                continue  # heading

            dest_range_start = int(words[0])
            source_range_start = int(words[1])
            range_length = int(words[2])
            if section_reading == 1:
                seed_to_soil_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 2:
                soil_to_fertilizer_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 3:
                fertilizer_to_water_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 4:
                water_to_light_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 5:
                light_to_temperature_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 6:
                temperature_to_humidity_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])
            elif section_reading == 7:
                humidity_to_location_ranges.append([
                    [source_range_start, source_range_start+range_length-1],
                    [dest_range_start, dest_range_start+range_length-1]
                ])

        not_done = True
        min_value = 0
        max_value = maxsize
        while not_done:
            pass


def test_a():
    assert a() == 313045984

def test_b():
    assert b() == 20283860

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
