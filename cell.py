""" Cell class, representing state of a single cell in Conway's game of life """


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.iterations_ran = 0
        self.bit = 0

    @property
    def char(self):
        if self.bit == 1:
            return "@"
        return "-"

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
