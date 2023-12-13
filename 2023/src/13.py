import pathlib


def get_input():
    q_nr = pathlib.Path(__file__).stem
    file_name = pathlib.Path('inputs/' + q_nr)
    with open(file=file_name) as f:
        return [line.strip() for line in f.readlines()]

def find_rows_above_reflection_line(field, max_corrections=0):
    for i_line in range(len(field) - 1):
        corrections_made = 0
        all_lines_match = True
        for j in range(0, len(field)):
            if not (0 <= i_line-j and i_line+j+1 < len(field)):
                break
            if field[i_line-j] != field[i_line+j+1]:
                if corrections_made < max_corrections:
                    unequal_elements = [True for i, j in zip(field[i_line-j], field[i_line+j+1]) if i != j]
                    if len(unequal_elements) == 1:
                        corrections_made += 1
                    else:
                        all_lines_match = False
                        break
                else:
                    all_lines_match = False
                    break
        if corrections_made == max_corrections and all_lines_match:
            return i_line+1

    return 0

def task(max_corrections):
    inp = get_input()
    fields = []
    field = []
    summ = 0

    for line in inp:
        if line == '':
            fields.append(field)
            field = []
        else:
            field.append(list(line))
    fields.append(field)

    # transpose
    t_fields = []
    for field in fields:
        t_field = []
        for i_col in range(len(field[0])):
            row = []
            for i_row in range(len(field)):
                row.append(field[i_row][i_col])
            t_field.append(row)
        t_fields.append(t_field)

    for ii in range(len(fields)):
        summ += 100 * find_rows_above_reflection_line(
            fields[ii], max_corrections=max_corrections
        )
        summ += find_rows_above_reflection_line(
            t_fields[ii], max_corrections=max_corrections
        )

    return summ

def a():
    return task(max_corrections=0)

def b():
    return task(max_corrections=1)

def test_a():
    assert a() == 34889

def test_b():
    assert b() == 34224

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
