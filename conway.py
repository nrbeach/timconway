#!/usr/bin/env python3

from random import randint
from curses import wrapper
from shutil import get_terminal_size
import curses
SLEEP = 0.1
BOLD = '\033[1m'
END = '\033[0m'


class Event():
    def __init__(self):
        self.event_name = 'eventname'

class SimEvent(Event):
    def __init__(self):
        self.event_name = 'sim event'

class UIEvent(Event):
    def __init__(self):
        self.event_name = 'UI event'

class RandomFill(SimEvent):
    def __init__(self):
        self.event_name = 'Random fill'

class Toggle(SimEvent):
    def __init__(self, y, x):
        self.event_name = 'Toggle'
        self.y = y
        self.x = x

class CursorMove(UIEvent):
    def __init__(self, y, x):
        self.event_name = 'Cursor move'
        self.y = y
        self.x = x

class Pause(SimEvent):
    def __init__(self):
        self.event_name = 'pause'

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.iterations_ran = 0
        self.bit = 0

    @property
    def char(self):
        if self.bit == 1:
            return '@'
        return '-'


    def flip(self):
        self.bit = abs(self.bit + -1)

    def update(self):
        live_neighbors = 0
        for neighbor in self.neighbors:
            if neighbor.bit:
                live_neighbors += 1
        if self.bit == 1 and live_neighbors < 2:
            return 0
        if self.bit == 1 and live_neighbors >= 2 and live_neighbors <= 3:
            return self.bit
        if self.bit == 1 and live_neighbors > 3:
            return 0
        if self.bit == 0 and live_neighbors == 3:
            return 1
        return self.bit

class GameState():
    def __init__(self, x=5, y=5, populate=False):
        self.x_size = x
        self.y_size = y
        self.board = [[Cell(x, y) for x in range(self.x_size)] for y in range(self.y_size)]
        if populate:
            self.populate()
        self.iterations_ran = 0
        self._paused = False
        self.find_neighbors()

    def handle_event(self, event):
        if isinstance(event, Pause):
            self._paused = not self._paused
        if isinstance(event, Toggle):
            self.board[event.y][event.x].flip()
        if isinstance(event, RandomFill):
            self.populate()
    


    def tick(self):
        yield from self._run_simulation()


    def _run_simulation(self):
        if not self._paused:
            new_array = [[None for _ in range(self.x_size)] for _ in range(self.y_size)]
            for row in self.board:
                for cell in row:
                    new_status = cell.update()
                    new_array[cell.y][cell.x] = new_status
            self.iterations_ran += 1
            for row in self.board:
                for cell in row:
                    cell.bit = new_array[cell.y][cell.x]
        return self.board, self.iterations_ran


    def find_neighbors(self):
        for row in self.board:
            for cell in row:
                if cell.y > 0: # up
                    cell.neighbors.append(self.board[cell.y - 1][cell.x])
                if cell.y > 0 and cell.x > 0: # up left
                    cell.neighbors.append(self.board[cell.y - 1][cell.x - 1])
                if cell.x > 0: # left
                    cell.neighbors.append(self.board[cell.y][cell.x - 1])
                if cell.x > 0 and cell.y < self.y_size - 1: # down left
                    cell.neighbors.append(self.board[cell.y + 1][cell.x - 1])
                if cell.y < self.y_size - 1: # down
                    cell.neighbors.append(self.board[cell.y + 1][cell.x])
                if cell.y < self.y_size - 1 and cell.x < self.x_size - 1: # down
                    cell.neighbors.append(self.board[cell.y + 1][cell.x + 1])
                if cell.x < self.x_size - 1: # down
                    cell.neighbors.append(self.board[cell.y][cell.x + 1])
                if cell.x < self.x_size - 1 and cell.y > 0: # up right
                    cell.neighbors.append(self.board[cell.y - 1][cell.x + 1])

    def populate(self, template=None):
        for row in self.board:
            for cell in row:
                cell.bit = randint(0, 1)

    def __str__(self):
        string = ''
        for row in self.board:
            for cell in row:
                string += f'{cell.char} '
            string += '\n'
        return string

    def __repr__(self):
        return self.__str__()


class GameScreen():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        term_width, term_height = get_terminal_size()
        height = term_height - 1
        width = term_width - 15
        self.screen = self.stdscr.subwin(height + 1, width, 0, 0)
        self.status_scr = self.stdscr.subwin(height + 1, 15, 0, width)
        self.stdscr.move(11, 11)
        self.screen.keypad(1)
        self.stdscr.timeout(500)

    def handle_keyboard(self):
        key = self.stdscr.getkey()
        if key == 'q':
            exit(1)
        if key == 'KEY_LEFT' or key == 'h':
            return CursorMove(0, -2)
        if key == 'KEY_RIGHT' or key == 'l':
            return CursorMove(0, 2)
        if key == 'KEY_UP' or key == 'k':
            return CursorMove(-1, 0)
        if key == 'KEY_DOWN' or key == 'j':
            return CursorMove(1, 0)
        if key == 'p' or key == 'P':
            return Pause()
        if key == 'f' or key == 'F':
            return RandomFill()
        if key == 't' or key == 'T':
            cur_y, cur_x = self.stdscr.getyx()
            cur_y = cur_y - 1
            cur_x = int(cur_x / 2)
            return Toggle(cur_y, cur_x)
        return None

    def move_cursor(self, event):
        cur_y, cur_x = self.stdscr.getyx()
        max_y, max_x = self.screen.getmaxyx()

        if cur_y + event.y > 0 and cur_y + event.y < max_y - 1 and cur_x + event.x > 0 and cur_x + event.x < max_x - 1:
            self.stdscr.move(cur_y + event.y, cur_x +event.x)

    def draw_screen(self, board, iterations):
        self.screen.border()
        self.status_scr.border()
        for row in board:
            string = ''
            for cell in row:
                string += f'{cell.char} '

            self.screen.addstr(cell.y + 1, 1, string)
        self.status_scr.addstr(1, 1, f'Generation')
        self.status_scr.addstr(2, 1, f'{iterations}')
        self.status_scr.noutrefresh()
        self.screen.noutrefresh()
        self.stdscr.noutrefresh()
        curses.doupdate()



def main(stdscr):
    curses.curs_set(2)
    stdscr.clear()

    term_width, term_height = get_terminal_size()
    height = term_height - 1
    width = term_width - 15
    t = GameState(int(width / 2) - 1, height - 1)
    #t = GameState(int(width / 2) - 1, height - 1, populate=True)
    g = GameScreen(stdscr)
    iterations = 0
    while True:
        board, iterations = t.tick()
        g.draw_screen(board, iterations)
        event = None
        try:
            event = g.handle_keyboard()
        except curses.error:
            pass
        if isinstance(event, CursorMove):
            g.move_cursor(event)
        if isinstance(event, SimEvent):
            t.handle_event(event)

if __name__ == '__main__':
    wrapper(main)
