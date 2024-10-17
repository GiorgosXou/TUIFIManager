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

    def __init__(self, items, border=Border(), on_choice=lambda *args : None ):
        super().__init__(border=border, height=len(items) + 2, width=len(max(items, key=len)) + 4)
        # self.parent = unicurses.stdscr
        self.exists = False
        self.items = items
        self.on_choice = on_choice


    def create(self, atY=None, atX=None):
        if atX is not None: self.x = atX
        if atY is not None: self.y = atY

        parent_width  = unicurses.getmaxx(self.parent.win)
        parent_height = unicurses.getmaxy(self.parent.win)
        if self.x + self.width  > parent_width : self.position.x -= self.width - 1
        if self.y + self.height > parent_height: self.position.y -= self.height - 1
        if self.y < 0 : self.position.y = 0

        if self.exists:
            unicurses.delwin(self.pad)

        self.pad = unicurses.newpad(self.height, self.width) #unicurses.newwin(len(self.items)*2+1, self.width, self.y+offy , self.x+offx )
        unicurses.wbkgd(self.pad,unicurses.COLOR_PAIR(3))
        i = 1
        # unicurses.mvwaddwstr(self.pad,0,0,'╭' + ('─'*(self.width-2)) + '╮')
        for item in self.items:
            unicurses.mvwaddwstr(self.pad, i, 2, f'{item}', unicurses.A_BOLD)
            i+=1

        self.exists = True
        self.refresh()
        self.is_focused = False # to allow redrawing of windows behind on creation-(first time)


    def delete(self):
        if self.exists:
            unicurses.delwin(self.pad)
            self.__it   = 0
            self.exists = False
            self.is_focused = False
            # unicurses.redrawwin(self.parent) # SuS? kinda same as touchwin? | Update: 2024-04-06 11:50:09 AM Not sure why i had this there... 
            # unicurses.wrefresh(self.parent)


    def refresh(self, redraw_parent=False):
        if self.exists:
            super().refresh(redraw_parent=redraw_parent, clear=False)
            self.is_focused = True
            # unicurses.wrefresh(self.parent.win)
            # # unicurses.touchwin(self.pad)
            # # unicurses.wrefresh(self.pad)
            # unicurses.prefresh(self.pad, 0, 0, self.y, self.x, self.y + self.height -1, self.x + self.width -1)


    def handle_resize(self, redraw_parent=True, redraw_border=True):
        self.is_focused = False; 
        return False # super().handle_resize(redraw_parent, redraw_border)


    __it = 0
    def handle_events(self, event, redraw_parent=True):
        if not self.exists: return False
        if event == unicurses.KEY_MOUSE : return self.__handle_mouse_events()
        if event == unicurses.KEY_RESIZE: return self.handle_resize()
        return self.handle_keyboard_events(event)


    def handle_keyboard_events(self, event):
        if not self.exists or event == unicurses.KEY_MOUSE: return False
        if event == unicurses.KEY_DOWN:
            if self.__it == len(self.items):
                self.delete()
                return True
            unicurses.mvwchgat(self.pad, self.__it   , 1, self.width -2, unicurses.A_BOLD, 3)
            unicurses.mvwchgat(self.pad, self.__it +1, 1, self.width -2, unicurses.A_BOLD, 1)
            self.__it +=1
        elif event == unicurses.KEY_UP:
            if self.__it <= 1:
                self.delete()
                return True
            self.__it -=1
            unicurses.mvwchgat(self.pad, self.__it +1, 1, self.width -2, unicurses.A_BOLD, 3)
            unicurses.mvwchgat(self.pad, self.__it , 1, self.width -2, unicurses.A_BOLD, 1)
        elif event in (unicurses.KEY_ENTER,10):
            i = self.__it -1 
            self.delete()
            self.on_choice(i)
        else:
            self.delete()
        return True


    __x = __y = 0
    def __handle_mouse_events(self):
        in_range, id, x, y, z, bstate = self.get_mouse()
        if self.x <= x < self.x + self.width and self.y <= y < self.y + self.height:
            relative_y = y - self.y -1
            if self.__y != y and self.height -2 > relative_y >= 0:
                unicurses.mvwchgat(self.pad, y-self.y , 1, self.width -2, unicurses.A_BOLD | unicurses.A_ITALIC, 1)
                unicurses.mvwchgat(self.pad, self.__y-self.y,1, self.width -2, unicurses.A_BOLD, 3)
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


