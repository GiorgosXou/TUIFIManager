# import sys                                                          # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# from os.path import dirname, abspath                                # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.insert(0, dirname(dirname(abspath(__file__))))             # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.append('..')                                               # TESTING WITH DAP
# sys.path.append('/home/xou/.local/lib/python3.10/site-packages/')   # TESTING WITH DAP

"""Entry point for TUIFIManager."""
from __future__ import annotations

import sys
import unicurses    as uc
from   TUIFIManager import TUIFIManager, BEGIN_MOUSE, END_MOUSE, __version__
from   typing       import TYPE_CHECKING


if TYPE_CHECKING:
    from ctypes import c_void_p
    from typing import Final
    Screen = c_void_p

ESCAPE_KEY: Final[int] = 27


def setup_curses_screen() -> Screen:
    global stdscr
    stdscr = uc.initscr()
    uc.start_color( )
    uc.cbreak     ( )
    uc.noecho     ( )
    uc.curs_set   (0)

    uc.mouseinterval(0) # Initializing Mouse and then Update/refresh() std screen
    uc.mousemask    (uc.ALL_MOUSE_EVENTS | uc.REPORT_MOUSE_POSITION)
    uc.keypad       (stdscr, True )
    uc.nodelay      (stdscr, False)
    print           (BEGIN_MOUSE) # Initializing mouse movement | Don't move it above because it won't work on Windows
    
    uc.refresh()


def close_curses_screen():
    print    (END_MOUSE)
    uc.endwin()


def start_tuifi():
    setup_curses_screen()
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    height, width  = uc.getmaxyx (stdscr)
    file_manager   = TUIFIManager(
        height     = height                  , 
        width      = width                   ,
        anchor     = (True, True, True, True),
        directory  = starting_directory      ,
        suffixes   = ['*']                   ,
        is_focused = True
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
