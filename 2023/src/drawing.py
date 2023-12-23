import curses
from time import sleep


class BulkDraw:
    def __init__(self):
        self.string = ''


class Drawer:
    def __init__(self):
        self.bulk_draw_str = ''
        self.draw_list = []
        pass

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
