# -*- coding: utf-8 -*-
#import sys                                               # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
#from os.path import dirname, abspath                     # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149                
#sys.path.insert(0, dirname(dirname(abspath(__file__))))  # TESTING: UNCOMMENT TO USE LOCAL PACKAGE (./__init__.py) | https://stackoverflow.com/a/25888670/11465149
from TUIFIManager import *
from unicurses import *             
             

def main(): 
    event  = -1
    global stdscr
    stdscr = initscr()  # Global UniCurses Variable
    
    start_color( )
    cbreak     ( )
    noecho     ( )
    curs_set   (0)
    
    # Initializing color pairs of (FOREGROUND, BACKGROUND) colors.
    init_pair(1, COLOR_WHITE  ,COLOR_BLACK)
    init_pair(2, COLOR_YELLOW ,COLOR_BLACK)
    init_pair(3, COLOR_RED    ,COLOR_BLACK)
    init_pair(4, COLOR_BLUE   ,COLOR_BLACK)
    init_pair(5, COLOR_GREEN  ,COLOR_BLACK)
    init_pair(6, COLOR_BLACK  ,COLOR_WHITE)
    init_pair(7, COLOR_BLUE   ,COLOR_WHITE)
    init_pair(8, COLOR_CYAN   ,COLOR_BLACK)
    
    # Initializing Mouse and then Update/refresh() stdscr
    mouseinterval(0)
    mousemask    (ALL_MOUSE_EVENTS)  # | REPORT_MOUSE_POSITION); print("\033[?1003h\n")
    keypad       (stdscr, True)
    refresh      ()
    
    # Initializing TUIFIManager
    tLINES,tCOLS       = getmaxyx(stdscr) 
    fileManagerPad     = newpad(tLINES, tCOLS)
    starting_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    fileManager        = TUIFIManager(fileManagerPad,0,0,True,True,True,True,starting_directory)  # Use suffixes=['*','.*'] for hidden files 
    fileManager.refresh()

    # Main loop exit at event/(ch)aracter 27 = ESC if not fileManager.is_on_reaname_mode 
    while (event != 27 or fileManager.is_on_reaname_mode):
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
# https://stackoverflow.com/questions/31488362/
    