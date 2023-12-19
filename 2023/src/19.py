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

class Rule:
    def __init__(self, rule_string):
        if ':' in rule_string:
            self.has_comparison = True
            if '<' in rule_string: words = rule_string.split('<')
            else: words = rule_string.split('>')
            self.attribute_to_compare = words[0]
            nr_to_compare_to, self.destination = words[1].split(':')
            self.nr_to_compare_to = int(nr_to_compare_to)
            if '<' in rule_string:
                self.comparison_is_less_than = True
                self.comparison_is_greater_than = False
            else:
                self.comparison_is_greater_than = True
                self.comparison_is_less_than = False
        else:
            self.has_comparison = False
            self.attribute_to_compare = None
            self.nr_to_compare_to = None
            self.comparison_is_greater_than = None
            self.comparison_is_less_than = None
            self.destination = rule_string

    def get_destination(self, part):
        if self.has_comparison:
            if self.comparison_is_greater_than:
                if part[self.attribute_to_compare] > self.nr_to_compare_to:
                    return self.destination
            else:
                if part[self.attribute_to_compare] < self.nr_to_compare_to:
                    return self.destination
            return 'next'
        else:
            return self.destination



def get_combinations(workflows, workflow_name, rule_index, ranges, shall_pass):
    if rule_index == -1:
        if workflow_name == 'in':
            return (
                (ranges['x'][1] - ranges['x'][0] + 1)
                * (ranges['m'][1] - ranges['m'][0] + 1)
                * (ranges['a'][1] - ranges['a'][0] + 1)
                * (ranges['s'][1] - ranges['s'][0] + 1)
            )
        else:
            # if we cleared all rules and got back to the start of the
            # workflow, see which other workflow rules end up in this workflow
            combs = 0
            for w_name, w in workflows.items():
                if w_name == workflow_name: continue
                for i_rule, rule in enumerate(w):
                    if rule.destination == workflow_name:
                        combs += get_combinations(workflows, w_name, i_rule, ranges, shall_pass=True)
            return combs

    for r in ranges.values():
        if r[0] > r[1]:  # impossible to satisfy, no combinations
            return 0

    rule = workflows[workflow_name][rule_index]
    if not rule.has_comparison:
        return get_combinations(workflows, workflow_name, rule_index - 1, ranges, False)
    else:
        if shall_pass:
            if rule.comparison_is_greater_than:
                min_value = rule.nr_to_compare_to + 1
                if ranges[rule.attribute_to_compare][0] < min_value:
                    ranges[rule.attribute_to_compare][0] = min_value
            else:
                max_value = rule.nr_to_compare_to - 1
                if ranges[rule.attribute_to_compare][1] > max_value:
                    ranges[rule.attribute_to_compare][1] = max_value
        else:  # shan't pass
            if rule.comparison_is_greater_than:
                max_value = rule.nr_to_compare_to
                if ranges[rule.attribute_to_compare][1] > max_value:
                    ranges[rule.attribute_to_compare][1] = max_value
            else:
                min_value = rule.nr_to_compare_to
                if ranges[rule.attribute_to_compare][0] < min_value:
                    ranges[rule.attribute_to_compare][0] = min_value
        return get_combinations(workflows, workflow_name, rule_index - 1, ranges, False)

def a(inp):
    workflows = {}
    done_with_workflows = False
    parts = []
    for line in inp:
        if line == '':
            done_with_workflows = True
            continue
        if not done_with_workflows:
            words = line[:-1].split('{')

            workflows[words[0]] = []
            for r in words[1].split(','):
                workflows[words[0]].append(Rule(r))
        else:
            words = line[1:-1].split(',')
            part = {}
            part['x'] = int(words[0][2:])
            part['m'] = int(words[1][2:])
            part['a'] = int(words[2][2:])
            part['s'] = int(words[3][2:])
            parts.append(part)

    summ = 0
    for part in parts:
        dest_workflow = 'in'
        i_rule = 0
        while dest_workflow not in ['A', 'R']:
            new_workflow = workflows[dest_workflow][i_rule].get_destination(part)
            if new_workflow == 'next':
                i_rule += 1
            else:
                dest_workflow = new_workflow
                i_rule = 0
        if dest_workflow == 'A':
            summ += part['x'] + part['m'] + part['a'] + part['s']
    return summ

def b(inp):
    workflows = {}
    done_with_workflows = False
    parts = []
    for line in inp:
        if line == '':
            done_with_workflows = True
            continue
        if not done_with_workflows:
            words = line[:-1].split('{')

            workflows[words[0]] = []
            for r in words[1].split(','):
                workflows[words[0]].append(Rule(r))
        else:
            words = line[1:-1].split(',')
            part = {}
            part['x'] = int(words[0][2:])
            part['m'] = int(words[1][2:])
            part['a'] = int(words[2][2:])
            part['s'] = int(words[3][2:])
            parts.append(part)

    combinations = 0
    for workflow, rules in workflows.items():
        start_rules = [i for i, r in enumerate(rules) if r.destination == 'A']
        if not start_rules:
            continue
        for start_rule in start_rules:
            ranges = {
                'x': [1, 4000],
                'm': [1, 4000],
                'a': [1, 4000],
                's': [1, 4000],
            }
            combinations += get_combinations(workflows, workflow, start_rule, ranges, shall_pass=True)

    return combinations

def test_a():
    assert a(get_input()) == 350678

def test_b():
    assert b(get_input()) == 124831893423809

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true')
    args = parser.parse_args()
    inp = get_input(test=args.test)

    print('a:', a(inp))
    print('b:', b(inp))
