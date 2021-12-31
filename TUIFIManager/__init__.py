from      unicurses import *
from           glob import glob
from           time import time
from             os import  sep
from       .TUIFile import *
from  .TUIFIProfile import * 
import   subprocess
import       shutil
import       signal
import          sys
import           os



PADDING_LEFT   = 2
PADDING_RIGHT  = 2
PADDING_TOP    = 1
PADDING_BOTTOM = 0

HOME_DIR  = os.getenv('UserProfile') if OPERATING_SYSTEM == 'Windows' else os.getenv('HOME')
IS_TERMUX = True if 'com.termux' in HOME_DIR else False

UP   = -1
DOWN =  1



class TUIFIManager:  # TODO: I need to create a TUIWindowManager class where i will manage all the anchor, resizing and positional stuff for future components (something like Visual-Studio's c#/vb's Winform's behaviour)
    """ 
    
    parent     (       win      ): Parent windows in which the Filemanager-pad is hosted. 
    pad        ( Window pointer ): The window/Pad where the manager is hosted.
    anchor_... (bool  , optional): Anchor refers to the position the Manager window has relative to the edges of the parent one. 
    y          (int   , optional): y-axis position of pad. Defaults to 0.
    x          (int   , optional): x-axis position of pad. Defaults to 0.
    directory  (str   , optional): Initital directory. Defaults to HOME_DIR which is $HOME or $UserProfile
    suffixes   (list  , optional): "Path expansion rules (file patterns to be found). Defaults to ['*'].
    sort_by    ([type], optional): [Not implemented yet]. Defaults to None.
    draw_files (bool  , optional): "draws" files the moment of initialization (must prefresh to show). Defaults to True.
    termux_touch_only (bool, optional)  : if true: full touch, no mouse support else: full mouse half touch support. Defaults to True.
    """  
    
    class struct_TUIFIparent:
        def __init__(self,win):
            self.win = win
            self.lines, self.columns = getmaxyx(self.win)
    
    files            = []   
    pad              = None  # for now only pads
    directory        = sep 
    __count_selected = 0
    
    def __init__(self, parent, pad, y=0, x=0, anchor_top=False, anchor_left=False, anchor_bottom=False, anchor_right=False, directory=HOME_DIR, suffixes=['*'], sort_by=None, draw_files=True, termux_touch_only=True):
        self.suffixes          = suffixes
        self.draw_files        = draw_files
        self.pad               = pad
        self.visibleW          = getmaxx(pad)
        self.visibleH          = getmaxy(pad)
        self.Y                 = y
        self.maxY              = None
        self.minY              = None
        self.X                 = x
        self.maxX              = None
        self.minX              = None
        self.visibleY          = 0  # Y at the visible range of pad
        self.prepl             = 0 ## i thk this need delete
        self.termux_touch_only = termux_touch_only
        self.parent            = self.struct_TUIFIparent(parent) 
        
        #if parent:
        #    self.parent        = self.struct_TUIFIparent(parent) 
        #else:
        #    self.parent        = self.struct_TUIFIparent(stdscr) 
        #self.pad_panel                     = new_panel(pad)
        self.set_anchor(anchor_top, anchor_left, anchor_bottom, anchor_right)
        
        if directory:
            self.directory = os.path.normpath(directory)
            self.load_files(directory, suffixes, sort_by)
            if draw_files:
                self.draw()
                
        if OPERATING_SYSTEM == 'Windows':
            pass #signal.signal(signal.CTRL_C_EVENT,override_exit_event) #windows Only
        else:
            signal.signal(signal.SIGINT,self.copy)
    
    
    def set_anchor(self, top=False, left=False, bottom=False, right=False):
        self.anchor = {
            'top'   : top,
            'left'  : left,
            'bottom': bottom,
            'right' : right
        }
    
    
    def draw(self):
        werase(self.pad)
        #self.refresh()
        if self.maxpLines < self.visibleH:
            self.maxpLines = self.visibleH 
        wresize(self.pad, self.maxpLines, self.visibleW)
        for f in self.files:
            f.draw(self.pad)
    
    
    #def get_TUIFIProfile_by_key(self, key): # https://stackoverflow.com/a/2974082/11465149       
        #return next((v for k, v in TUIFIProfiles.items() if (key == k) or (isinstance(k,tuple) and key in k)),FILE_profile)
    
    
    def load_files(self, directory, suffixes=None, sort_by=None):  # DON'T load and then don't show :P
        directory = os.path.realpath(os.path.normpath(directory))
        if not os.path.isdir(directory):
            raise Exception('DirectoryNotFound: "' + directory + '"') 
        if not suffixes == None: 
            self.suffixes = suffixes
        
        self.directory = directory
        self.files = []
        glob_files = []
        glob_files.append(directory + sep + '..')
        for suffix in self.suffixes:
            glob_files.extend(glob(directory + sep + suffix))
            
        max_h, pCOLS, count, y, x = 0, self.visibleW, 0, PADDING_TOP, PADDING_LEFT 
        for f in glob_files:
            is_link  = os.path.islink(f)
            filename = f.split(sep)[-1]
              
            if os.path.isdir(f):
                temp_profile = TUIFIProfiles.get("empty_folder")
                for suffix in self.suffixes:
                    if not len(glob(f + sep + suffix)) == 0:
                        temp_profile = TUIFIProfiles.get('folder')
                        break
            else:
                file_extension = os.path.splitext(filename)[1]
                temp_profile = TUIFIProfiles.get(file_extension.lower(),DEFAULT_PROFILE) # ..[-1] = extension                                                    
                
            file_ = TUIFile(filename,y,x,temp_profile,is_link=is_link)
            self.files.append(file_)
            tempX = (PADDING_LEFT + file_.profile.width + PADDING_RIGHT)
            
            if x > pCOLS-tempX + PADDING_RIGHT - self.X:
                x  = PADDING_LEFT
                y += max_h + PADDING_TOP + PADDING_BOTTOM
                count = 0
                max_h = 0
                
            file_.y = y
            file_.x = x
            x      += tempX
            count  += 1
            
            h = file_.profile.height + file_.name_height
            if h > max_h: 
                max_h = h
                     
        if not count == 0:
            self.maxpLines = y + max_h + PADDING_TOP + PADDING_BOTTOM + self.Y     
        else:
            self.maxpLines = y + self.Y
        return self.files
    
    
    def resort(self): #draw_files=True # repeating code but nvm 
        """In case of resize, call this function to resort/replace existing files to the new dimensions of pad 

        Returns:
            list: self.files
        """
        werase(self.pad)
            
        max_h, pCOLS, count, y, x = 0, self.visibleW, 0, PADDING_TOP, PADDING_LEFT 
        for f in self.files:
            tempX = (PADDING_LEFT + f.profile.width + PADDING_RIGHT)
            if x > pCOLS-tempX + PADDING_RIGHT - self.X:
                x  = PADDING_LEFT
                y += max_h + PADDING_TOP + PADDING_BOTTOM  # ... +1 because the next has to be below :P
                count = 0
                max_h = 0
                
            f.y = y
            f.x = x
            x  += tempX
            count += 1
            
            h = f.profile.height + f.name_height #len(f.chunkStr(f.name, f.profile.width).split('\n')) #total hight i might merge them  but nvm for now, i messed the up anyways
            if h > max_h:
                max_h = h
                if not count == 0:
                    self.maxpLines = y + max_h + PADDING_TOP + PADDING_BOTTOM  + self.Y
                else:
                    self.maxpLines = y + self.Y 
                if self.maxpLines < self.visibleH:
                    self.maxpLines = self.visibleH 
                wresize(self.pad, self.maxpLines, self.visibleW) 
                
            f.draw(self.pad,redraw_icon=True)
            
        #wresize(self.pad, self.maxpLines, self.visibleW) # because it works doesn't also mean that i should do it like that  

        #if self.visibleY >= getmaxy(self.pad) - self.visibleH + self.Y:
            #self.visibleY = getmaxy(self.pad) - self.visibleH
        #if self.visibleH + self.visibleY > y:
        #    self.visibleY -= self.visibleH + self.visibleY - y  # NOT SURE AT ALL BUT IT WORKS LOL, actually NOP ):(            
        #self.draw() 
        #self.select(self.__clicked_file) #  ??????????????
        return self.files
        
    
    def reload(self,draw_files=True):
        self.visibleY                = 0
        self.__clicked_file          = None
        self.__index_of_clicked_file = None
        self.load_files(self.directory)
        if draw_files:
            self.draw()
    
    
    def open(self, directory, suffixes=None, sort_by=None):
        """
        `open()` is `load_files()` + `draw()`
        """
        if directory in (None,''):
            return None
        if isinstance(directory,TUIFile):
            directory = self.directory + sep + directory.name
        if not os.path.isdir(directory): 
            open_with = TUIFIProfiles.get(os.path.splitext(directory)[1],DEFAULT_PROFILE).open_with
            if open_with:
                proc = subprocess.Popen([open_with, directory])
                proc.wait()
                subprocess.call(['tuifi', self.directory])  # sys.executable, __file__
            #subprocess.call(['micro', directory])   
            return None
        self.__clicked_file          = None
        self.__index_of_clicked_file = None
        self.__count_selected        = 0
        self.visibleY                = 0
        self.load_files(directory, suffixes, sort_by)
        self.draw()
        return self.files
    
    
    def refresh(self, pminrow_vY=None, pmincol=None, sminrow=None, smincol=None, smaxrow=None, smaxcol=None):
        self.visibleH = smaxrow    if not smaxrow    == None else self.visibleH
        self.visibleW = smaxcol    if not smaxcol    == None else self.visibleW
        self.visibleY = pminrow_vY if not pminrow_vY == None else self.visibleY
        self.Y        = sminrow    if not sminrow    == None else self.Y
        self.X        = smincol    if not smincol    == None else self.X
        wrefresh(self.parent.win)
        prefresh(self.pad,self.visibleY, pmincol, self.Y, self.X, self.visibleH -1, self.visibleW -1)
    
    
    def get_tuifile_by_name(self, name):
        return next((f for f in self.files if f.name == name), None)
    
    
    def get_tuifile_by_coordinates(self, y, x, relative_to_pad=False, return_enumerator=False):
        if not relative_to_pad:
            y += self.visibleY - self.Y
            x -= self.X
        for i, f in enumerate(self.files):
            if x >= f.x and x < (f.x + f.profile.width) and y >= f.y and y < (f.y + f.profile.height + f.name_height ):  # y <= because name_height
                if not return_enumerator:
                    return f
                else:
                    return i, f  # lol "if" with a comma
        
        if not return_enumerator:
            return None
        else:
            return None, None
    
    
    def deselect(self,tuifile=None):
        if not tuifile and self.__count_selected == 1:
            tuifile = self.__clicked_file
        if not tuifile:
            for f in self.files:
                if f.is_selected:
                    f.is_selected = False
                    f.draw(self.pad)     
            self.__count_selected = 0 # i can just -= 1 and break it if 0 :P
        else:
            tuifile.is_selected = False
            tuifile.draw(self.pad)
            self.__count_selected -=1
                  
        
    def select(self, tuifile):
        self.__count_selected +=1
        if not tuifile: 
            return
        #for y in range(tuifile.y, tuifile.y + tuifile.profile.height):
        #    mvwchgat(self.pad,y, tuifile.x, tuifile.profile.width,A_REVERSE,7)
        tuifile.is_selected = True
        tuifile.draw(self.pad)
                
    
    def scroll_pad(self, y):
        if self.visibleY == 0 and y < 0:
            return
        if self.visibleY >= getmaxy(self.pad) - self.visibleH  and y > 0:
            return
        self.visibleY += y
    
    
    is_on_termux_select_mode   = False
    __mouse_btn1_pressed_file  = None
    __pre_clicked_file         = None
    __clicked_file             = None
    __index_of_clicked_file    = None
    __start_time               = 0
    __temp__copied_files       = [] 
    __temp_dir_of_copied_files = ''
        
    events = { # Disable or replace Events if you want (with 0x11111111? and None for CTRL(x)? i think) 
        'BUTTON1_DOUBLE_CLICKED': BUTTON1_DOUBLE_CLICKED       ,  # Temp because https://github.com/wmcbrine/PDCurses/issues/130 
        'KEY_MOUSE'             : KEY_MOUSE                    ,
        'BUTTON4_PRESSED'       : BUTTON4_PRESSED              ,
        'BUTTON5_PRESSED'       : BUTTON5_PRESSED              ,
        'BUTTON1_PRESSED'       : BUTTON1_PRESSED              ,
        'BUTTON1_RELEASED'      : BUTTON1_RELEASED             ,
        'BUTTON1_CLICKED'       : BUTTON1_CLICKED              ,
        'BUTTON_CTRL'           : BUTTON_CTRL                  ,
        'KEY_UP'                : KEY_UP                       ,
        'KEY_DOWN'              : KEY_DOWN                     ,
        'KEY_LEFT'              : KEY_LEFT                     ,
        'KEY_RIGHT'             : KEY_RIGHT                    ,
        'KEY_BACKSPACE'         : (KEY_BACKSPACE, 8, 127, 263) ,
        'KEY_ENTER'             : (KEY_ENTER,10)               ,
        'KEY_BTAB'              : KEY_BTAB                     ,
        'KEY_DC'                : KEY_DC                       ,
        'CTRL_S'                : CTRL('S')                    ,
        'CTRL_R'                : CTRL('R')                    ,
        'CTRL_X'                : CTRL('X')                    ,  
        'CTRL_C'                : CTRL('C')                    ,  
        'CTRL_V'                : CTRL('V')                      
    }  
    def __delete_file(self,file):
        if isinstance(file, TUIFile):
            file = self.directory + sep + file.name
        elif not isinstance(file, str):
            raise Exception('TUIFileTypeError: file must be of type string or TUIFile.')
        if not os.path.isdir(file):
            os.remove(file)
        else:
            shutil.rmtree(file)    
        self.__count_selected -= 1
            
    
    def scroll_to_file(self, tuifile, select=False, deselect=False):
        if select:
            self.select(tuifile)
        if tuifile.y - PADDING_TOP < self.visibleY :
            self.visibleY = tuifile.y - PADDING_TOP
            return
        temp_sum_of_Y__y_and_height_of_tuifile = self.Y + tuifile.y + tuifile.profile.height + tuifile.name_height + PADDING_TOP
        temp_sum_of_visible_H_and_Y =  self.visibleH + self.visibleY                       
        if temp_sum_of_Y__y_and_height_of_tuifile > temp_sum_of_visible_H_and_Y  :
            self.visibleY += temp_sum_of_Y__y_and_height_of_tuifile - (temp_sum_of_visible_H_and_Y )
  
  
    __is_cut = False
    def cut(self):
        """
        Cut-copies the selected files
        """
        self.__is_cut = True
        self.__copy()
        
         
    def copy(self, signum=None, frame=None):
        """
        Copies the selected files (ignore signum=None, frame=None [...])
        """ 
        self.__is_cut = False
        self.__copy()    


    def __copy(self):
        """
        this function is TEMPOTATY and will be REMOVED, 
        it will be pressent until i find a way of drawing/managing cutted files efficiently
        """
        if self.__clicked_file and not self.__clicked_file.name == '..':
            self.__temp_dir_of_copied_files = self.directory
            if self.__count_selected == 1:                                        
                self.__temp__copied_files = [self.__clicked_file]                 
            else:
                self.__temp__copied_files = []
                for f in self.files:                      
                    if f.is_selected:
                        self.__temp__copied_files.append(f) 
                        
    
    def handle_events(self, event): # wtf, ok .. works acceptably :P, TODO: REMOVE rrrrepeating code but nvm for now >:( xD
        if event == self.events.get('KEY_MOUSE'): 
            id, x, y, z, bstate = getmouse() 
            if bstate & self.events.get('BUTTON4_PRESSED'):
                self.scroll_pad(UP) 
            elif bstate & self.events.get('BUTTON5_PRESSED'):
                self.scroll_pad(DOWN)  
            elif (not IS_TERMUX) or (IS_TERMUX and not self.termux_touch_only): # because there are some times that long like presses might be translated to BUTTON1_PRESSED instead of CLICK
                pass
                if (bstate & self.events.get('BUTTON1_RELEASED')) or (OPERATING_SYSTEM == 'Windows' and bstate & self.events.get('BUTTON1_DOUBLE_CLICKED')): # OPERATING_SYSTEM == 'Windows' because issues with ncurses 
                    self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
                    self.__delay1 = time() - self.__delay1
                    sumed_time = time() - self.__start_time - self.__delay1 # yeah whatever
                        
                    if self.__mouse_btn1_pressed_file == self.__clicked_file and not bstate & self.events.get('BUTTON_CTRL'):
                        self.deselect()
                        if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..':
                            self.select(self.__mouse_btn1_pressed_file )
                        if (sumed_time < 0.4 or bstate & self.events.get('BUTTON1_DOUBLE_CLICKED')) and self.__clicked_file: #and count == 2  :
                            if self.open(self.__clicked_file):
                                self.__index_of_clicked_file = None
                                self.__pre_clicked_file      = None
                    elif self.__clicked_file and self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file == self.__clicked_file: #and not self.__clicked_file.is_selected:
                        if os.path.isdir(self.directory + sep + self.__clicked_file.name): 
                            for f in self.files:
                                if f.is_selected:
                                    shutil.move(self.directory + sep + f.name, self.directory + sep + self.__clicked_file.name + sep + f.name)
                            self.__pre_clicked_file = None
                            self.reload()

                    self.__start_time = time()       
                elif bstate & self.events.get('BUTTON1_PRESSED'):
                    self.__delay1 = time()
                    self.__mouse_btn1_pressed_file = self.get_tuifile_by_coordinates(y, x)
                    
                    if not bstate & self.events.get('BUTTON_CTRL') and self.__pre_clicked_file and self.__pre_clicked_file.is_selected and  self.__count_selected == 1:#and summ > 0.4:
                        self.deselect(self.__pre_clicked_file)
                    if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..' :
                        if not self.__mouse_btn1_pressed_file.is_selected : 
                            self.select(self.__mouse_btn1_pressed_file)                   
                        elif bstate & self.events.get('BUTTON_CTRL') :#and summ > 0.4:
                            self.deselect(self.__mouse_btn1_pressed_file)
                            
                    self.__pre_clicked_file = self.__mouse_btn1_pressed_file 
            else:
                if bstate & self.events.get('BUTTON1_CLICKED') or bstate & self.events.get('BUTTON1_PRESSED'): # TERMUX                
                    clicked_file = self.get_tuifile_by_coordinates(y, x)
                    
                    if not self.is_on_termux_select_mode: # bstate & BUTTON_CTRL :
                        self.deselect()
                            
                    if self.is_on_termux_select_mode and clicked_file and not clicked_file.name == '..' : # bstate & BUTTON_CTRL 
                        if not clicked_file.is_selected : 
                            self.select(clicked_file)
                        else:                   
                            self.deselect(clicked_file)
                    elif clicked_file:
                        self.open(clicked_file)
           
        elif event == KEY_RESIZE: # maybe i will add a calculate_size() function for this code part that will call a function from the TUIWindowManager 
            new_lines, new_columns = getmaxyx(self.parent.win)
            if self.anchor.get('bottom'):
                if self.anchor.get('top'):
                    self.visibleH += (new_lines - self.parent.lines)
                else:
                    deltaY = (new_lines - self.parent.lines)
                    self.Y += deltaY
                    self.visibleH += deltaY 
            if self.anchor.get('right'):
                if self.anchor.get('left'):
                    self.visibleW += (new_columns - self.parent.columns)
                else:
                    deltaX = (new_columns - self.parent.columns)
                    self.X += deltaX
                    self.visibleW += deltaX
               
            #if fileManager.visibleY > getmaxy(fileManager.pad) - fileManager.visibleH + fileManager.Y:
                #fileManager.visibleY = getmaxy(fileManager.pad) - fileManager.visibleH + fileManager.Y
            self.parent.lines   = new_lines
            self.parent.columns = new_columns
            self.resort()
            touchwin(self.parent.win)
            
        elif event in self.events.get('KEY_BACKSPACE'):
            self.open(self.directory + sep + '..')
        elif event == self.events.get('CTRL_S') and IS_TERMUX:
            if self.is_on_termux_select_mode:  # hmm..
                self.is_on_termux_select_mode = False
            else:
                self.is_on_termux_select_mode = True
        elif event in self.events.get('KEY_ENTER'):
            if self.__count_selected == 1 and self.__clicked_file.is_selected:
                if self.open(self.__clicked_file):
                    self.__index_of_clicked_file = None
                    self.__pre_clicked_file      = None
                    
        elif event == self.events.get('KEY_UP'):  # Not the most reliable way but nvm for now | A lot of REPEATING CODE but  nvm ffor now
            if not self.__index_of_clicked_file == None:
                for i in range(self.__index_of_clicked_file,0,-1):
                    if (self.files[i-1].y < self.files[self.__index_of_clicked_file].y) and (self.files[i-1].x <= self.files[self.__index_of_clicked_file].x):
                        self.deselect()
                        self.__index_of_clicked_file = i -1
                        self.__clicked_file = self.files[i-1]
                        self.scroll_to_file(self.__clicked_file, True)
                        break
            else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                self.select(self.files[0])
                self.__clicked_file = self.files[0]
                self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_DOWN'):
            if not self.__index_of_clicked_file == None:
                for i in range(self.__index_of_clicked_file,len(self.files)-1):
                    if (self.files[i+1].y > self.files[self.__index_of_clicked_file].y) and (self.files[i+1].x >= self.files[self.__index_of_clicked_file].x):
                        self.deselect()
                        self.__index_of_clicked_file = i +1
                        self.__clicked_file = self.files[i+1]
                        self.scroll_to_file(self.__clicked_file, True)
                        break
            else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                self.select(self.files[0])
                self.__clicked_file = self.files[0]
                self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_RIGHT'): # __arrow_key_navigation
            if not self.__index_of_clicked_file == len(self.files) - 1:
                if not self.__index_of_clicked_file == None:
                    self.deselect()
                    self.__index_of_clicked_file = self.__index_of_clicked_file +1
                    self.__clicked_file = self.files[self.__index_of_clicked_file]
                    self.scroll_to_file(self.__clicked_file, True)
                else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                    self.select(self.files[0])
                    self.__clicked_file = self.files[0]
                    self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_LEFT'):
            if not self.__index_of_clicked_file == 0:
                if not self.__index_of_clicked_file == None:
                    self.deselect()
                    self.__index_of_clicked_file = self.__index_of_clicked_file -1
                    self.__clicked_file = self.files[self.__index_of_clicked_file]
                    self.scroll_to_file(self.__clicked_file, True)
                else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                    self.select(self.files[0])
                    self.__clicked_file = self.files[0]
                    self.__index_of_clicked_file = 0
                    
        elif event == self.events.get('KEY_BTAB'):
            if self.__clicked_file and not self.__clicked_file.name == '..':
                shutil.move(self.directory + sep + self.__clicked_file.name, self.directory + sep + '..' + sep + self.__clicked_file.name)
                temp_i = self.__index_of_clicked_file - 1
                self.reload()
                self.__index_of_clicked_file = temp_i
                self.__clicked_file = self.files[temp_i]
                self.select(self.__clicked_file)
                
        elif event == self.events.get('KEY_DC'): # TODO: FIX ISSUE WHEN NAVIGATING trough link and deleting | Update i think i fixed it lol
            if self.__clicked_file and not self.__clicked_file.name == '..':
                if self.__count_selected == 1:
                    self.__delete_file(self.__clicked_file)
                    temp_i = self.__index_of_clicked_file - 1
                    self.reload()
                    self.__index_of_clicked_file = temp_i
                    self.__clicked_file = self.files[temp_i]
                    self.__pre_clicked_file = None # hmm.. sus?
                    self.select(self.__clicked_file)
                else: # if self.__count_selected > 1:  # Why do i even > 1 very sus
                    temp_i = self.__index_of_clicked_file - self.__count_selected 
                    for f in self.files:
                        if f.is_selected:
                            self.__delete_file(f)
                            if self.__count_selected == 0:
                                self.reload()
                                self.__index_of_clicked_file = temp_i
                                self.__clicked_file = self.files[temp_i]
                                self.__pre_clicked_file = None # hmm.. sus
                                self.select(self.__clicked_file)
                                break
                    
        elif event == self.events.get('CTRL_R'):
            self.reload()  
            
        elif event == self.events.get('CTRL_C'):  # or KEY_IC ? | copy selected files
            self.copy()
             
        elif event == self.events.get('CTRL_X'): 
            self.cut() 
            
        elif event == self.events.get('CTRL_V'): # check if path the  same as self.directory maybe? 
            if not len(self.__temp__copied_files) == 0 and os.path.exists(self.__temp_dir_of_copied_files):  # u never no if the user deleted anything from other file manager this is also something i haven't consider for the rest of the things and [...]
                if not self.__temp_dir_of_copied_files == self.directory:
                    for f in self.__temp__copied_files:
                        f_path_name = self.__temp_dir_of_copied_files + sep + f.name
                        if os.path.isfile(f_path_name):   # Does 'file' exist?
                            shutil.copyfile(f_path_name,self.directory + sep + f.name, follow_symlinks=False)
                            if self.__is_cut:
                                os.remove(f_path_name) 
                        elif not f_path_name == self.directory and os.path.isdir(f_path_name):  # Does 'directory' exist?                
                            shutil.copytree(f_path_name,self.directory + sep + f.name, symlinks=True)
                            if self.__is_cut:
                                shutil.rmtree(f_path_name)                             
                else:
                    pass # just duplicate the files 
                self.reload()
                
        elif event == CTRL('f'):
            pass # find 
        else:
            waddstr(self.pad, lib1.keyname(event))
    
