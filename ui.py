""" UI/ Game Screen class """
import curses

from constants import STATUS_SCREEN_CLEAR_V_ALIGN
from constants import STATUS_SCREEN_DEC_SIM_RATE_V_ALIGN
from constants import STATUS_SCREEN_DIR_KEYMAP_V_ALIGN
from constants import STATUS_SCREEN_FILL_V_ALIGN
from constants import STATUS_SCREEN_INC_SIM_RATE_V_ALIGN
from constants import STATUS_SCREEN_PAUSE_V_ALIGN
from constants import STATUS_SCREEN_QUIT_V_ALIGN
from constants import STATUS_SCREEN_SIM_RATE_V_ALIGN
from constants import STATUS_SCREEN_SIM_TALLY_HEADER_V_ALIGN
from constants import STATUS_SCREEN_SIM_TALLY_V_ALIGN
from constants import STATUS_SCREEN_TOGGLE_V_ALIGN
from constants import STATUS_SCREEN_VIM_KEYMAP_V_ALIGN
from eventhandler import EventHandler
from events import CurrentCursorPos
from events import CurrentSimRate
from events import CursorMove
from events import GetCursorPos
from events import SimulationState

# from logger import log_line


class GameScreen:
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
        self._reported_sim_rate = 5
        self._last_sim_state = None

    def handle_event(self, event):
        if isinstance(event, CursorMove):
            self.move_cursor(event)
        if isinstance(event, GetCursorPos):
            return self._get_cursor_pos()
        if isinstance(event, SimulationState):
            self._last_sim_state = event
            self.draw_screen(event)
        if isinstance(event, CurrentSimRate):
            self._reported_sim_rate = event.sim_rate_number
            self.draw_screen(self._last_sim_state)

    def _get_cursor_pos(self):
        cur_y, cur_x = self.stdscr.getyx()
        return CurrentCursorPos(cur_y, cur_x)

    def move_cursor(self, event):
        cur_y, cur_x = self.stdscr.getyx()
        max_y, max_x = self.screen.getmaxyx()

        new_y_pos = cur_y + event.y
        new_x_pos = cur_x + event.x
        if new_y_pos in range(1, max_y - 1) and new_x_pos in range(0, max_x - 1):
            self.stdscr.move(cur_y + event.y, cur_x + event.x)

    def draw_screen(self, event):
        self.screen.border()
        self.status_scr.border()

        for idx, row in enumerate(event.board.split("\n")):
            self.screen.addstr(idx + 1, 1, row)

        self.status_scr.addstr(STATUS_SCREEN_SIM_TALLY_HEADER_V_ALIGN, 1, f"Generation")
        self.status_scr.addstr(
            STATUS_SCREEN_SIM_TALLY_V_ALIGN, 1, f"{event.iterations}"
        )
        self.status_scr.addstr(
            STATUS_SCREEN_SIM_RATE_V_ALIGN, 1, f"Rate: {self._reported_sim_rate}/10 "
        )

        self.status_scr.addstr(STATUS_SCREEN_VIM_KEYMAP_V_ALIGN, 1, f"h, j, k, l")
        self.status_scr.addstr(
            STATUS_SCREEN_DIR_KEYMAP_V_ALIGN, 1, f"\u2190, \u2193, \u2191, \u2192"
        )
        self.status_scr.addstr(STATUS_SCREEN_INC_SIM_RATE_V_ALIGN, 1, f"+: Inc sim")
        self.status_scr.addstr(STATUS_SCREEN_DEC_SIM_RATE_V_ALIGN, 1, f"-: Dec sim")
        self.status_scr.addstr(STATUS_SCREEN_PAUSE_V_ALIGN, 1, f"p: pause")
        self.status_scr.addstr(STATUS_SCREEN_FILL_V_ALIGN, 1, f"f: fill")
        self.status_scr.addstr(STATUS_SCREEN_TOGGLE_V_ALIGN, 1, f"t: toggle")
        self.status_scr.addstr(STATUS_SCREEN_CLEAR_V_ALIGN, 1, f"c: clear sim")
        self.status_scr.addstr(STATUS_SCREEN_QUIT_V_ALIGN, 1, f"q: quit")
        self.status_scr.noutrefresh()
        self.screen.noutrefresh()
        self.stdscr.noutrefresh()
        curses.doupdate()
