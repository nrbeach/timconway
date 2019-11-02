""" UI/ Game Screen class """

import curses
from constants import (STATUS_SCREEN_SIM_TALLY_V_ALIGN, STATUS_SCREEN_DIR_KEYMAP_V_ALIGN, STATUS_SCREEN_FILL_V_ALIGN,
                       STATUS_SCREEN_VIM_KEYMAP_V_ALIGN, STATUS_SCREEN_PAUSE_V_ALIGN, STATUS_SCREEN_TOGGLE_V_ALIGN,
                       STATUS_SCREEN_QUIT_V_ALIGN)
from events import CursorMove, Pause, RandomFill, Toggle

class GameScreen():
    def __init__(self, stdscr, height, width):
        self.stdscr = stdscr
        self._height = height
        self._width = width
        self.screen = self.stdscr.subwin(self._height + 1, self._width, 0, 0)
        self.status_scr = self.stdscr.subwin(self._height + 1, 15, 0, self._width)
        self.stdscr.move(11, 11)
        self.screen.keypad(1)
        self.stdscr.timeout(0)
        self.screen.border()
        self.status_scr.border()

    def handle_keyboard(self):
        key = self.stdscr.getkey()
        if key == 'q':
            exit(1)
        if key in ('KEY_LEFT', 'h'):
            return CursorMove(0, -2)
        if key in ('KEY_RIGHT', 'l'):
            return CursorMove(0, 2)
        if key in ('KEY_UP', 'k'):
            return CursorMove(-1, 0)
        if key in ('KEY_DOWN', 'j'):
            return CursorMove(1, 0)
        if key in ('p', 'P'):
            return Pause()
        if key in ('f', 'F'):
            return RandomFill()
        if key in ('t', 'T'):
            cur_y, cur_x = self.stdscr.getyx()
            cur_y = cur_y - 1
            cur_x = int(cur_x / 2)
            return Toggle(cur_y, cur_x)
        return None

    def move_cursor(self, event):
        cur_y, cur_x = self.stdscr.getyx()
        max_y, max_x = self.screen.getmaxyx()

        new_y_pos = cur_y + event.y
        new_x_pos = cur_x + event.x
        if new_y_pos in range(1, max_y - 1) and new_x_pos in range(0, max_x - 1):
            self.stdscr.move(cur_y + event.y, cur_x +event.x)

    def draw_screen(self, board, iterations):
        self.screen.border()
        self.status_scr.border()
        for row in board:
            string = ''
            for cell in row:
                string += f'{cell.char} '

            self.screen.addstr(cell.y + 1, 1, string)

        self.status_scr.addstr(STATUS_SCREEN_SIM_TALLY_V_ALIGN, 1, f'Generation')
        self.status_scr.addstr(STATUS_SCREEN_SIM_TALLY_V_ALIGN + 1, 1, f'{iterations}')
        self.status_scr.addstr(STATUS_SCREEN_VIM_KEYMAP_V_ALIGN, 1, f'h, j, k, l')
        self.status_scr.addstr(STATUS_SCREEN_DIR_KEYMAP_V_ALIGN, 1, f'\u2190, \u2193, \u2191, \u2192')
        self.status_scr.addstr(STATUS_SCREEN_PAUSE_V_ALIGN, 1, f'p: pause')
        self.status_scr.addstr(STATUS_SCREEN_FILL_V_ALIGN, 1, f'f: fill')
        self.status_scr.addstr(STATUS_SCREEN_TOGGLE_V_ALIGN, 1, f't: toggle')
        self.status_scr.addstr(STATUS_SCREEN_QUIT_V_ALIGN, 1, f'q: quit')
        self.status_scr.noutrefresh()
        self.screen.noutrefresh()
        self.stdscr.noutrefresh()
        curses.doupdate()

