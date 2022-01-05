#from unicurses import  *
import unicurses
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS 
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS
# WORK IN PROGRESS  | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS | WORK IN PROGRESS

# I had 0 time so the code is a bit messed up

class TUIMenu:    
    
    x    , y      = 0 , 0
    width, height = 20, 15
    items  = ['Open       │ ENTER' ,
              'Cut        │ CTRL+X',
              'Delete     │ DEL'   ,
              'Copy       │ CTRL+C',
              'Paste      │ CTRL+V',
              'Rename     │ CTRL+R',  
              'Reload     │ KEY_F5',
              'Properties '
    ]
    events = {
        'KEY_UP'          : unicurses.KEY_UP          ,
        'KEY_DOWN'        : unicurses.KEY_DOWN        ,
        'KEY_MOUSE'       : unicurses.KEY_MOUSE       ,
        'KEY_ENTER'       : (unicurses.KEY_ENTER,10)  ,
        'BUTTON1_RELEASED': unicurses.BUTTON1_RELEASED,
        'BUTTON1_PRESSED' : unicurses.BUTTON1_PRESSED ,
        'BUTTON3_RELEASED': unicurses.BUTTON3_RELEASED         
    }
    
    def __init__(self, items=None):
        self.parent = unicurses.stdscr
        self.exists = False
        if items:self.items = items   
        self.width  = len(max(self.items, key=len)) + 4 
        self.height = len(self.items)*2 + 1 
            

    def create(self, atY=None, atX=None):
        if atX is not None: self.x = atX 
        if atY is not None: self.y = atY   
        
        offx, offy = 1,1
        parent_width  = unicurses.getmaxx(self.parent)
        parent_height = unicurses.getmaxy(self.parent)
        if self.x + self.width > parent_width:
            self.x -= self.width
            offx = 0
        if self.y + self.height > parent_height:
            self.y -= self.height 
            offy = 1
             
        if self.exists:
            unicurses.delwin(self.win)
        self.win = unicurses.newwin(len(self.items)*2+1, self.width, self.y+offy , self.x+offx )
        unicurses.wbkgd(self.win,unicurses.COLOR_PAIR(1))
        i = 1
        unicurses.mvwaddwstr(self.win,0,0,'╭' + ('‒'*(self.width-2)) + '╮')
        for item in self.items:
            unicurses.mvwaddwstr(self.win,i,0,'│ ' + item, unicurses.A_BOLD)
            unicurses.mvwaddwstr(self.win,i,self.width-1,'│',unicurses.A_BOLD)
            unicurses.mvwaddwstr(self.win,i+1,0,'├' + ('‒'*(self.width-2)) + '┤')
            i+=2
        unicurses.mvwaddwstr(self.win,i-1,0,'╰' + ('‒'*(self.width-2)) + '╯')
        
        self.refresh()
        self.exists = True
        
    
    def delete(self):
        if self.exists:
            unicurses.delwin(self.win)
            self.__it   = -1
            self.exists = False
    
    
    def refresh(self):
        if self.exists:
            unicurses.wrefresh(self.parent)
            unicurses.touchwin(self.win)
            unicurses.wrefresh(self.win)
    
    
    def __getItem(self,i):
        return self.items[i].split('│')[0].strip()

    
    __it = -1
    def handle_keyboard_events(self, event): 
        performed = False
        if self.exists and not event == self.events.get('KEY_MOUSE'):
            if event == self.events.get('KEY_DOWN'):
                performed=True
                if self.__it == len(self.items) -1:
                    self.delete()
                    return True
                self.__it +=1
                unicurses.mvwchgat(self.win, self.__it *2 -1, 1, self.width -2, unicurses.A_BOLD, 1)
                unicurses.mvwchgat(self.win, self.__it *2 +1, 1, self.width -2, unicurses.A_BOLD, 7)
            elif event == self.events.get('KEY_UP'):
                performed=True
                if self.__it <= 0:
                    self.delete()
                    return True
                self.__it -=1
                unicurses.mvwchgat(self.win, self.__it *2 +3, 1, self.width -2, unicurses.A_BOLD, 1)
                unicurses.mvwchgat(self.win, self.__it *2 +1, 1, self.width -2, unicurses.A_BOLD, 7)
            elif event in self.events.get('KEY_ENTER'):
                i = self.__it
                self.delete()
                return self.__getItem(i)
            else:                   
                self.delete()
                performed=True

        return performed
    
      
    def handle_mouse_events(self, id, x, y, z, bstate):
        performed = False
        if self.exists: # mevent == self.events.get('KEY_MOUSE')  #id, x, y, z, bstate = unicurses.getmouse()
            if (x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height):
                relative_y = y - self.y
                if (bstate & self.events.get('BUTTON1_RELEASED')):
                    item_position = len(self.items)
                    if (relative_y % 2) == 0:
                        self.delete()
                        return self.__getItem(relative_y//2 -1)
                            
                    performed=True
                if (bstate & self.events.get('BUTTON1_PRESSED')):
                    performed=True
            else:
                self.delete() #unicurses.ungetmouse(id, x, y, z, bstate ) 
                        
        return performed
        
        