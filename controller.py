""" Class to control sim rate """

from constants import SIM_RATE
from events import IncreaseSimRate, DecreaseSimRate, CurrentSimRate


class SimulationRate:
    def __init__(self):
        self._rates = {
            1: 1,
            2: 0.81375,
            3: 0.6275,
            4: 0.44125,
            5: SIM_RATE,
            6: 0.204,
            7: 0.153,
            8: 0.102,
            9: 0.051,
            10: 0,
        }

        self._current_rate_number = 5
        self._current_rate = SIM_RATE

    @property
    def sim_rate(self):
        return self._current_rate

    def _update_sim_rate(self, val):
        diff = self._current_rate_number + val
        if diff >= 1 and diff <= 10:
            self._current_rate_number = diff
            self._current_rate = self._rates[self._current_rate_number]

    def handle_event(self, event):
        if isinstance(event, IncreaseSimRate):
            self._update_sim_rate(1)
            return self._current_rate_number
        if isinstance(event, DecreaseSimRate):
            self._update_sim_rate(-1)
            return self._current_rate_number
