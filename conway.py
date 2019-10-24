#!/usr/bin/env python3

from random import randint, choice
import sys
import copy
from curses import wrapper
from shutil import get_terminal_size
import curses
import time
SLEEP = 0.1
BOLD = '\033[1m'
END = '\033[0m'


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.bit = 0

    @property
    def char(self):
        if self.bit == 1:
            return '@'
        return '-'


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

class Board():
    def __init__(self, x=5, y=5):
        self.x_size = x
        self.y_size = y
        self._pic_array = [[Cell(x, y) for x in range(self.x_size)] for y in range(self.y_size)]
        self.iterations_ran = 0
        self.find_neighbors()

    def find_neighbors(self):
        for row in self._pic_array:
            for cell in row:
                # up
                if cell.y > 0:
                    cell.neighbors.append(self._pic_array[cell.y - 1][cell.x])
                # up left
                if cell.y > 0 and cell.x > 0:
                    cell.neighbors.append(self._pic_array[cell.y - 1][cell.x - 1])
                # left:
                if cell.x > 0:
                    cell.neighbors.append(self._pic_array[cell.y][cell.x - 1])
                # down left:
                if cell.x > 0 and cell.y < self.y_size - 1:
                    cell.neighbors.append(self._pic_array[cell.y + 1][cell.x - 1])
                # down
                if cell.y < self.y_size - 1:
                    cell.neighbors.append(self._pic_array[cell.y + 1][cell.x])
                # down right
                if cell.y < self.y_size - 1 and cell.x < self.x_size - 1:
                    cell.neighbors.append(self._pic_array[cell.y + 1][cell.x + 1])
                # right
                if cell.x < self.x_size - 1:
                    cell.neighbors.append(self._pic_array[cell.y][cell.x + 1])
                # up right
                if cell.x < self.x_size - 1 and cell.y > 0:
                    cell.neighbors.append(self._pic_array[cell.y - 1][cell.x + 1])

    def populate(self):
        for row in self._pic_array:
            for cell in row:
                cell.bit = randint(0, 1)

    def handle_keyboard(self, key):
        if key == 'q':
            exit(1)
        if key == curses.KEY_LEFT or key == 'h':
            return (0, -2)
        if key == curses.KEY_RIGHT or key == 'l':
            return (0, 2)
        if key == curses.KEY_UP or key == 'k':
            return (-1, 0)
        if key == curses.KEY_DOWN or key == 'j':
            return (1, 0)
        return (1, 1)

    def draw_screen(self, screen, status_scr):
        screen.clear()
        screen.border()
        screen.keypad(True)
        screen.leaveok(False)
        status_scr.clear()
        status_scr.border()
        cur_y, cur_x = curses.getsyx()
        for row in self._pic_array:
            string = ''
            for cell in row:
                string += f'{cell.char} '

            screen.addstr(cell.y + 1, 1, string)
            #screen.addstr(cell.y, 0, string)

        mov_y, mov_x = self.handle_keyboard(screen.getkey())
        status_scr.addstr(1, 1, f'Generation')
        status_scr.addstr(2, 1, f'{self.iterations_ran}')
        status_scr.addstr(3, 1, f'{cur_y}, {cur_x}')
        screen.move(cur_y + mov_y, cur_x + mov_x)
        screen.cursyncup()
        status_scr.noutrefresh()
        screen.noutrefresh()
        curses.doupdate()

    def _generate(self, iterations, screen, status_scr):

        self.iterations_ran = 0

        new_array = [[None for _ in range(self.x_size)] for _ in range(self.y_size)]
        while self.iterations_ran < iterations:
            self.draw_screen(screen, status_scr)
            time.sleep(SLEEP)
            for row in self._pic_array:
                for cell in row:
                    new_status = cell.update()
                    new_array[cell.y][cell.x] = new_status
            self.iterations_ran += 1
            for row in self._pic_array:
                for cell in row:
                    cell.bit = new_array[cell.y][cell.x]


    def __str__(self):
        string = ''
        for row in self._pic_array:
            for cell in row:
                string += f'{cell.char} '
            string += '\n'
        return string

    def __repr__(self):
        return self.__str__()


def main(stdscr):
    stdscr.clear()

    term_width, term_height = get_terminal_size()
    height = term_height - 1
    width = term_width - 15
    board_scr = curses.newwin(height + 1, width, 0, 0)
    status_scr = curses.newwin(height + 1, 15, 0, width)
    t = Board(int(width / 2) - 1, height - 1)
    t.populate()
    t._generate(999, board_scr, status_scr)
    #t._generate(999, stdscr)

if __name__ == '__main__':
    wrapper(main)
