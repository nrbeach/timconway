""" EventHandler class """
import sys

from constants import DEBUG
from events import *

# sys.path.append('/home/nate/projects/')
# from lumberjack.lumberjack import Lumberjack
#
# lj = Lumberjack('ljlog.txt')
#
#
# from logger import LJ
class EventHandler:
    def __init__(self, sim_event_handler, ui_event_handler, sim_rate_event_handler):
        self._received_event_queue = []
        self._dispatch_event_queue = []
        self.sim_event_handler = sim_event_handler
        self.ui_event_handler = ui_event_handler
        self.sim_rate_event_handler = sim_rate_event_handler
        self._result = None

    def dispatch_event(self, event):
        # if DEBUG:
        # LJ.info(event)

        if isinstance(event, MultiStepEvent):
            for step in event.steps:
                self._result = self.dispatch_event(step)

            temp = event.final(self._result)
            self.dispatch_event(temp)
        if isinstance(event, SimEvent):
            self._result = self.sim_event_handler(event)
            return self._result
        if isinstance(event, UIEvent):
            self._result = self.ui_event_handler(event)
            return self._result
        if isinstance(event, SimRateEvent):
            self._result = self.sim_rate_event_handler(event)
            return self._result
        if self._result:
            self.dispatch_event(self._result)
