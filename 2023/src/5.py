import pathlib
from sys import maxsize


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_initial_seeds_and_conversions(inp):

    all_conversions = []
    local_conversions = []

    initial_seeds = []
    max_range_ends = [0] * 7  # one for each type of conversion

    for i_line, line in enumerate(inp):
        if line == '':
            if local_conversions:
                all_conversions.append(local_conversions)
            local_conversions = []
        elif i_line == 0:
            initial_seeds.extend([int(e) for e in line.split()[1:]])
        else:
            words = line.split()
            if not words[0].isdigit():
                continue  # line is a heading

            dest_range_start = int(words[0])
            source_range_start = int(words[1])
            range_length = int(words[2])

            if source_range_start + range_length > max_range_ends[len(all_conversions)]:
                max_range_ends[len(all_conversions)] = source_range_start + range_length

            local_conversions.append({'dest_start': dest_range_start, 'source_start':
                                source_range_start, 'range_length':
                                range_length})
    all_conversions.append(local_conversions)

    for i_conv, convs in enumerate(all_conversions):
        min_value = maxsize
        max_value = 0
        for conversion in convs:
            if conversion['source_start'] < min_value:
                min_value = conversion['source_start']
            elif conversion['source_start'] + conversion['range_length'] > max_value:
                max_value = conversion['source_start'] + conversion['range_length']

        # add conversions from 0 to beyond the maximum value to make interval
        # conversions easier in b()
        if min_value > 0:
            convs.append({'dest_start': 0, 'source_start': 0,
                                'range_length': min_value})
        convs.append({'dest_start': max_range_ends[i_conv],
                            'source_start': max_range_ends[i_conv],
                            'range_length': max_range_ends[i_conv] + 1000})

    return (initial_seeds, all_conversions)

def a():
    inp = get_input()
    (initial_seeds, conversions) = get_initial_seeds_and_conversions(inp)

    final_values = []

    for seed in initial_seeds:
        value = seed
        for conversion in conversions:
            for rangee in conversion:
                if rangee['source_start'] <= value < rangee['source_start'] + rangee['range_length']:
                    offset = value - rangee['source_start']
                    value = rangee['dest_start'] + offset
                    break

        final_values.append(value)
    return min(final_values)

def b():
    inp = get_input()
    initial_seed_values, conversions = get_initial_seeds_and_conversions(inp)

    initial_seed_ranges = []
    for i in range(0, len(initial_seed_values), 2):
        initial_seed_ranges.append([initial_seed_values[i], initial_seed_values[i+1]])


    ranges = initial_seed_ranges
    for conversions in conversions:
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
