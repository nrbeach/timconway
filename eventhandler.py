""" EventHandler class """


from events import *
from logger import log_line


class EventHandler:
    def __init__(self, sim_event_handler, ui_event_handler):
        self._received_event_queue = []
        self._dispatch_event_queue = []
        self.sim_event_handler = sim_event_handler
        self.ui_event_handler = ui_event_handler
        self._result = None

    def dispatch_event(self, event):
        if isinstance(event, MultiStepEvent):
            self._result = None
            for step in event.steps:
                self._result = self.dispatch_event(step)

            temp = event.final(self._result)
            self.dispatch_event(temp)
        if isinstance(event, SimEvent):
            return self.sim_event_handler(event)
        if isinstance(event, UIEvent):
            return self.ui_event_handler(event)


