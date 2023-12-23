import curses
from abc import ABC, abstractmethod
from time import sleep


class DrawBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, stdscr):
        pass

class BulkDraw(DrawBase):
    def __init__(self, string='', column=0, row=0, sleep_sec=0,
                 keypress_after=False):
        self.string = string
        self.column = column
        self.row = row
        self.sleep = sleep_sec
        self.keypress_after = keypress_after

    def set_position(self, row, column):
        self.row = row
        self.column = column

    def add_to_str(self, string):
        self.string += string

    def add_sleep_after(self, sleep_sec):
        self.sleep = sleep_sec

    def draw(self, stdscr):
        stdscr.addstr(self.row, self.column, self.string)
        if self.sleep:
            stdscr.refresh()
            sleep(self.sleep)
        if self.keypress_after:
            stdscr.getch()


class CharSeqDraw(DrawBase):
    def __init__(self, chars=None, rows=None, columns=None,
                 keypress_after=False):
        if not chars is None and not rows is None and not columns is None:
            self.chars = chars
            self.rows = rows
            self.columns = columns
        else:
            self.chars = []
            self.rows = []
            self.columns = []
        self.keypress_after = keypress_after
        self.time = 0.0
        self.colors = []

    def add_char(self, char, row, col, color=0):
        self.chars.append(char)
        self.rows.append(row)
        self.columns.append(col)
        self.colors.append(color)

    def set_total_sleep(self, sleep_sec):
        self.sleep = sleep_sec / len(self.chars)

    def set_individual_sleep(self, sleep_sec):
        self.sleep = sleep_sec

    def draw(self, stdscr, required_color_pairs):
        for char, row, col, color in zip(self.chars, self.rows, self.columns,
                                         self.colors):
            if (row, col) in required_color_pairs:
                stdscr.addch(
                    row, col, char,
                    curses.color_pair(required_color_pairs[(row, col)])
                )
            else:
                stdscr.addch(row, col, char, curses.color_pair(color))

            if self.sleep > 0:
                stdscr.refresh()
                sleep(self.sleep)
        if self.keypress_after:
            stdscr.getch()

class Drawer:
    def __init__(self):
        self.bulk_draw_str = ''
        self.draw_list = []
        self.draw_elements: list[DrawBase] = []
        self.color_pairs = []
        self.position_colors = {}

    def add_draw_element(self, element: DrawBase):
        self.draw_elements.append(element)

    def require_color_pair_for_pos(self, color_pair, row, col):
        self.position_colors[(row, col)] = color_pair

    def clear_draw_elements(self):
        self.draw_elements = []

    def get_curses_color(self, color):
        if color == 'black':
            return curses.COLOR_BLACK
        elif color == 'white':
            return curses.COLOR_WHITE
        elif color == 'red':
            return curses.COLOR_RED
        elif color == 'green':
            return curses.COLOR_GREEN
        elif color == 'yellow':
            return curses.COLOR_YELLOW
        elif color == 'blue':
            return curses.COLOR_BLUE
        else:
            raise Exception('Could not find color')

    def set_color_pair(self, foreground, background):
        fore_real = self.get_curses_color(foreground)
        back_real = self.get_curses_color(background)
        self.color_pairs.append((back_real, fore_real))

    def draw_draw_elements(self):
        def main(stdscr):
            curses.curs_set(0)  # make cursor invisible
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
            curses.use_default_colors()
            for element in self.draw_elements:
                if type(element) == CharSeqDraw:
                    element.draw(stdscr, self.position_colors)
                else:
                    element.draw(stdscr)

        curses.wrapper(main)

    def check_window_dimensions(self, inp):
        def main(stdscr):
            rows, cols = stdscr.getmaxyx()
            s = '({}, {}) (probably) needed, current window is ({}, {}).'.format(
                len(inp), len(inp[0]), rows, cols
            )
            stdscr.addstr(0, 0, s)
            stdscr.refresh()
            stdscr.getch()

        curses.wrapper(main)
    def position_is_valid(self, row, col):
        def main(stdscr, row, col):
            rows, cols = stdscr.getmaxyx()
            if row >= rows or col >= cols:
                s1 = 'Too small window. Need {} rows and {} cols to draw'.format(
                    row, col
                )
                stdscr.addstr(0, 0, s1)
                stdscr.refresh()
                stdscr.getch()
                return False
            return True

        return curses.wrapper(main, row, col)

    def draw_char(self, char, row=0, col=0, await_keypress=False, refresh_after=False):
        def main(stdscr):
            #hide_cursor()
            stdscr.addch(row, col, char)
            if refresh_after:
                stdscr.refresh()
            if await_keypress:
                stdscr.getch()

        if not self.position_is_valid(row, col):
            raise curses.error

        curses.wrapper(main)

    def draw_str(self, string, row=0, col=0, await_keypress=False, refresh_after=False):
        def main(stdscr):
            #hide_cursor()
            stdscr.addstr(row, col, string)
            if refresh_after:
                stdscr.refresh()
            if await_keypress:
                stdscr.getch()

        if not self.position_is_valid(row, col):
            raise curses.error

        curses.wrapper(main)

    def hide_cursor(self):
        curses.curs_set(0)

    def wait_for_keypress(self):
        def main(stdscr):
            stdscr.getch()
        curses.wrapper(main)

    def refresh(self):
        def main(stdscr):
            stdscr.refresh()
        curses.wrapper(main)

    def clear(self):
        def main(stdscr):
            stdscr.clear()
        curses.wrapper(main)

    def clear_bulk_draw(self):
        self.bulk_draw_str = ''

    def bulk_str_add(self, string):
        self.bulk_draw_str += string

    def bulk_draw(self, row=0, col=0, sleep_sec=0.0):
        def main(stdscr):
            curses.curs_set(0)  # hide cursor
            stdscr.addstr(row, col, self.bulk_draw_str)
            if sleep_sec:
                stdscr.refresh()
                sleep(sleep_sec)

        curses.wrapper(main)

    def char_list_clear(self):
        self.draw_list = []

    def char_list_push(self, char, row, col):
        self.draw_list.append((char, row, col))

    def char_list_draw(self, sleep_sec=0.0, sleep_sec_total=0.0):
        def main(stdscr):
            for char, row, col in self.draw_list:
                stdscr.addstr(row, col, char)
                if sleep_sec_total > 0:
                    stdscr.refresh()
                    sleep(sleep_sec_total / len(self.draw_list))
                if sleep_sec > 0:
                    stdscr.refresh()
                    sleep(sleep_sec)

        curses.wrapper(main)
