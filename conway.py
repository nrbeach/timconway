#!/usr/bin/env python3

from random import randint, choice
import sys
import copy
from curses import wrapper
import time
SLEEP = 0.4
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
            #return f'{BOLD}*{END}'
        return '-'


    def update(self):
        live_neighbors = 0
        for neighbor in self.neighbors:
            if neighbor.bit:
                live_neighbors += 1
        if self.bit == 1 and live_neighbors < 2:
            return 0
        elif self.bit == 1 and live_neighbors >= 2 and live_neighbors <= 3:
            return self.bit
        elif self.bit == 1 and live_neighbors > 3:
            return 0
        elif self.bit == 0 and live_neighbors == 3:
            return 1
        else:
            return self.bit

class Board():
    def __init__(self, x=5, y=5):
        self.x_size = x 
        self.y_size = y
        self._pic_array = [[Cell(x, y) for x in range(self.x_size)] for y in range(self.y_size)]

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


    def draw_screen(self, screen):
        screen.clear()
        for row in self._pic_array:
            string = ''
            for cell in row:
                string += f'{cell.char} '

                #screen.addstr(cell.y, cell.x, f'{cell.char}')
            screen.addstr(cell.y, 0, string)
        screen.refresh()
    def _generate(self, iterations, screen):

        iterations_ran = 0

        new_array = [[None for _ in range(self.x_size)] for _ in range(self.y_size)]
        while iterations_ran < iterations:
            self.draw_screen(screen)
            time.sleep(SLEEP)
            for row in self._pic_array:
                for cell in row:
                    new_status = cell.update()
                    new_array[cell.y][cell.x] = new_status
            iterations_ran += 1
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

    t = Board(60, 35)
    t._pic_array[15][15].bit = 1
    t._pic_array[15][16].bit = 1
    t._pic_array[15][17].bit = 1
    t._pic_array[14][17].bit = 1
    t._pic_array[13][16].bit = 1
    t._generate(999, stdscr)

if __name__ == '__main__':
    wrapper(main)
