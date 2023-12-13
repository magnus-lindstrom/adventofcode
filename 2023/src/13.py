import pathlib


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

def find_rows_above_reflection_line(field):
    for i_line in range(len(field) - 1):
        if field[i_line] == field[i_line+1]:
            all_lines_match = True
            for j in range(1, len(field)):
                if not (0 <= i_line-j and i_line+j+1 < len(field)):
                    break
                if field[i_line-j] != field[i_line+j+1]:
                    all_lines_match = False
                    break
            if all_lines_match:
                return i_line+1
    return 0

def find_rows_above_reflection_line_b(field):
    for i_line in range(len(field) - 1):
        has_corrected = False
        # first pair of reflected rows match. One of the other reflections must
        # have an imperfection
        if field[i_line] == field[i_line+1]:
            all_lines_match = True
            for j in range(1, len(field)):
                if not (0 <= i_line-j and i_line+j+1 < len(field)):
                    break
                if field[i_line-j] != field[i_line+j+1]:
                    unequal_elements = [True for i, j in zip(field[i_line-j], field[i_line+j+1]) if i != j]
                    if (not has_corrected and len(unequal_elements) == 1):
                        has_corrected = True
                    else:
                        all_lines_match = False
                        break
            if has_corrected and all_lines_match:
                return i_line+1

        # the first reflection has an imperfection, the rest of the reflections
        # must be perfect
        elif 1 == len([True for i, j in zip(field[i_line], field[i_line+1]) if i != j]):
            all_lines_match = True
            for j in range(1, len(field)):
                if not (0 <= i_line-j and i_line+j+1 < len(field)):
                    break
                if field[i_line-j] != field[i_line+j+1]:
                    all_lines_match = False
                    break
            if all_lines_match:
                return i_line+1
    return 0

def a():
    inp = get_input()
    #inp = get_test_input()
    fields = []
    f = []
    summ = 0

    for line in inp:
        if line == '':
            fields.append(f)
            f = []
        else:
            f.append(line)
    fields.append(f)

    # transpose
    t_fields = []
    for field in fields:
        t_f = []
        for i_col in range(len(field[0])):
            string = ''
            for i_row in range(len(field)):
                string += field[i_row][i_col]
            t_f.append(string)
        t_fields.append(t_f)

    for ii in range(len(fields)):
        summ += 100 * find_rows_above_reflection_line(fields[ii])
        summ += find_rows_above_reflection_line(t_fields[ii])

    return summ

def b():
    inp = get_input()
    #inp = get_test_input()
    fields = []
    f = []
    summ = 0

    for line in inp:
        if line == '':
            fields.append(f)
            f = []
        else:
            f.append(list(line))
    fields.append(f)

    # transpose
    t_fields = []
    for field in fields:
        t_f = []
        for i_col in range(len(field[0])):
            row = []
            for i_row in range(len(field)):
                row.append(field[i_row][i_col])
            t_f.append(row)
        t_fields.append(t_f)

    for ii in range(len(fields)):
        summ += 100 * find_rows_above_reflection_line_b(fields[ii])
        summ += find_rows_above_reflection_line_b(t_fields[ii])

    return summ

def test_a():
    assert a() == 34889

def test_b():
    assert b() == 34224

if __name__ == '__main__':
    print('a:', a())
    print('b:', b())
