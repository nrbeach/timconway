#!/usr/bin/env python3

from random import randint
import curses
import time
from curses import wrapper
from shutil import get_terminal_size
from constants import CPU_NICE, SIM_RATE
from events import SimEvent, UIEvent, RandomFill, Toggle, CursorMove, Pause
from keyboard_handler import KeyboardHandler
from simulation import GameState
from ui import GameScreen
from eventhandler import EventHandler




def main(stdscr):
    curses.curs_set(2)
    stdscr.clear()

    term_width, term_height = get_terminal_size()
    height = term_height - 1
    width = term_width - 15
    t = GameState(int(width / 2) - 1, height - 1)
    g = GameScreen(stdscr, height, width)
    iterations = 0
    loop_start = time.time()
    board, iterations = t.tick()
    keyboard_handler = KeyboardHandler(stdscr)
    event_handler = EventHandler(t.handle_event, g.handle_event)

    while True:
        g.draw_screen(board, iterations)
        event = None
        try:
            event = keyboard_handler.get_key()
        except curses.error:
            pass
        if event:
            event_handler.dispatch_event(event)

        loop_end = time.time()
        if loop_end - loop_start > SIM_RATE:
            board, iterations = t.tick()
            loop_start = time.time()
        time.sleep(CPU_NICE)    # sleep to avoid excessive CPU use

if __name__ == '__main__':
    wrapper(main)
