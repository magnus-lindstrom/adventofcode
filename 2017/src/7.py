import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_weight_of_program(program, hierarchies, weights):
    total_weight = weights[program]
    for child_program in hierarchies[program]:
        total_weight += get_weight_of_program(child_program, hierarchies, weights)
    return total_weight

def a():
    inp = get_input()
    hierarchies = {}
    for line in inp:
        words = line.split(' ')
        if words[0] not in hierarchies.keys():
            hierarchies[words[0]] = []

        if len(words) > 2:
            for word in words[3:]:
                hierarchies[words[0]].append(word.removesuffix(','))

    for base in hierarchies.keys():
        unseen = True
        for value_list in hierarchies.values():
            if base in value_list:
                unseen = False
        if unseen:
            return base

    return 'did not find base'

class Tower:
    def __init__(self, name, hierarchies, weights):
        self.weight = weights[name]
        self.name = name
        self.sub_towers = []

        for sub_tower_name in hierarchies[name]:
            self.sub_towers.append(
                Tower(sub_tower_name, hierarchies, weights)
            )

    def get_total_weight(self) -> int:
        return self.weight + sum([tower.get_total_weight() for tower in self.sub_towers])

    def get_corrected_weight(self, corr_to_apply=None):
        weights_of_children = [tower.get_total_weight() for tower in self.sub_towers]
        # print(self.name, [t.name for t in self.sub_towers], weights_of_children, corr_to_apply)
        if corr_to_apply is not None:
            # no children, but i have a correction to achieve -> return
            # modified weight
            if not self.sub_towers:
                print('tjipp')
                return self.weight + corr_to_apply

            # all my children weigh the same, my weight is thus off
            if all([e == weights_of_children[0] for e in weights_of_children]):
                # print('Name:', self.name, 'weight:', self.weight)
                return self.weight + corr_to_apply

            # one child's weight is off, pass the correction to child and
            # return it's return value

            # 2 children, so can't know which one is wrong. Check grandchildren
            # to find out
            # out of all grandchildren, one must be wrong
            if len(self.sub_towers) == 2:
                wrong_child = None
                for i_child, child in enumerate(self.sub_towers):
                    weights_of_grandchildren = [gchild.get_total_weight() for gchild in child.sub_towers]
                    if not all([e == weights_of_grandchildren[0] for e in weights_of_grandchildren]):
                        wrong_child = i_child
                if wrong_child is None:
                    print('god help us')
                else:
                    print('here goes nothing')
                    return self.sub_towers[wrong_child].get_corrected_weight(
                        corr_to_apply
                    )

            elif len(self.sub_towers) > 2:
                # one child's weight is off and we know which one it is
                # return it's return value
                weight_a = weights_of_children[0]
                for i_weight, weight_b in enumerate(weights_of_children):
                    if i_weight == 0 or weight_a == weight_b:
                        continue
                    if i_weight == 1:
                        if weight_a != weight_b and weight_a != weights_of_children[i_weight+1]:
                            # child 0 (weight_a) is wrong
                            return self.sub_towers[0].get_corrected_weight(
                                corr_to_apply
                            )
                        else:
                            # child i (weight_b) is wrong
                            return self.sub_towers[i_weight].get_corrected_weight(
                                corr_to_apply
                            )
                    if i_weight > 1:
                        if weight_a != weight_b and weight_a != weights_of_children[i_weight-1]:
                            # child 0 (weight_a) is wrong
                            return self.sub_towers[0].get_corrected_weight(
                                corr_to_apply
                            )
                        else:
                            # child i (weight_b) is wrong
                            return self.sub_towers[i_weight].get_corrected_weight(
                                corr_to_apply
                            )

                return None

        # there is no correction to apply yet
        else:
            if not self.sub_towers:
                print('no correction and is at leaf node')
                return None

            # all my children weigh the same, but no correction
            if all([e == weights_of_children[0] for e in weights_of_children]):
                print('Returning None2. My name:', self.name)
                return None

            # 2 children, so can't know which one is wrong. Check grandchildren
            # to find out
            # out of all grandchildren, one must be wrong
            if len(self.sub_towers) == 2:
                wrong_child = None
                for i_child, child in enumerate(self.sub_towers):
                    weights_of_grandchildren = [gchild.get_total_weight() for gchild in child.sub_towers]
                    if not all([e == weights_of_grandchildren[0] for e in weights_of_grandchildren]):
                        wrong_child = i_child
                if wrong_child is None:
                    print('god help us')
                else:
                    print('here goes nothing')
                    return self.sub_towers[wrong_child].get_corrected_weight(
                        weights_of_children[(wrong_child + 1) % 2] - weights_of_children[wrong_child]
                    )

            elif len(self.sub_towers) > 2:
                # one child's weight is off and we know which one it is
                # return it's return value
                weight_a = weights_of_children[0]
                for i_weight, weight_b in enumerate(weights_of_children):
                    if i_weight == 0:
                        continue
                    if weight_a != weight_b and weight_a != weights_of_children[i_weight+1]:
                        # child 0 (weight_a) is wrong
                        return self.sub_towers[0].get_corrected_weight(
                            weight_b - weight_a
                        )
                    else:
                        # child i (weight_b) is wrong
                        return self.sub_towers[i_weight].get_corrected_weight(
                            weight_a - weight_b
                        )

                return None


def b():
    inp = get_input()
    base_tower_name = a()
    hierarchies = {}
    weights = {}
    for line in inp:
        words = line.split(' ')
        weights[words[0]] = int(words[1].removesuffix(')').removeprefix('('))

        if words[0] not in hierarchies.keys():
            hierarchies[words[0]] = []

        if len(words) > 2:
            for word in words[3:]:
                hierarchies[words[0]].append(word.removesuffix(','))

    tower = Tower(base_tower_name, hierarchies, weights)
    return tower.get_corrected_weight()

def test_a():
    assert a() == 'svugo'

def test_b():
    assert b() == 1152

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
