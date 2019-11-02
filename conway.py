#!/usr/bin/env python3

from random import randint
import curses
import time
from curses import wrapper
from shutil import get_terminal_size
from constants import CPU_NICE, DEBUG, SIM_RATE
from keyboard_handler import KeyboardHandler
from simulation import GameState
from ui import GameScreen
from eventhandler import EventHandler

from datetime import datetime
from logger import log_line



def main(stdscr):
    if DEBUG:
        log_line(f'===== {datetime.now()} =====')
    curses.curs_set(2)
    stdscr.clear()

    term_width, term_height = get_terminal_size()
    height = term_height - 1
    width = term_width - 15
    t = GameState(int(width / 2) - 1, height - 1)
    g = GameScreen(stdscr, height, width)
    loop_start = time.time()
    #board, iterations = t.tick()
    event = t.tick()
    keyboard_handler = KeyboardHandler(stdscr)
    event_handler = EventHandler(t.handle_event, g.handle_event)
    event_handler.dispatch_event(event)

    while True:
        #g.draw_screen(board, iterations)
        event = None
        try:
            event = keyboard_handler.get_key()
        except curses.error:
            pass
        if event:
            event_handler.dispatch_event(event)

        loop_end = time.time()
        if loop_end - loop_start > SIM_RATE:
            event = t.tick()
            event_handler.dispatch_event(event)
            loop_start = time.time()
        time.sleep(CPU_NICE)    # sleep to avoid excessive CPU use

if __name__ == '__main__':
    wrapper(main)
