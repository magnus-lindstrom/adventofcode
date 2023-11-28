def get_input():
    with open(file='inputs/1') as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    string = get_input()[0]
    summ = 0
    for i in range(len(string)):
        if string[(i+1) % len(string)] == string[i]:
            summ += int(string[i])
    return summ

def b():
    string = get_input()[0]
    summ = 0
    for i in range(len(string)):
        if string[(i+int(len(string)/2)) % len(string)] == string[i]:
            summ += int(string[i])
    return summ

def test_a():
    assert a() == 1047

def test_b():
    assert b() == 982

if __name__ == "__main__":
    print(a())
    print(b())
