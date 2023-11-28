import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    phrases = get_input()
    summ = 0
    for phrase in phrases:
        word_list = phrase.split()
        word_set = set(word_list)
        if len(word_set) == len(word_list):
            summ += 1
    return summ

def b():
    phrases = get_input()
    summ = 0
    for phrase in phrases:
        are_equal = True
        word_sets = []
        for word in phrase.split():
            word_sets.append(set(word))
        for i_set1, word_set1 in enumerate(word_sets):
            for word_set2 in word_sets[i_set1+1:]:
                if word_set1 == word_set2:
                    are_equal = False
        if are_equal:
            summ += 1
    return summ

def test_a():
    assert a() == 451

def test_b():
    assert b() == 223

if __name__ == "__main__":
    print('a:', a())
    print('b:', b())
