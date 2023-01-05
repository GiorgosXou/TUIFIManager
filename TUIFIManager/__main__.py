"""Entry point for TUIFIManager."""
from __future__ import annotations
# import sys                                                          # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# from os.path import dirname, abspath                                # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.insert(0, dirname(dirname(abspath(__file__))))             # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.append('..')                                               # TESTING WITH DAP
# sys.path.append('/home/xou/.local/lib/python3.10/site-packages/')   # TESTING WITH DAP
import sys
from typing import Final, TYPE_CHECKING

import unicurses as uc
from TUIFIManager import TUIFIManager, BEGIN_MOUSE, END_MOUSE, __version__

if TYPE_CHECKING:
    from ctypes import c_void_p

    Screen = c_void_p

ESCAPE_KEY = 27
EXIT_SUCCESS: Final[int] = 0


def init_tui() -> Screen:
    std_screen = uc.initscr()              # Global UniCurses Variable

    uc.start_color  ( )
    uc.cbreak       ( )
    uc.noecho       ( )
    uc.curs_set     (0)
    uc.mouseinterval(0)                 # Initializing Mouse and then Update/refresh() the screen
    uc.mousemask    (uc.ALL_MOUSE_EVENTS | uc.REPORT_MOUSE_POSITION) # print("\033[?1003h\n")
    uc.keypad       (std_screen, True)
    uc.nodelay      (std_screen, False)
    print           (BEGIN_MOUSE)       # Initializing mouse movement | Don't move it above because it won't work on Windows
    uc.refresh      ( )

    return std_screen


def run_file_manager(file_manager: TUIFIManager, std_screen: Screen):
    event = -1

    file_manager.refresh()
    while event != ESCAPE_KEY or file_manager.escape_event_consumed: # Main loop
        event = uc.get_wch()

        file_manager.handle_events(event)
        file_manager.refresh()

        if event == uc.KEY_RESIZE:
            uc.resize_term(0, 0)


def run_tui():
    std_screen = init_tui()
    height , width       = uc.getmaxyx(std_screen)
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    fileManager        = TUIFIManager(
        height=height, width=width,
        anchor=(True, True, True, True),
        directory=starting_directory,
        suffixes=['*'], is_focused=True
    )

    run_file_manager(fileManager, std_screen)

    print(END_MOUSE)
    uc.endwin()

def main() -> int:
    if "-v" in sys.argv or "--version" in sys.argv:
        print(f"TUIFIManager v.{__version__}")
    else:
        run_tui()
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())


# https://askubuntu.com/questions/17299/what-do-the-different-colors-mean-in-ls
# https://stackoverflow.com/questions/11753909/clean-up-ncurses-mess-in-terminal-after-a-crash
# https://stackoverflow.com/questions/35336532/ncurses-subwin-or-subpad-of-a-pad
# https://stackoverflow.com/questions/31488362/why-is-dict-faster-than-if-else-in-python
# https://stackoverflow.com/questions/18166977/cd-to-dir-after-exiting-script-system-independent-way-purely-in-python

# TODO:
"""
- Scroll sensitivity
- TERMUX start from bottom (because most mobile screens are too big)
"""
