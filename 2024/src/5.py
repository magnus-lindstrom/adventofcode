import argparse
import sys
import pathlib


def get_input(test=False):
    q_nr = pathlib.Path(__file__).stem
    if test:
        file_name = pathlib.Path('inputs/' + q_nr + '_test')
    else:
        file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_page_orders(inp):
    # which numbers must come after a certain number?
    subsequent_pages = {}
    for line in inp:
        if not line:
            return subsequent_pages
        first_page, second_page = line.split('|')
        if first_page not in subsequent_pages:
            subsequent_pages[first_page] = set()
        subsequent_pages[first_page].add(second_page)
    print('ERROR parsing page orders')
    sys.exit(1)

def get_updates(inp):
    updates = []
    passed_the_empty_line = False
    for line in inp:
        if not line:
            passed_the_empty_line = True
            continue
        if passed_the_empty_line:
            updates.append(line.split(','))

    return updates

def middle_number(update):
    return int(update[(len(update) - 1) // 2])

def a(inp):
    subsequent_pages = get_page_orders(inp)
    updates = get_updates(inp)
    summ = 0

    for update in updates:
        invalid_update = False
        seen_nrs = []
        for nr in update:
            for seen_nr in seen_nrs:
                if nr in subsequent_pages and seen_nr in subsequent_pages[nr]:
                    invalid_update = True
                    break
            if invalid_update: break
            seen_nrs.append(nr)
        if not invalid_update:
            summ += middle_number(update)

    return summ

def b(inp):
    subsequent_pages = get_page_orders(inp)
    updates = get_updates(inp)
    invalid_updates = []

    # find all invalid updates
    for update in updates:
        invalid_update = False
        seen_nrs = []
        for nr in update:
            for seen_nr in seen_nrs:
                if nr in subsequent_pages and seen_nr in subsequent_pages[nr]:
                    invalid_update = True
                    break
            if invalid_update: break
            seen_nrs.append(nr)
        if invalid_update:
            invalid_updates.append(update)

    # rearrange invalid updates to become valid
    for update in invalid_updates:
        while(True):
            seen_nrs = []
            seen_nrs_indeces = []
            to_swap = None
            for i_nr, nr in enumerate(update):
                for i_seen_nr, seen_nr in enumerate(seen_nrs):
                    if nr in subsequent_pages and seen_nr in subsequent_pages[nr]:
                        to_swap = (i_nr, i_seen_nr)
                        break
                seen_nrs.append(nr)
                seen_nrs_indeces.append(i_nr)
                if to_swap is not None:
                    break
            if to_swap is None:
                break

            nr_0 = update[to_swap[0]]
            nr_1 = update[to_swap[1]]
            update[to_swap[0]] = nr_1
            update[to_swap[1]] = nr_0

    summ = 0
    for update in invalid_updates:
        summ += middle_number(update)

    return summ

def test_a():
    assert a(get_input()) == 4766

def test_b():
    assert b(get_input()) == 6257

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
