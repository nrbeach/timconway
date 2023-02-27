""" Keyboard Handler """
from events import *


class KeyboardHandler:
    def __init__(self, screen):
        self._screen = screen

    def get_key(self):
        key = self._screen.getkey()
        if key == "q":
            exit(1)
        if key in ("KEY_LEFT", "h"):
            return CursorMove(0, -2)
        if key in ("KEY_RIGHT", "l"):
            return CursorMove(0, 2)
        if key in ("KEY_UP", "k"):
            return CursorMove(-1, 0)
        if key in ("KEY_DOWN", "j"):
            return CursorMove(1, 0)
        if key in ("p", "P"):
            return Pause()
        if key in ("f", "F"):
            return RandomFill()
        if key in ("t", "T"):
            return Toggle()
        if key in ("c", "C"):
            return ClearSimState()
        if key in ("+"):
            return ModifySimRate(1)
        if key in ("-"):
            return ModifySimRate(-1)
        return None
