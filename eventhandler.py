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
        #log_line(f'begin dispatch_event(), {event}')
        if isinstance(event, MultiStepEvent):
            #self._result = None
            for step in event.steps:
                self._result = self.dispatch_event(step)

            temp = event.final(self._result)
            #log_line(f'MultiStepEvent: {temp}')
            self.dispatch_event(temp)
        if isinstance(event, SimEvent):
            self._result = self.sim_event_handler(event)
        #    log_line(f'SimEvent: {self._result}')
            return self._result
        if isinstance(event, UIEvent):
            self._result = self.ui_event_handler(event)
        #    log_line(f'UI: {self._result}')
            return self._result
        if self._result:
        #    log_line(f'self._result dispatch: {self._result}')
            self.dispatch_event(self._result)


