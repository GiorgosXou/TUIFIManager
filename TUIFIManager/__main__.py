# -*- coding: utf-8 -*-
# import sys                                               # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# from os.path import dirname, abspath                     # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149                
# sys.path.insert(0, dirname(dirname(abspath(__file__))))  # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
# sys.path.append('..')                                               # TESTING WITH DAP
# sys.path.append('/home/xou/.local/lib/python3.10/site-packages/')   # TESTING WITH DAP
from TUIFIManager import *
from unicurses    import *             
             

def main(): 
    global stdscr
    stdscr = initscr()              # Global UniCurses Variable
    event  = -1
    
    start_color  ( )
    cbreak       ( )
    noecho       ( )
    curs_set     (0)
    mouseinterval(0)                 # Initializing Mouse and then Update/refresh() stdscr
    mousemask    (ALL_MOUSE_EVENTS)  # | REPORT_MOUSE_POSITION); print("\033[?1003h\n")
    keypad       (stdscr, True)
    refresh      ( )
    
    # Initializing TUIFIManager
    HEIGHT,WIDTH       = getmaxyx(stdscr) 
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    fileManager        = TUIFIManager(0,0, HEIGHT,WIDTH, (True,True,True,True), starting_directory,suffixes=['*'], is_focused=True)
    fileManager.refresh()

    while (event != 27 or fileManager.escape_event_consumed): # Main loop exit at event/(ch)aracter 27 = ESC if not fileManager.escape_event_consumed 
        event = get_wch()
        fileManager.handle_events(event)          
        fileManager.refresh()  
        if event == KEY_RESIZE: 
            resize_term(0,0)
    endwin()


if __name__ == "__main__":
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
