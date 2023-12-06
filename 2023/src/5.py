import pathlib
from sys import maxsize


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_initial_seeds_and_conversions(inp):
    initial_seeds = []
    section_reading = 0
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    max_range_ends = [0] * 7
    for line in inp:
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

            if source_range_start + range_length > max_range_ends[section_reading-1]:
                max_range_ends[section_reading-1] = source_range_start + range_length

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

    for i_conv, conversions in enumerate([seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]):
        min_value = maxsize
        max_value = 0
        for conversion in conversions:
            if conversion['source_start'] < min_value:
                min_value = conversion['source_start']
            elif conversion['source_start'] + conversion['range_length'] > max_value:
                max_value = conversion['source_start'] + conversion['range_length']
        # add conversions from 0 to beyond the maximum value to make interval
        # conversions easier in b()
        if min_value > 0:
            conversions.append({'dest_start': 0, 'source_start': 0,
                                'range_length': min_value})
        conversions.append({'dest_start': max_range_ends[i_conv],
                            'source_start': max_range_ends[i_conv],
                            'range_length': max_range_ends[i_conv] + 1000})

    seed_to_soil.sort(key=lambda x: x['source_start'])
    soil_to_fertilizer.sort(key=lambda x: x['source_start'])
    fertilizer_to_water.sort(key=lambda x: x['source_start'])
    water_to_light.sort(key=lambda x: x['source_start'])
    light_to_temperature.sort(key=lambda x: x['source_start'])
    temperature_to_humidity.sort(key=lambda x: x['source_start'])
    humidity_to_location.sort(key=lambda x: x['source_start'])

    return (
        initial_seeds, seed_to_soil, soil_to_fertilizer,
        fertilizer_to_water, water_to_light, light_to_temperature,
        temperature_to_humidity, humidity_to_location
    )

def a():
    inp = get_input()
    #inp = get_test_input()
    (initial_seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
     water_to_light, light_to_temperature, temperature_to_humidity,
     humidity_to_location) = get_initial_seeds_and_conversions(inp)

    final_values = []

    for seed in initial_seeds:
        value = seed
        for conversion in [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]:
            for rangee in conversion:
                if rangee['source_start'] <= value < rangee['source_start'] + rangee['range_length']:
                    offset = value - rangee['source_start']
                    value = rangee['dest_start'] + offset
                    break

        final_values.append(value)
    return min(final_values)

def slow_naive_b():
    inp = get_input()
    #inp = get_test_input()
    (initial_seed_values, seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
     water_to_light, light_to_temperature, temperature_to_humidity,
     humidity_to_location) = get_initial_seeds_and_conversions(inp)

    humidity_to_location.sort(key=lambda x: x['dest_start'])

    initial_seed_ranges = []
    for i in range(0, len(initial_seed_values), 2):
        initial_seed_ranges.append([initial_seed_values[i], initial_seed_values[i+1]])

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


def b():
    inp = get_input()
    (initial_seed_values, seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
     water_to_light, light_to_temperature, temperature_to_humidity,
     humidity_to_location) = get_initial_seeds_and_conversions(inp)

    humidity_to_location.sort(key=lambda x: x['dest_start'])

    initial_seed_ranges = []
    for i in range(0, len(initial_seed_values), 2):
        initial_seed_ranges.append([initial_seed_values[i], initial_seed_values[i+1]])


    ranges = initial_seed_ranges
    for conversions in [seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
                        water_to_light, light_to_temperature,
                        temperature_to_humidity, humidity_to_location]:
        new_ranges = []
        for rangee in ranges:
            for conv in conversions:
                # check if left interval "border" is included in conversion range
                if conv['source_start'] <= rangee[0] < conv['source_start'] + conv['range_length']:
                    # is whole range included in conversion range?
                    if rangee[0] + rangee[1] <= conv['source_start'] + conv['range_length']:
                        offset = rangee[0] - conv['source_start']
                        new_ranges.append([conv['dest_start'] + offset, rangee[1]])
                    else:  # only part of range is included
                        offset = rangee[0] - conv['source_start']
                        new_ranges.append([conv['dest_start'] + offset, conv['range_length'] - offset])

                # check if right interval "border" is included in conversion range
                elif conv['source_start'] <= rangee[0] + rangee[1] - 1 < conv['source_start'] + conv['range_length']:
                    new_ranges.append([conv['dest_start'], rangee[0] + rangee[1] - conv['source_start']])
                    # No need to check if entire range is included again
                # check if entire conversion range is within the incoming range
                elif (rangee[0] <= conv['source_start'] < rangee[0] + rangee[1]
                      and rangee[0] <= conv['source_start'] +
                      conv['range_length'] - 1 < rangee[0] + rangee[1]):
                    new_ranges.append([conv['dest_start'], conv['range_length']])


        ranges = new_ranges.copy()

    return min(ranges, key=lambda x: x[0])[0]


def test_a():
    assert a() == 313045984

def test_b():
    assert b() == 20283860

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
