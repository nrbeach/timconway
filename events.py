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
