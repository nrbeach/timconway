""" Event module """

class Event():
    def __init__(self):
        self.event_name = 'eventname'

class SimEvent(Event):
    def __init__(self):
        self.event_name = 'sim event'

class UIEvent(Event):
    def __init__(self):
        self.event_name = 'UI event'

class MultiStepEvent(Event):
    def __init__(self):
        self.steps = []

class GetCursorPos(UIEvent):
    def __init__(self):
        self.x = None
        self.y = None

class CurrentCursorPos(UIEvent):
    def __init__(self, y, x):
        self.x = x
        self.y = y

class RandomFill(SimEvent):
    def __init__(self):
        self.event_name = 'Random fill'

class FlipBit(SimEvent):
    def __init__(self, parent):
        self._parent = parent
        self.y = self._parent.y - 1
        self.x = int(self._parent.x / 2)

class Toggle(MultiStepEvent):
    def __init__(self):
        self.event_name = 'Toggle'
        self.steps = [GetCursorPos()]
        self.final = FlipBit

class CursorMove(UIEvent):
    def __init__(self, y, x):
        self.event_name = 'Cursor move'
        self.y = y
        self.x = x

class Pause(SimEvent):
    def __init__(self):
        self.event_name = 'pause'

class SimulationState(UIEvent):
    def __init__(self, board, iterations):
        self.board = board
        self.iterations = iterations
