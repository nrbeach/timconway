""" Event module """

class Event():
    def __init__(self):
        self.event_name = 'Base event'

    def __repr__(self):
        return f'{self.event_name}: {id(self)}'

class SimEvent(Event):
    def __init__(self):
        self.event_name = 'SimEvent'

class UIEvent(Event):
    def __init__(self):
        self.event_name = 'UIEvent'

class MultiStepEvent(Event):
    def __init__(self):
        self.event_name = 'MultiStepEvent'
        self.steps = []

class GetCursorPos(UIEvent):
    def __init__(self):
        self.event_name = 'GetCursorPos'
        self.x = None
        self.y = None

class CurrentCursorPos(UIEvent):
    def __init__(self, y, x):
        self.event_name = 'CurrentCursorPos'
        self.x = x
        self.y = y

class RandomFill(SimEvent):
    def __init__(self):
        self.event_name = 'RandomFill'

class FlipBit(SimEvent):
    def __init__(self, parent):
        self.event_name = 'FlipBit'
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
        self.event_name = 'CursorMove'
        self.y = y
        self.x = x

class Pause(SimEvent):
    def __init__(self):
        self.event_name = 'Pause'


class SimulationState(UIEvent):
    def __init__(self, board, iterations):
        self.event_name = 'SimulationState'
        self.board = board
        self.iterations = iterations


class ClearSimState(SimEvent):
    def __init__(self):
        self.event_name = 'ClearSimState'


