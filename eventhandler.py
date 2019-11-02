""" EventHandler class """


from events import *


class EventHandler:
    def __init__(self, sim_event_handler, ui_event_handler):
        self._received_event_queue = []
        self._dispatch_event_queue = []
        self.sim_event_handler = sim_event_handler
        self.ui_event_handler = ui_event_handler
        self._result = None

    def dispatch_event(self, event):
        if isinstance(event, MultiStepEvent):
            for step in event.steps:
                self._result = self.dispatch_event(step)
            self.dispatch_event(event.final(self._result))
        if isinstance(event, SimEvent):
            return self.sim_event_handler(event)
        if isinstance(event, UIEvent):
            return self.ui_event_handler(event)
        #if self._result:
        #    self._result = None
        #    event = self._result
        #    self.dispatch_event(event)


