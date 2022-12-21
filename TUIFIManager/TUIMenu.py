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
              'Copy       │ CTRL+C',
              'Paste      │ CTRL+V',
              'Delete     │ DEL'   ,
              'Rename     │ CTRL+R',  
              'Reload     │ KEY_F5',
              'New File   │ CTRL+W',
              'New Folder │ CTRL+N',
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
    
    def __init__(self, items=None, color_pair_offset=0):
        self.parent = unicurses.stdscr
        self.exists = False
        if items:self.items = items   
        self.width  = len(max(self.items, key=len)) + 4 
        self.height = len(self.items)*2 + 1 
        self.color_pair_offset = color_pair_offset
            

    def create(self, atY=None, atX=None):
        if atX is not None: self.x = atX 
        if atY is not None: self.y = atY   
        
        parent_width  = unicurses.getmaxx(self.parent)
        parent_height = unicurses.getmaxy(self.parent)
        if self.x + self.width  > parent_width : self.x -= self.width
        if self.y + self.height > parent_height: self.y -= self.height 
             
        if self.exists:
            unicurses.delwin(self.pad)

        self.pad = unicurses.newpad(self.height, self.width) #unicurses.newwin(len(self.items)*2+1, self.width, self.y+offy , self.x+offx )
        unicurses.wbkgd(self.pad,unicurses.COLOR_PAIR(1 + self.color_pair_offset))
        i = 1
        unicurses.mvwaddwstr(self.pad,0,0,'╭' + ('‒'*(self.width-2)) + '╮')
        for item in self.items:
            unicurses.mvwaddwstr(self.pad,i,0,'│ ' + item, unicurses.A_BOLD)
            unicurses.mvwaddwstr(self.pad,i,self.width-1,'│',unicurses.A_BOLD)
            unicurses.mvwaddwstr(self.pad,i+1,0,'├' + ('‒'*(self.width-2)) + '┤')
            i+=2
        unicurses.mvwaddwstr(self.pad,i-1,0,'╰' + ('‒'*(self.width-2)) + '╯')
        
        self.exists = True
        self.refresh()
        
    
    def delete(self):
        if self.exists:
            unicurses.delwin(self.pad)
            self.__it   = -1
            self.exists = False
            unicurses.redrawwin(self.parent) # SuS? kinda same as touchwin?
            # unicurses.wrefresh(self.parent)
    
    
    def refresh(self):
        if self.exists:
            # unicurses.wrefresh(self.parent)
            # unicurses.touchwin(self.pad)
            # unicurses.wrefresh(self.pad)
            unicurses.prefresh(self.pad, 0, 0, self.y, self.x, self.y + self.height -1, self.x + self.width -1)
    
    
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
                unicurses.mvwchgat(self.pad, self.__it *2 -1, 1, self.width -2, unicurses.A_BOLD, 1 + self.color_pair_offset)
                unicurses.mvwchgat(self.pad, self.__it *2 +1, 1, self.width -2, unicurses.A_BOLD, 7 + self.color_pair_offset)
            elif event == self.events.get('KEY_UP'):
                performed=True
                if self.__it <= 0:
                    self.delete()
                    return True
                self.__it -=1
                unicurses.mvwchgat(self.pad, self.__it *2 +3, 1, self.width -2, unicurses.A_BOLD, 1 + self.color_pair_offset)
                unicurses.mvwchgat(self.pad, self.__it *2 +1, 1, self.width -2, unicurses.A_BOLD, 7 + self.color_pair_offset)
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
                relative_y = y - self.y +1 # really Sus the +1 but nvm
                if (bstate & self.events.get('BUTTON1_RELEASED')):
                    item_position = len(self.items)
                    if (relative_y % 2) == 0:
                        # exit()
                        self.delete()
                        return self.__getItem(relative_y//2 -1)                   
                    performed=True
                if (bstate & self.events.get('BUTTON1_PRESSED')):
                    performed=True
            else:
                self.delete() #unicurses.ungetmouse(id, x, y, z, bstate ) 
        return performed
        
        
