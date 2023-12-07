import pathlib

individual_card_strengths = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

individual_card_strengths_with_jokers = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'T': 11,
    '9': 10,
    '8': 9,
    '7': 8,
    '6': 7,
    '5': 6,
    '4': 5,
    '3': 4,
    '2': 3,
    'J': 2,
}


def get_test_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr + '_test')
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def get_hand_strength(hand: str, joker_counting=False):
    cards = [e for e in hand]
    counts = {}
    if joker_counting:
        strength = get_individual_card_strength_of_hand_with_jokers(hand)
    else:
        strength = get_individual_card_strength_of_hand(hand)

    has_a_pair = False
    has_two_pairs = False
    has_a_triple = False

    #print('a', hand)

    for card in cards:
        if card not in counts.keys():
            counts[card] = 1
        else:
            counts[card] += 1
    #print(counts)
    for card, count in counts.items():
        if count == 5:
            return strength + 600
        elif count == 4:
            return strength + 500
        elif count == 3:
            if has_a_pair:  # full house
                return strength + 400
            else:
                has_a_triple = True
        elif count == 2:
            if has_a_pair:
                has_two_pairs = True
            elif has_a_triple:  # full house
                return strength + 400
            else:
                has_a_pair = True

    if has_a_triple:
        strength += 300
    elif has_two_pairs:
        #print('b two pairs')
        strength += 200
    elif has_a_pair:
        strength += 100

    return strength

def get_hand_strength_with_jokers(hand: str):
    cards = [e for e in hand]
    if 'J' not in cards:
        return get_hand_strength(hand, joker_counting=True)

    counts = {}
    strength = get_individual_card_strength_of_hand_with_jokers(hand)

    has_a_pair = False
    has_two_pairs = False
    has_a_triple = False
    has_four_of_a_kind = False

    for card in cards:
        if card not in counts.keys():
            counts[card] = 1
        else:
            counts[card] += 1
    #print(counts)
    for card, count in counts.items():
        if card == 'J':
            continue

        elif count == 4:
            has_four_of_a_kind = True
        elif count == 3:
            has_a_triple = True
        elif count == 2:
            if has_a_pair:
                has_two_pairs = True
            else:
                has_a_pair = True

    # we never create a two-pair hand. ToaK is always better
    if counts['J'] == 1:
        if has_four_of_a_kind:
            strength += 600
        elif has_a_triple:
            strength += 500
        elif has_two_pairs:
            strength += 400
        elif has_a_pair:
            strength += 300
        else:
            strength += 100
    elif counts['J'] == 2:
        # we never create a two-pair hand. ToaK is always better
        if has_a_triple:
            strength += 600
        elif has_a_pair:
            strength += 500
        else:
            strength += 300
    elif counts['J'] == 3:
        # we never create a two-pair hand. ToaK is always better
        if has_a_pair:
            strength += 600
        else:
            strength += 500
    else:
        # we can always make FoaK with 4 or 5 jokers
        strength += 600

    return strength

def get_individual_card_strength_of_hand(hand: str):
    strength = 0
    for i, char in enumerate(hand):
        strength += individual_card_strengths[char] / pow(100, i)
    return strength

def get_individual_card_strength_of_hand_with_jokers(hand: str):
    strength = 0
    for i, char in enumerate(hand):
        strength += individual_card_strengths_with_jokers[char] / pow(100, i)
    return strength

def order_hands_by_strength(hands: list[list[str]]):
    return hands.sort(key= lambda x: get_hand_strength(x[0]))

def a():
    inp = get_input()
    hands = []
    score = 0
    for line in inp:
        words = line.split()
        hands.append([words[0], int(words[1])])
    hands.sort(key=lambda x: get_hand_strength(x[0]))
    for i_hand, hand in enumerate(hands):
        score += (i_hand + 1) * hand[1]

    return score

def b():
    inp = get_input()
    hands = []
    score = 0
    for line in inp:
        words = line.split()
        hands.append([words[0], int(words[1])])

    hands.sort(key=lambda x: get_hand_strength_with_jokers(x[0]))

    for i_hand, hand in enumerate(hands):
        score += (i_hand + 1) * hand[1]

    return score

def test_a():
    assert a() == 253933213

def test_b():
    assert b() == 253473930

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
