""" Simple logging facilities """

from inspect import currentframe, getframeinfo
from enum import Enum
from pathlib import Path
import sys
sys.path.append('/home/nate/projects/lumberjack')
from lumberjack.lumberjack import Lumberjack

LJ = Lumberjack('ljz.txt')

def get_line_number():
    cf = currentframe()
    return cf.f_back.f_back.f_lineno

def get_filename():
    cf = currentframe()
    return getframeinfo(cf.f_back.f_back).filename


def get_function():
    cf = currentframe()
    return getframeinfo(cf.f_back.f_back).function

def get_class_name():
    cf = currentframe()
    try:
        cls = cf.f_back.f_back.f_locals['self'].__class__
        return cls.__name__
    except KeyError:
        return None

class LogLevel(Enum):
    info = 0
    debug = 1
    warning = 2
    fatal = 3

class Line:
    def __init__(self, msg=None, log_level=0):
        self.log_level = LogLevel(log_level)
        self.msg = msg
        self.loc = get_line_number()
        self._path = get_filename()
        self.filename = Path(self._path).stem   # or use .name for full filename
        self.function = get_function()
        self._class_name = get_class_name()

    def __str__(self):
        return f'[{self.log_level.name.upper()}] {self.filename}.{self.class_name}{self.function}() #{self.loc}: {self.msg}'

    @property
    def class_name(self):
        if self._class_name:
            return f'{self._class_name}.'
        return ''

def log_line(line):
    line = str(line)
    if line[-1] != '\n':
        line += '\n'

    with open('log.txt', 'a') as fh:
        fh.write(line)
