"""
TUItilities is a set of TUI components in ALPHA version. 
"""
import unicurses   as uc
from   dataclasses import dataclass



@dataclass
class Position:
    y    :int
    x    :int
    iy   :int = 0 # inner y
    ix   :int = 0 # inner x
    maxy :int = 0
    maxx :int = 0
    miny :int = 0
    minx :int = 0

@dataclass
class Size:
    height    :int # visible
    width     :int # visible 
    iheight   :int # inner
    iwidth    :int # inner 
    maxheight :int = 0
    maxwidth  :int = 0
    minheight :int = 0
    minwidth  :int = 0

@dataclass
class Anchor:
    top    : bool
    bottom : bool
    left   : bool
    right  : bool

class Parent:
    def __init__(self,win):
        self.win = win
        self.lines, self.columns = uc.getmaxyx(self.win)


MY_COLOR_PAIRS = (
    (uc.COLOR_WHITE  ,uc.COLOR_BLACK  ),
    (uc.COLOR_YELLOW ,uc.COLOR_BLACK  ),
    (uc.COLOR_RED    ,uc.COLOR_BLACK  ),
    (uc.COLOR_BLUE   ,uc.COLOR_BLACK  ),
    (uc.COLOR_GREEN  ,uc.COLOR_BLACK  ),
    (uc.COLOR_BLACK  ,uc.COLOR_WHITE  ),
    (uc.COLOR_BLUE   ,uc.COLOR_WHITE  ),
    (uc.COLOR_CYAN   ,uc.COLOR_BLACK  ),
    (uc.COLOR_BLACK  ,uc.COLOR_YELLOW ),
)

class Component():
    def __init__(self, win, y, x, height, width, anchor, is_focused=False, color_pair_offset=0, iheight=None, iwidth=None ) -> None:
        self.pad               = uc.newpad(height, width)
        self.parent            = Parent   (win if win else uc.stdscr)
        self.position          = Position (y, x)
        self.size              = Size     (height, width, iheight if iheight else height, iwidth if iwidth else width)
        self.anchor            = Anchor   (*anchor)
        self.is_focused        = is_focused
        self.color_pair_offset = color_pair_offset
        for i in range(1, 10):                                            # Initializing color pairs of (FOREGROUND, BACKGROUND) colors.
            if uc.pair_content(i+color_pair_offset) == (0,0):            # if it exists in some way
                uc.init_pair(i+color_pair_offset, *MY_COLOR_PAIRS[i-1] )


    def refresh(self, redraw_parent=False):
        if redraw_parent:
            uc.touchwin(self.parent.win) # Do i need this? YES
        uc.wrefresh(self.parent.win) # Do i need this? YES
        uc.prefresh(self.pad, self.position.iy, self.position.ix, self.position.y, self.position.x, self.position.y + self.size.height -1, self.position.x + self.size.width -1)


    @property #TODO: ADD descrition like use `self.position.x` instead if you don't want to redraw the `parent.win` immediately after
    def x(self): return self.position.x
    
    @x.setter
    def x(self, X): self.position.x = X; self.refresh(redraw_parent=True)

    @property
    def y(self): return self.position.y

    @y.setter
    def y(self, Y): self.position.y = Y; self.refresh(redraw_parent=True)

    @property
    def ix(self): return self.position.ix

    @ix.setter
    def ix(self, iX): self.position.ix = iX; self.refresh(redraw_parent=True)

    @property
    def iy(self): return self.position.iy

    @iy.setter
    def iy(self, iY): self.position.iy = iY; self.refresh(redraw_parent=True)

    @property
    def width(self): return self.size.width

    @width.setter
    def width(self, width): self.size.width = width; self.refresh(redraw_parent=True)

    @property
    def height(self): return self.size.height

    @height.setter
    def height(self, height): self.size.height = height; self.refresh(redraw_parent=True)


    def get_mouse(self):
        id, x, y, z, bstate = uc.getmouse() 
        in_range = True if x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height else False
        return (in_range, id, x, y, z, bstate )


    def handle_resize(self, redraw_parent=True): # TODO: max min sizes
        new_lines, new_columns = uc.getmaxyx(self.parent.win)
        if self.anchor.bottom:
            if self.anchor.top:
                self.size.height += (new_lines - self.parent.lines)
                uc.wresize(self.pad, self.height, self.width) 
            else:
                deltaY           = (new_lines - self.parent.lines)
                self.position.y  += deltaY
                # self.size.height += deltaY
        if self.anchor.right:
            if self.anchor.left:
                self.size.width += (new_columns - self.parent.columns)
                uc.wresize(self.pad, self.height, self.width) 
            else:
                deltaX           = (new_columns - self.parent.columns)
                self.position.x += deltaX
                # self.size.width += deltaX

        self.parent.lines   = new_lines
        self.parent.columns = new_columns
        if redraw_parent:
            uc.touchwin(self.parent.win)


    def handle_events(self, event, redraw_parent=True):
        if event == uc.KEY_RESIZE: self.handle_resize(redraw_parent)



class Label(Component):
    __text     = ''
    style      = uc.A_NORMAL
    color_pair = 2

    def __init__(self,y=0, x=0, height=1, width=45, anchor=(False, False, False, False), text='', color_pair_offset=0, win=None) -> None:
        super().__init__(win, y, x, height, width, anchor, color_pair_offset)
        self.text       = text


    @property
    def text(self): return self.__text

    @text.setter
    def text(self, text): 
        self.__text = text
        uc.mvwaddstr(self.pad,0,0, ' '*self.width, uc.color_pair(self.color_pair+self.color_pair_offset) | self.style ) 
        uc.mvwaddstr(self.pad,0,0, text, uc.color_pair(self.color_pair+self.color_pair_offset) | self.style ) 


    def handle_resize(self, redraw_parent=True):
        super().handle_resize(redraw_parent)
        self.text = self.__text



# THIS IS ONLY FOR TESTING PURPOSES
def main(): 
    event  = -1
    global stdscr
    stdscr = uc.initscr()  # Global UniCurses Variable

    uc.start_color( )
    uc.cbreak     ( )
    uc.noecho     ( )
    uc.curs_set   (0)

    # Initializing color pairs of (FOREGROUND, BACKGROUND) colors.
    uc.init_pair(1, uc.COLOR_WHITE  ,uc.COLOR_BLACK)
    uc.init_pair(2, uc.COLOR_YELLOW ,uc.COLOR_BLACK)
    uc.init_pair(3, uc.COLOR_RED    ,uc.COLOR_BLACK)
    uc.init_pair(4, uc.COLOR_BLUE   ,uc.COLOR_BLACK)
    uc.init_pair(5, uc.COLOR_GREEN  ,uc.COLOR_BLACK)
    uc.init_pair(6, uc.COLOR_BLACK  ,uc.COLOR_WHITE)
    uc.init_pair(7, uc.COLOR_BLUE   ,uc.COLOR_WHITE)
    uc.init_pair(8, uc.COLOR_CYAN   ,uc.COLOR_BLACK)

    # Initializing Mouse and then Update/refresh() stdscr
    uc.mouseinterval(0)
    uc.mousemask    (uc.ALL_MOUSE_EVENTS)  # | REPORT_MOUSE_POSITION); print("\033[?1003h\n")
    uc.keypad       (uc.stdscr, True)
    uc.bkgd(uc.CCHAR("#"))
    uc.refresh      ()

    # Initializing TUIFIManager
    tb = Label(anchor=(False, True, False, True))
    tc = Label(2,1,anchor=(False, True, True, True))

    while (event != 27):
        event = uc.get_wch()
        tb.handle_events(event)          
        tc.handle_events(event)          
        tb.refresh()  
        tc.refresh()
        if event == uc.KEY_RESIZE: 
            uc.resize_term(0,0)

    uc.endwin()


if __name__ == "__main__":
    main()
