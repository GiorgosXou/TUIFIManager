"""Entry point for TUIFIManager."""
from __future__ import annotations

import sys
import unicurses as uc

from TUIFIManager import TUIFIManager, BEGIN_MOUSE, END_MOUSE, __version__
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ctypes import c_void_p
    from typing import Final

    Screen = c_void_p

ESCAPE_KEY: Final[int] = 27


def setup_curses_screen() -> Screen:
    std_scr = uc.initscr()
    uc.start_color()
    uc.cbreak()
    uc.noecho()
    uc.curs_set(0)

    # Initializing Mouse and then Update/refresh() std screen
    uc.mouseinterval(0)
    uc.mousemask(uc.ALL_MOUSE_EVENTS | uc.REPORT_MOUSE_POSITION)
    uc.keypad(std_scr, True)
    uc.nodelay(std_scr, False)

    # Initializing mouse movement | Don't move it above because it won't work on Windows
    print(BEGIN_MOUSE)
    uc.refresh()
    return std_scr


def close_curses_screen():
    print(END_MOUSE)
    uc.endwin()


def start_tuifi():
    std_scr = setup_curses_screen()
    height, width = uc.getmaxyx(std_scr)
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    file_manager = TUIFIManager(
        height=height, width=width,
        anchor=(True, True, True, True),
        directory=starting_directory,
        suffixes=['*'],
        is_focused=True
    )

    run_tuifi(file_manager)
    close_curses_screen()


def run_tuifi(file_manager: TUIFIManager):
    event: int = -1

    file_manager.refresh()
    while event != ESCAPE_KEY or file_manager.escape_event_consumed:  
        event = uc.get_wch()
        file_manager.handle_events(event)
        file_manager.refresh()

        if event == uc.KEY_RESIZE:
            uc.resize_term(0, 0)


def main():
    if "-v" in sys.argv or "--version" in sys.argv:
        print(f"TUIFIManager v{__version__}")
    else:
        start_tuifi()
