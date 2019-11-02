""" Class representing simulation state """

from cell import Cell
from random import randint
from events import Pause, RandomFill, FlipBit, SimulationState

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
        if isinstance(event, FlipBit):
            self.board[event.y][event.x].flip()
        if isinstance(event, RandomFill):
            self.populate()


    def tick(self):
        return self._run_simulation()
        #yield from self._run_simulation()


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

        return SimulationState(str(self), self.iterations_ran)
        #return self.board, self.iterations_ran


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

