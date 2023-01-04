"""Entry point for TUIFIManager."""
from __future__ import annotations
# import sys                                                          # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# from os.path import dirname, abspath                                # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.insert(0, dirname(dirname(abspath(__file__))))             # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.append('..')                                               # TESTING WITH DAP
# sys.path.append('/home/xou/.local/lib/python3.10/site-packages/')   # TESTING WITH DAP
import sys
import unicurses as uc
from TUIFIManager import TUIFIManager, BEGIN_MOUSE, END_MOUSE, __version__

ESCAPE_KEY = 27


def main():
    global stdscr
    stdscr = uc.initscr()              # Global UniCurses Variable
    event  = -1

    uc.start_color  ( )
    uc.cbreak       ( )
    uc.noecho       ( )
    uc.curs_set     (0)
    uc.mouseinterval(0)                 # Initializing Mouse and then Update/refresh() stdscr
    uc.mousemask    (uc.ALL_MOUSE_EVENTS | uc.REPORT_MOUSE_POSITION) # print("\033[?1003h\n")
    uc.keypad       (stdscr, True )
    uc.nodelay      (stdscr, False)
    print           (BEGIN_MOUSE)       # Initializing mouse movement | Don't move it above because it won't work on Windows
    uc.refresh      ( )

    # Initializing TUIFIManager
    HEIGHT,WIDTH       = uc.getmaxyx(stdscr)
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    fileManager        = TUIFIManager(0,0, HEIGHT,WIDTH, (True,True,True,True), starting_directory,suffixes=['*'], is_focused=True)
    fileManager.refresh()

    while event != ESCAPE_KEY or fileManager.escape_event_consumed: # Main loop 
        event = uc.get_wch()
        fileManager.handle_events(event)
        fileManager.refresh()
        if event == uc.KEY_RESIZE:
            uc.resize_term(0,0)
    print(END_MOUSE)
    uc.endwin()


if __name__ == "__main__":
    if "-v" in sys.argv or "--version" in sys.argv:
        print(f"TUIFIManager v.{__version__}")
        exit()
    main()


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
