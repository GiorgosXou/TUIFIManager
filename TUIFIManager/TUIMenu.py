#from unicurses import  *
import unicurses

# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS

# I had 0 time so the code is a bit messed up
from .TUItilities import Border, WindowPad

class TUIMenu(WindowPad): # TODO: fix alt+down in __init__.py i think when no file is selected (not here)

    # x    , y      = 0 , 0
    # width, height = 20, 15
    items  = []
    events = {
    }

    def __init__(self, items=[], border=Border(), on_choice=lambda *args : None ):
        super().__init__(border=border)
        # self.parent = unicurses.stdscr
        self.exists = False
        if items:self.items = items
        self.width  = len(max(self.items, key=len)) + 4
        self.height = len(self.items) + 2
        self.on_choice = on_choice


    def create(self, atY=None, atX=None):
        if atX is not None: self.x = atX
        if atY is not None: self.y = atY

        parent_width  = unicurses.getmaxx(self.parent.win)
        parent_height = unicurses.getmaxy(self.parent.win)
        if self.x + self.width  > parent_width : self.x -= self.width
        if self.y + self.height > parent_height: self.y -= self.height
        if self.y < 0 : self.y = 0

        if self.exists:
            unicurses.delwin(self.pad)

        self.pad = unicurses.newpad(self.height, self.width) #unicurses.newwin(len(self.items)*2+1, self.width, self.y+offy , self.x+offx )
        unicurses.wbkgd(self.pad,unicurses.COLOR_PAIR(1))
        i = 1
        # unicurses.mvwaddwstr(self.pad,0,0,'╭' + ('─'*(self.width-2)) + '╮')
        for item in self.items:
            unicurses.mvwaddwstr(self.pad, i, 2, f'{item}', unicurses.A_BOLD)
            i+=1

        self.exists = True
        self.refresh()


    def delete(self):
        if self.exists:
            unicurses.delwin(self.pad)
            self.__it   = 0
            self.exists = False
            # unicurses.redrawwin(self.parent) # SuS? kinda same as touchwin? | Update: 2024-04-06 11:50:09 AM Not sure why i had this there... 
            # unicurses.wrefresh(self.parent)


    def refresh(self, redraw_parent=False):
        if self.exists:
            super().refresh(redraw_parent=redraw_parent)
            # unicurses.wrefresh(self.parent.win)
            # # unicurses.touchwin(self.pad)
            # # unicurses.wrefresh(self.pad)
            # unicurses.prefresh(self.pad, 0, 0, self.y, self.x, self.y + self.height -1, self.x + self.width -1)


    __it = 0
    def handle_keyboard_events(self, event):
        if not self.exists or event == unicurses.KEY_MOUSE: return False
        if event == unicurses.KEY_DOWN:
            if self.__it == len(self.items):
                self.delete()
                return True
            unicurses.mvwchgat(self.pad, self.__it   , 1, self.width -2, unicurses.A_BOLD, 1)
            unicurses.mvwchgat(self.pad, self.__it +1, 1, self.width -2, unicurses.A_BOLD, 6)
            self.__it +=1
        elif event == unicurses.KEY_UP:
            if self.__it <= 1:
                self.delete()
                return True
            self.__it -=1
            unicurses.mvwchgat(self.pad, self.__it +1, 1, self.width -2, unicurses.A_BOLD, 1)
            unicurses.mvwchgat(self.pad, self.__it , 1, self.width -2, unicurses.A_BOLD, 6)
        elif event in (unicurses.KEY_ENTER,10):
            i = self.__it -1 
            self.delete()
            self.on_choice(i)
        else:
            self.delete()
        return True


    __x = __y = 0
    def handle_mouse_events(self, id, x, y, z, bstate):
        if not self.exists: return False
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            relative_y = y - self.y -1
            if self.__y != y and self.height -2 > relative_y >= 0:
                unicurses.mvwchgat(self.pad, y-self.y , 1, self.width -2, unicurses.A_BOLD | unicurses.A_ITALIC, 6)
                unicurses.mvwchgat(self.pad, self.__y-self.y,1, self.width -2, unicurses.A_BOLD, 1)
                # unicurses.mvwchgat(self.pad, self.__x , 1, self.width -2, unicurses.A_BOLD, 1)
            if bstate & unicurses.BUTTON1_RELEASED:
                if self.__x != x or self.__y != y : return True
                if  self.height -2 > relative_y >= 0:
                    self.delete()
                    self.on_choice(relative_y)
            # if bstate & unicurses.BUTTON1_PRESSED:
        else:
            self.delete() #unicurses.ungetmouse(id, x, y, z, bstate )
        self.__x, self.__y = x,y
        return True


