def get_input():
    with open(file='inputs/1') as f:
        a = [line.strip() for line in f.readlines()]
    return a

def a():
    string = get_input()[0]
    sum = 0
    for i in range(len(string)):
        if string[(i+1) % len(string)] == string[i]:
            sum += int(string[i])
    return sum

def b():
    string = get_input()[0]
    sum = 0
    for i in range(len(string)):
        if string[(i+int(len(string)/2)) % len(string)] == string[i]:
            sum += int(string[i])
    return sum

if __name__ == "__main__":
    print(a())
    print(b())
