"""
TUItilities is a set of TUI components and terminal utilities in ALPHA version (They will be exported to a new package).
"""
import   unicurses as uc
import  subprocess
import   threading
from   dataclasses import dataclass
from       os.path import isfile
from        shutil import which
from         pipes import quote
from          time import sleep
from            os import getenv, getcwd


lock = threading.Lock()


# ======================== ========== ========================
#                          -UTILITIES                         
# ======================== ========== ========================
BEGIN_MOUSE = "\033[?1003h"
END_MOUSE   = "\033[?1003l"

IS_MACOS            = uc.OPERATING_SYSTEM == 'Darwin'
IS_WINDOWS          = uc.OPERATING_SYSTEM == 'Windows'
HOME_DIR            = getenv('UserProfile') if IS_WINDOWS else getenv('HOME')
SHELL               = getenv('SHELL') # https://stackoverflow.com/a/35662469/11465149 | https://superuser.com/questions/1515578/
IS_TERMUX           = 'com.termux' in HOME_DIR
DEFAULT_BACKGROUND  =  -1 if getenv('tuitilities_default_background') == 'True' else uc.COLOR_BLACK
COPY_APP = (
    ["pbcopy"] if IS_MACOS else
    ["clip"] if IS_WINDOWS else
    ["termux-clipboard-set"] if IS_TERMUX else
    ["xclip", "-sel", "clipboard"] if which("xclip") else
    ["wl-copy"] if which("wl-copy") else None
)



class Cd: # https://stackoverflow.com/a/16694919/11465149
    directory  = HOME_DIR 
    perform_cd = True

    def quote_against_shell_expansion(self, s):
        return quote(s)

    def put_text_back_into_terminal_input_buffer(self, text):
        from termios import TIOCSTI
        from   fcntl import ioctl 
        for c in text: ioctl(1, TIOCSTI, c)

    def cd(self, dest): # change_parent_process_directory
        self.put_text_back_into_terminal_input_buffer("cd "+self.quote_against_shell_expansion(dest)+"\n")

    def __del__(self):
        if self.perform_cd and not IS_WINDOWS and not self.directory == getcwd():
             self.cd(self.directory)



def clipboard(text:str):
    if COPY_APP:
        try:
            subprocess.run(COPY_APP, input=text, universal_newlines=True, check=True)
            return True
        except Exception as e:
            return False
    else:
        return False



# ======================== ========== ========================
#                          COMPONENTS                         
# ======================== ========== ========================
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



# # mapping function values 0-255 to 0-1000
# C = lambda x: int((x - 0) * (1000 - 0) / (255 - 0) + 0)

MY_COLOR_PAIRS = (
    (uc.COLOR_BLACK  ,uc.COLOR_WHITE    ),
    (uc.COLOR_BLUE   ,uc.COLOR_WHITE    ),
    (uc.COLOR_WHITE  ,DEFAULT_BACKGROUND),
    (uc.COLOR_YELLOW ,DEFAULT_BACKGROUND),
    (uc.COLOR_RED    ,DEFAULT_BACKGROUND),
    (uc.COLOR_BLUE   ,DEFAULT_BACKGROUND),
    (uc.COLOR_GREEN  ,DEFAULT_BACKGROUND),
    (uc.COLOR_CYAN   ,DEFAULT_BACKGROUND),
    (uc.COLOR_YELLOW ,DEFAULT_BACKGROUND), # I'll keep it extra for ui
)

# Might need  TODO:  setters for dimming and bold effects because of this custom color theming thing....

# due to https://invisible-island.net/ncurses/man/curs_color.3x.html#:~:text=default%20colors%20are%0A%20%20%20%20%20%20%20%20%20%20%20not%20allowed%20here.
EFFECTS_OFFSET = 82 # ^^^ (255-8) / 3 where 247 = Available colors... and for a good reason, if you use A_BOLD with an initialized color between 0-7 you get the wrong color in some terminal eg. XTerm, Kitty... but not alacritty
DIM__OFFSET = EFFECTS_OFFSET*2
BOLD_OFFSET = EFFECTS_OFFSET

custom_colorscheme = False


def has_custom_colorscheme():
    return custom_colorscheme


def __DIM1 (pair_num): return uc.A_NORMAL , pair_num + DIM__OFFSET # DIM  FOR CUSTOM COLORSCHEMES
def __BOLD1(pair_num): return uc.A_BOLD   , pair_num + BOLD_OFFSET # BOLD FOR CUSTOM COLORSCHEMES
def __DIM2 (pair_num): return uc.A_DIM    , pair_num
def __BOLD2(pair_num): return uc.A_BOLD   , pair_num

__dim  = __DIM2
__bold = __BOLD2

def DIM(pair_num): return __dim (pair_num)
def BLD(pair_num): return __bold(pair_num) # NOTE: BRIGHT BOLD NOT JUST BOLD


def color_pair_with_effect2(pair, style): return uc.COLOR_PAIR(pair) | style # this is when theres no custom_colorscheme
def color_pair_with_effect1(pair, style): # you can't have both bold and dim so i don't count for it
    # if (style | uc.A_BOLD == style): return uc.COLOR_PAIR(pair) | style # (uc.COLOR_PAIR(pair+BOLD_OFFSET) | (style)) # we want A_BOLD so we don't subtract it
    if (style | uc.A_DIM  == style): return (uc.COLOR_PAIR(pair+DIM__OFFSET) | (style-uc.A_DIM))
    return uc.color_pair(pair) | style

color_pair_with_effect = color_pair_with_effect2


initialized = False # Initializing color pairs of (FOREGROUND, BACKGROUND) colors.
def toggle_colorsheme_initialization():
    global initialized , custom_colorscheme
    initialized = not initialized
    custom_colorscheme = not custom_colorscheme


def init_colorscheme(colorscheme_path, light=False):
    if not isfile(colorscheme_path) or custom_colorscheme :return # meaning if colorscheme_path doesn't exist OR a custom_colorscheme has already been initialized by another app
    toggle_colorsheme_initialization()
    with open(colorscheme_path, 'r') as file:
        bold_offset = BOLD_OFFSET
        dim__offset = DIM__OFFSET
        if light:
            bold_offset = DIM__OFFSET
            dim__offset = BOLD_OFFSET
        global __dim, __bold, color_pair_with_effect
        color_pair_with_effect = color_pair_with_effect1
        __dim  = __DIM1
        __bold = __BOLD1

        # Initialize background at 0
        rgb = file.__next__().strip().split(',')
        r,g,b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        uc.init_color(uc.COLOR_BLACK, r, g, b) # which is the uc.COLOR_BLACK

        for i, ln in enumerate(file, start=8):
            rgb = ln.strip().split(',')
            r,g,b = int(rgb[0]), int(rgb[1]), int(rgb[2]) 
            uc.init_color(i, r, g, b)
            uc.init_color(i+dim__offset, r-200 if r-200 >= 0 else 0,g-200 if g-200 >= 0 else 0,b-200 if b-200 >= 0 else 0) # A_DIM
            uc.init_color(i+bold_offset, r+200 if r+200 <= 1000 else 1000,g+200 if g+200 <= 1000 else 1000,b+200 if b+200 <= 1000 else 1000) # A_BOLD
            uc.init_pair(i-7 ,i  ,DEFAULT_BACKGROUND)
            uc.init_pair(i+bold_offset-7,i+bold_offset,DEFAULT_BACKGROUND)
            uc.init_pair(i+dim__offset-7,i+dim__offset,DEFAULT_BACKGROUND)
        f1,_ = uc.pair_content(1)
        f2,_ = uc.pair_content(2)
        uc.init_pair(1  ,f1  , 17)
        uc.init_pair(2  ,f2  , 18)


def initialize_colors():
    global initialized 
    if initialized: return
    # if MY_COLORS:
    #     for i in range(0, len(MY_COLORS)):
    #         uc.init_color(i+1, *MY_COLORS[i])
    for i in range(0, len(MY_COLOR_PAIRS)): # if uc.pair_content(i) in ((0,0),(7,0)): # if it exists in some way already | also TODO: https://github.com/GiorgosXou/TUIFIManager/issues/48
        uc.init_pair(i+1 , *MY_COLOR_PAIRS[i] )
    initialized = True



@dataclass
class Border: # TODO: Make clear and draw availabe both for Drawables and WindowPads
    left                : int = uc.ACS_VLINE
    right               : int = uc.ACS_VLINE
    top                 : int = uc.ACS_HLINE
    bottom              : int = uc.ACS_HLINE
    top_left_corner     : int = uc.ACS_ULCORNER
    top_right_corner    : int = uc.ACS_URCORNER
    bottom_left_corner  : int = uc.ACS_LLCORNER
    bottom_right_corner : int = uc.ACS_LRCORNER

    def __post_init__(self):
        self.left                = uc.CCHAR(self.left               )
        self.right               = uc.CCHAR(self.right              )
        self.top                 = uc.CCHAR(self.top                )
        self.bottom              = uc.CCHAR(self.bottom             )
        self.top_left_corner     = uc.CCHAR(self.top_left_corner    )
        self.top_right_corner    = uc.CCHAR(self.top_right_corner   )
        self.bottom_left_corner  = uc.CCHAR(self.bottom_left_corner )
        self.bottom_right_corner = uc.CCHAR(self.bottom_right_corner)

    def clear(self, win): uc.wborder(win, uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '), uc.CCHAR(' '))
    def draw (self, win): uc.wborder(win, self.left, self.right, self.top, self.bottom, self.top_left_corner, self.top_right_corner, self.bottom_left_corner, self.bottom_right_corner)

    def update(self, win):
        self.clear(win)
        self.draw (win)


class Events:
    @property
    def on_click (self): return self.__on_click
    @property
    def on_hover  (self): return self.__on_hover

    @on_click.setter
    def on_click (self, value): self.__on_click = value
    @on_hover.setter
    def on_hover  (self, value): self.__on_hover  = value

    def __init__(self):
        self.__on_click = lambda *args : None
        self.__on_hover  = lambda *args : None



class Component(Events):
    __mouse_was_read = False
    __colors_initialized = False

    def __init__(self, win=None, y=0, x=0, height=0, width=0, anchor=(False, False, False, False), iheight=None, iwidth=None, warp=True, border:Border=None, visibility=True) -> None:
        super().__init__()
        self.parent            = Parent(win or uc.stdscr)
        self.position          = Position (y, x)
        self.size              = Size(height, width, iheight or height, iwidth or width)
        self.anchor            = Anchor   (*anchor)
        self.warp              = warp
        self.border            = border # TODO: to check
        self.components        = []
        self.__visibility      = visibility
        self._x_fraction = 0
        self._y_fraction = 0
        # if border: self.border.draw(self.pad) #TODO: see Border 
        if not Component.__colors_initialized:
            initialize_colors()
            Component.__colors_initialized = True


    def refresh(self, redraw_parent=False):
        Component.__mouse_was_read = False


    def hide(self): self.visibility = False
    def show(self): self.visibility = True


    @property #TODO: ADD descrition like use `self.position.x` instead if you don't want to redraw the `parent.win` immediately after
    def visibility(self): return self.__visibility

    @visibility.setter
    def visibility(self, visibility): self.__visibility = visibility; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property #TODO: ADD descrition like use `self.position.x` instead if you don't want to redraw the `parent.win` immediately after
    def x(self): return self.position.x

    @x.setter
    def x(self, X): self.position.x = X; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def y(self): return self.position.y

    @y.setter
    def y(self, Y): self.position.y = Y; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def ix(self): return self.position.ix

    @ix.setter
    def ix(self, iX): self.position.ix = iX; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def iy(self): return self.position.iy

    @iy.setter
    def iy(self, iY): self.position.iy = iY; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def width(self): return self.size.width

    @width.setter
    def width(self, width): self.size.width = width; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def height(self): return self.size.height

    @height.setter
    def height(self, height): self.size.height = height; self.refresh(redraw_parent=isinstance(self,WindowPad))

    @property
    def minwidth(self): return self.size.minwidth

    @minwidth.setter
    def minwidth(self, minwidth): self.size.minwidth = minwidth

    @property
    def minheight(self): return self.size.minheight

    @minheight.setter
    def minheight(self, minheight): self.size.minheight = minheight

    @property
    def maxwidth(self): return self.size.maxwidth

    @maxwidth.setter
    def maxwidth(self, maxwidth): self.size.maxwidth = maxwidth

    @property
    def maxheight(self): return self.size.maxheight

    @maxheight.setter
    def maxheight(self, maxheight): self.size.maxheight = maxheight

    @property
    def iwidth(self): return self.size.iwidth

    @property
    def iheight(self): return self.size.iheight


    def get_mouse(self):
        if not Component.__mouse_was_read:
            Component.id, Component._x, Component._y, Component._z, Component.bstate = uc.getmouse()
            Component.__mouse_was_read = True
        Component.in_range = self._in_range()
        return (Component.in_range, Component.id, Component._x, Component._y, Component._z, Component.bstate )


    def handle_events(self, event, redraw_parent=True):
        if event == uc.KEY_MOUSE:
            in_range, id, x, y, z, bstate = self.get_mouse() # aah... here because calling getmouse more than once, returns 0,0...
            if not in_range: return False # If not in_range, there's no consumption of the event
            if ( bstate & uc.BUTTON1_RELEASED or bstate & uc.BUTTON3_RELEASED or bstate & uc.BUTTON2_RELEASED) or \
                (bstate & uc.BUTTON1_CLICKED  or bstate & uc.BUTTON3_CLICKED  or bstate & uc.BUTTON2_CLICKED): # because Termux doesn't care about uc.mouseinterval(0), see also /TUIFIManager/issues/114
                self.on_click(self, id, x, y, z, bstate)
                return True
            self.on_hover(self, id, x, y, z, bstate)
            return True
        return False


    def centerX(self):
        _, new_columns = uc.getmaxyx(self.parent.win)
        self.position.x = (new_columns //2) - (self.width //2)
        uc.touchwin(self.parent.win) # Do i need this? YES

    def centerY(self):
        new_lines, _ = uc.getmaxyx(self.parent.win)
        self.position.y = (new_lines//2) - (self.height//2)
        uc.touchwin(self.parent.win) # Do i need this? YES

    def center(self):
        new_lines, new_columns = uc.getmaxyx(self.parent.win)
        self.position.x = (new_columns //2) - (self.width //2)
        self.position.y = (new_lines//2) - (self.height//2)
        uc.touchwin(self.parent.win) # Do i need this? YES

    def handle_resize(self, redraw_parent=True, redraw_border=True):
        if self.border and redraw_border:
            self.border.clear(self.pad)  # TODO: implementation when I'll have borders for drawables too

        new_lines, new_columns = uc.getmaxyx(self.parent.win)
        deltaY = new_lines - self.parent.lines
        deltaX = new_columns - self.parent.columns

        # Handle vertical anchor resizing
        if self.anchor.bottom and self.anchor.top:
            tmp_height = self.size.height + deltaY
            if self.size.maxheight != 0 and tmp_height > self.size.maxheight:
                deltaY = tmp_height - self.size.maxheight
                self.position.y += deltaY // 2
                self._y_fraction += deltaY % 2
                self.size.height = self.size.maxheight
                if self._y_fraction >= 2:
                    self.position.y += self._y_fraction // 2
                    self._y_fraction %= 2
            elif tmp_height < self.size.minheight:
                deltaY = tmp_height - self.size.minheight
                self.position.y += deltaY // 2
                self._y_fraction += deltaY % 2
                self.size.height = self.size.minheight
                if self._y_fraction >= 2:
                    self.position.y += self._y_fraction // 2
                    self._y_fraction %= 2
            else:
                self.size.height = tmp_height

            if self.warp or self.size.height > self.size.iheight:
                self.size.iheight = self.size.height
                self._resize()

        elif self.anchor.bottom:
            self.position.y += deltaY

        # Handle horizontal anchor resizing
        if self.anchor.right and self.anchor.left:
            tmp_width = self.size.width + deltaX

            if self.size.maxwidth != 0 and tmp_width > self.size.maxwidth:
                deltaX = tmp_width - self.size.maxwidth
                self.position.x += deltaX // 2
                self._x_fraction += deltaX % 2
                self.size.width = self.size.maxwidth
                if self._x_fraction >= 2:
                    self.position.x += self._x_fraction // 2
                    self._x_fraction %= 2
            elif tmp_width < self.size.minwidth:
                deltaX = tmp_width - self.size.minwidth 
                self.position.x += deltaX // 2
                self._x_fraction += deltaX % 2
                self.size.width = self.size.minwidth
                if self._x_fraction >= 2:
                    self.position.x += self._x_fraction // 2
                    self._x_fraction %= 2
            else:
                self.size.width = tmp_width

            if self.warp or self.size.width > self.size.iwidth:
                self.size.iwidth = self.size.width
                self._resize()

        elif self.anchor.right:
            self.position.x += deltaX

        self.parent.lines = new_lines
        self.parent.columns = new_columns

        if redraw_parent:
            uc.touchwin(self.parent.win)
        if self.border and redraw_border:
            self.border.draw(self.pad)


class WindowPad(Component):
    def __init__(self, win=None, y=0, x=0, height=0, width=0, anchor=(False, False, False, False), is_focused=False, iheight=None, iwidth=None, warp=True, border:Border=None) -> None:
        super().__init__(win, y, x, height, width, anchor, iheight, iwidth, warp, border)
        self.pad               = uc.newpad(height, width)
        self.is_focused        = is_focused
        self.components        = []
        initialize_colors()


    def add_component(self, obj):
        self.components.append(obj)


    def refresh(self, redraw_parent=False, clear=True):
        lock.acquire_lock()
        if not self.visibility: 
            if redraw_parent: # when visibility changes it calls refresh with redraw_parent=True
                uc.touchwin(self.parent.win) # Do i need this? YES
            uc.wrefresh(self.parent.win) # Do i need this? YES | IMPORTANT: wrefresh works only with windows, not pads also look at https://stackoverflow.com/a/35351060/11465149
            return
        if self.border: self.border.update(self.pad)
        if clear: uc.werase(self.pad)
        for drawable in self.components:
            if drawable.visibility: drawable.draw()
        if redraw_parent:
            uc.touchwin(self.parent.win) # Do i need this? YES
            # uc.wtouchline(self.parent.win, self.y,1) 
            # uc.wtouchline(self.parent.win, self.y,self.height)
        uc.wrefresh(self.parent.win) # Do i need this? YES | IMPORTANT: wrefresh works only with windows, not pads also look at https://stackoverflow.com/a/35351060/11465149
        uc.prefresh(self.pad, self.position.iy, self.position.ix, self.position.y, self.position.x, self.position.y + self.size.height -1, self.position.x + self.size.width -1)
        super().refresh()
        lock.release()


    def _in_range(self):
        return (
            self.x <= Component._x < self.x + self.width
            and self.y <= Component._y < self.y + self.height
        )

    def handle_events(self, event, redraw_parent=True): #  prevent multiple if conditions for drawable components too
        if event == uc.KEY_RESIZE: return self.handle_resize(redraw_parent) # meaning no event consumption, we let KEY_RESIZE pass through
        elif self.visibility:
            event_consumed = super().handle_events(event,redraw_parent) 
            for drawable in self.components: 
                if drawable.visibility: event_consumed |= drawable.handle_events(event, redraw_parent)
            return event_consumed
        return False # meaning no event consumption, we found no event matching


    def _resize(self):
        uc.wresize(self.pad, self.iheight, self.iwidth)


    def handle_resize(self, redraw_parent=True, redraw_border=True): # TODO: max min sizes
        super().handle_resize(redraw_parent=redraw_parent, redraw_border=redraw_border)
        for drawable in self.components:
            drawable.handle_resize()
        return False # meaning no event consumption, we let KEY_RESIZE pass through




class Drawable(Component):
    def __init__(self,winpad:WindowPad, y=0, x=0, height=1, width=45, anchor=(False, False, False, False) ) -> None:
        self.winpad = winpad
        super().__init__(winpad.pad, y, x, height, width, anchor)
        self.__add_component_to(winpad) 


    def _in_range(self):
        return (
            self.winpad.x+self.x <= Component._x < self.winpad.x + self.x + self.width 
            and self.winpad.y+self.y <= Component._y < self.winpad.y + self.y + self.height
        )


    def centerX(self):
        self.position.y = (self.winpad.height//2) - (self.height//2)

    def centerY(self):
        self.position.y = (self.winpad.height//2) - (self.height//2)

    def center(self):
        self.position.x = (self.winpad.width //2) - (self.width //2)
        self.position.y = (self.winpad.height//2) - (self.height//2)


    def refresh(self, redraw_parent=False):
        self.winpad.refresh(redraw_parent)


    def __add_component_to(self, winpad):
        winpad.add_component(self)



class Label(Drawable): # TODO: make components a type of Drawables\components rather than a WindowPad
    def __init__(self,winpad:WindowPad, y=0, x=0, text='', height=1, width=None, anchor=(False, False, False, False), wrap_text=False, color=4, style=uc.A_NORMAL ) -> None:
        super().__init__(winpad, y, x, height, width if width else len(text), anchor)
        self.style      = style
        self.color_pair = color
        self._text      = text
        self.wrap_text  = wrap_text
        self.maxheight  = 1 # WARN         : this is temporary maybe?
        self.minwidth   = len(text) # WARN : this is temporary maybe?

    @property
    def text(self): return self._text


    def draw(self):
        x = self.x
        w = self.width
        text = self.text
        if self.wrap_text and len(text) > self.width:
            w = self.minwidth = self.size.width = len(text)
        elif not self.wrap_text and len(text) > self.width:
            text = text[:self.width-3] + '...'

        if self.x < 0: 
            x = 0
            w = self.width +self.x
            text = text[-self.x:]
        if self.winpad.x < 0: 
            x = 0
            w = self.width +self.winpad.x 
            text = text[-self.winpad.x:] 
        uc.mvwaddstr(self.parent.win,self.y,x, ' '*w, color_pair_with_effect(self.color_pair , self.style ))
        uc.mvwaddstr(self.parent.win,self.y,x, text , color_pair_with_effect(self.color_pair , self.style ))


    @text.setter
    def text(self, text):
        self._text = text
        self.refresh()


    def _resize(self):
        self.draw() # means clear so it's fine to just draw



class Button(Label): # Let's pretend for a momment that this is a button too :P
    def __init__(self, winpad: WindowPad, y=0, x=0, text='', height=1, width=None, anchor=(False, False, False, False)) -> None:
        super().__init__(winpad, y, x, text, height, width , anchor)



class PictureBoxMono(Drawable): # Monochrome
    def __init__(self,winpad:WindowPad, y=0, x=0, text='', height=1, width=None, anchor=(False, False, False, False), wrap_text=False, color=4 ) -> None:
        super().__init__(winpad, y, x, height, width if width else len(text), anchor)
        self.style      = uc.A_NORMAL
        self._text      = text
        self.color_pair = color


    @property
    def text(self): return self._text


    @text.setter
    def text(self, text):
        self._text = text
        self.refresh()


    def draw(self):
        if not self.text: return
        for i, ln in enumerate(self.text.split('\n')):
            uc.mvwaddstr(self.parent.win,self.y+i,self.x, ' '*len(ln), color_pair_with_effect(self.color_pair , self.style ))
            uc.mvwaddstr(self.parent.win,self.y+i,self.x, ln         , color_pair_with_effect(self.color_pair , self.style ))





# THIS IS ONLY FOR TESTING PURPOSES
def main():
    def label_clicked(label, id, x, y, z, bstate):
        label.text = f'C x:{x} y:{y}'

    def label_hoverd(label, id, x, y, z, bstate):
        label.text = f'HOVERED x:{x} y:{y} win: {winform.width} {winform.iwidth}'
        
    event  = -1
    global stdscr
    stdscr = uc.initscr()  # Global UniCurses Variable

    uc.use_default_colors()
    uc.start_color( )
    uc.cbreak     ( )
    uc.noecho     ( )
    uc.curs_set   (0)

    # Initializing color pairs of (FOREGROUND, BACKGROUND) colors.
    uc.init_pair(10, -1   ,-1 )

    # Initializing Mouse and then Update/refresh() stdscr
    uc.mouseinterval(0)
    uc.mousemask    (uc.ALL_MOUSE_EVENTS | uc.REPORT_MOUSE_POSITION) # print("\033[?1003h\n")
    uc.keypad       (stdscr, True )
    uc.nodelay      (stdscr, False)
    print           (BEGIN_MOUSE) # Initializing mouse movement | Don't move it above because it won't work on Windows
    uc.keypad       (uc.stdscr, True)

    winform = WindowPad(stdscr,2,4,10,60, anchor=(True, True, True, True)) #TODO: default minmax to size when anchor ....?
    winform.minwidth = 50
    winform.maxwidth = 70
    winform.minheight = 10
    winform.maxheight = 20

    uc.wbkgd(winform.pad, uc.COLOR_PAIR(1))
    
    winform2 = WindowPad(stdscr,12,4,10,60, anchor=(True, False, True, False))
    # # winform2.minwidth = 30
    # winform2.minwidth = 40
    # winform2.maxwidth = 60
    uc.wbkgd(winform2.pad, uc.COLOR_PAIR(1))

    tl = Label(winform ,1,2 ,anchor=(True, False, True, False),text='top-left')
    tr = Label(winform ,1,winform.width-11 ,anchor=(True, False, False, True),text='top-right')
    bl = Label(winform ,winform.height-2,2 ,anchor=(False, True, True, False),text='btm-left')
    br = Label(winform ,winform.height-2,winform.width-11 ,anchor=(False, True, False, True),text='btm-right')
    tb = Label(winform ,0,0 ,anchor=(False, True, False, True),text='0123456789',width=10)
    ta = Label(winform ,0,11,anchor=(False, True, False, True),text='0123456789',width=10)
    td = Label(winform ,3,5 ,anchor=(True , True, True, True),text='teeeest')
    tc = Label(winform ,2,1 ,anchor=(False, True,  True, True),text='teeeestloong', width=58,)
    t2 = Label(winform2,0,0 ,anchor=(False, True,  True, True),text='winform2_label', wrap_text=True)
    td.maxwidth = 7
    ta.style = uc.A_REVERSE; ta.color_pair = 5
    tc.style = uc.A_REVERSE; tb.color_pair = 8
    tb.style = uc.A_REVERSE; 
    t2.style = uc.A_REVERSE; t2.color_pair = 5
    tb.on_click = label_clicked
    tc.on_click = label_clicked
    t2.on_click = label_clicked
    t2.on_hover = label_hoverd
    winform2.refresh()
    winform.refresh()

    # Initializing TUIFIManager

    while event != 27:
        event = uc.get_wch()
        if event == uc.CCHAR('a'):
            for _ in range(0,5):
                ta.x +=1
                sleep(.1)
        elif event == uc.CCHAR('b'):
            for _ in range(0,5): # problematic, (maybe) needs a winpad handler for animations
                winform2.x +=1
                sleep(.1)
        elif event == uc.CCHAR('d'): # problematic, (maybe) needs a winpad handler for animations
            for _ in range(0,5):
                winform.y +=1;
                sleep(.1)
        elif event == uc.CCHAR('c'): td.center()
        elif event == uc.CCHAR('C'): winform.center()
        elif event == uc.CCHAR('h'): tc.hide()
        elif event == uc.CCHAR('s'): tc.show()
        elif event == uc.CCHAR('H'): winform2.hide()
        elif event == uc.CCHAR('S'): winform2.show()
        elif event == uc.CCHAR('e'): uc.bkgd(uc.CCHAR("/"))
        elif event == uc.CCHAR('f'): uc.bkgd(uc.CCHAR("%"))
        elif event == uc.CCHAR('g'): uc.bkgd(uc.CCHAR(" "))

        winform2.handle_events(event)
        winform.handle_events(event)
        winform2.refresh()
        winform.refresh()
        uc.refresh      ()
        if event == uc.KEY_RESIZE:
            uc.resize_term(0,0)

    print(END_MOUSE)
    uc.endwin()


if __name__ == "__main__":
    main()
