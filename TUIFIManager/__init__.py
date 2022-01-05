#TODO: I NEED TO ADD GETTERS AND SETTERS FOR Y AND X BECAUSE THEY NEED unicurses.touchwin(self.parent.win)

from           glob import glob
from           time import time
from             os import  sep
from       .TUIMenu import    * 
from       .TUIFile import    *
from  .TUIFIProfile import    * 
import   subprocess
import    unicurses  
import       shutil
import       signal
import          sys
import           os



PADDING_LEFT   = 2
PADDING_RIGHT  = 2
PADDING_TOP    = 1
PADDING_BOTTOM = 0

HOME_DIR  = os.getenv('UserProfile') if unicurses.OPERATING_SYSTEM == 'Windows' else os.getenv('HOME')
IS_TERMUX = True if 'com.termux' in HOME_DIR else False

UP   = -1
DOWN =  1



def stty_a(key=None):  # whatever [...] 
    if shutil.which('stty'):
        if key:
            for sig in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';'):
                if sig.endswith(key):
                    return sig.split('=')[0].strip()
                    break
        else:
            return [s.strip() for s in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';')[4:-3]] # risky? i've no idea.. thats why i've not done the same when "if key:"
    return None



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
    draw_files (bool  , optional): "draws" files the moment of initialization (must unicurses.prefresh to show). Defaults to True.
    termux_touch_only (bool, optional)  : if true: full touch, no mouse support else: full mouse half touch support. Defaults to True.
    """  
    
    class struct_TUIFIparent:
        def __init__(self,win):
            self.win = win
            self.lines, self.columns = unicurses.getmaxyx(self.win)
    
    files              = []
    pad                = None  # for now only pads
    directory          = sep
    __count_selected   = 0
    double_click_DELAY = 0.4 
    
    def __init__(self, pad, y=0, x=0, anchor_top=False, anchor_left=False, anchor_bottom=False, anchor_right=False, directory=HOME_DIR, suffixes=['*'], sort_by=None, parent=None, draw_files=True, termux_touch_only=True):
        self.suffixes          = suffixes
        self.draw_files        = draw_files
        self.pad               = pad
        self.visibleW          = unicurses.getmaxx(pad)
        self.visibleH          = unicurses.getmaxy(pad)
        self.Y                 = y
        self.maxY              = None
        self.minY              = None
        self.X                 = x
        self.maxX              = None
        self.minX              = None
        self.visibleY          = 0  # Y at the visible range of pad
        self.prepl             = 0 ## i thk this need delete
        self.termux_touch_only = termux_touch_only
        self.menu              = TUIMenu()
        if parent:
            self.parent        = self.struct_TUIFIparent(parent)  
        else:
            self.parent        = self.struct_TUIFIparent(unicurses.stdscr)  
        
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
                
        if stty_a('^C') or unicurses.OPERATING_SYSTEM == 'Windows': # https://docs.microsoft.com/en-us/windows/console/ctrl-c-and-ctrl-break-signals
            signal.signal(signal.SIGINT,self.copy)
    
    
    def set_anchor(self, top=False, left=False, bottom=False, right=False):
        self.anchor = {
            'top'   : top,
            'left'  : left,
            'bottom': bottom,
            'right' : right
        }
    
    
    def draw(self):
        unicurses.werase(self.pad)
        #self.refresh()
        if self.maxpLines < self.visibleH:
            self.maxpLines = self.visibleH 
        unicurses.wresize(self.pad, self.maxpLines, self.visibleW)
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
        unicurses.werase(self.pad)
            
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
                unicurses.wresize(self.pad, self.maxpLines, self.visibleW) 
                
            f.draw(self.pad,redraw_icon=True)
            
        #unicurses.wresize(self.pad, self.maxpLines, self.visibleW) # because it works doesn't also mean that i should do it like that  

        #if self.visibleY >= unicurses.getmaxy(self.pad) - self.visibleH + self.Y:
            #self.visibleY = unicurses.getmaxy(self.pad) - self.visibleH
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
        self.__pre_clicked_file      = None
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
        unicurses.wrefresh(self.parent.win) # Do i need this? YES
        unicurses.prefresh(self.pad,self.visibleY, pmincol, self.Y, self.X, self.visibleH -1, self.visibleW -1)
        self.menu.refresh()
    
    
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
        if self.visibleY >= unicurses.getmaxy(self.pad) - self.visibleH  and y > 0:
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
        'BUTTON1_DOUBLE_CLICKED': unicurses.BUTTON1_DOUBLE_CLICKED       ,  # Temp because https://github.com/wmcbrine/PDCurses/issues/130 
        'KEY_MOUSE'             : unicurses.KEY_MOUSE                    ,
        'BUTTON4_PRESSED'       : unicurses.BUTTON4_PRESSED              ,
        'BUTTON5_PRESSED'       : unicurses.BUTTON5_PRESSED              ,
        'BUTTON1_PRESSED'       : unicurses.BUTTON1_PRESSED              ,
        'BUTTON1_RELEASED'      : unicurses.BUTTON1_RELEASED             ,
        'BUTTON1_CLICKED'       : unicurses.BUTTON1_CLICKED              ,
        'BUTTON3_PRESSED'       : unicurses.BUTTON3_PRESSED              ,
        'BUTTON3_RELEASED'      : unicurses.BUTTON3_RELEASED             ,
        'BUTTON_CTRL'           : unicurses.BUTTON_CTRL                  ,
        'KEY_UP'                : unicurses.KEY_UP                       ,
        'KEY_DOWN'              : unicurses.KEY_DOWN                     ,
        'KEY_LEFT'              : unicurses.KEY_LEFT                     ,
        'KEY_RIGHT'             : unicurses.KEY_RIGHT                    ,
        'KEY_BACKSPACE'         : (unicurses.KEY_BACKSPACE, 8, 127, 263) ,
        'KEY_ENTER'             : (unicurses.KEY_ENTER,10)               ,
        'KEY_BTAB'              : unicurses.KEY_BTAB                     ,
        'KEY_DC'                : unicurses.KEY_DC                       ,
        'KEY_HOME'              : unicurses.KEY_HOME                     ,
        'KEY_END'               : unicurses.KEY_END                      ,
        'CTRL_DOWN'             : 'kDN5'                                 ,
        'CTRL_UP'               : 'kUP5'                                 ,
        'CTRL_LEFT'             : 'kLFT5'                                ,
        'ALT_DOWN'              : 'kDN3'                                 ,
        'KEY_F5'                : unicurses.KEY_F(5)                     ,
        'CTRL_R'                : unicurses.CTRL('R')                    ,
        'CTRL_X'                : unicurses.CTRL('X')                    ,  
        'CTRL_C'                : unicurses.CTRL('C')                    ,  
        'CTRL_V'                : unicurses.CTRL('V')                      
    }  
    def __delete_file(self,file):
        if isinstance(file, TUIFile):
            file = self.directory + sep + file.name
        elif not isinstance(file, str):
            raise Exception('TUIFileTypeError: file must be of type string or TUIFile.')
        if os.path.isfile(file): # checking if exists too.
            os.remove(file)
        elif os.path.exists(file) and not file.endswith(sep + '..'): # "and not .." whatever
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
        Cut-copies the selected files | Not fully implemented yet
        """
        self.__is_cut = True  # TODO: DON'T FORGET TO CHANGE TERMUX CUT WHEN NEW VERSION[...]
        self.__copy()
        
         
    def copy(self, signum=None, frame=None):
        """
        Copies the selected files (ignore signum=None, frame=None [...]) | Not fully implemented yet
        """ 
        self.__is_cut = False
        self.__copy()    


    def __copy(self):
        """
        this function is TEMPOTATY and will be REMOVED, 
        it will be pressent until i find a way of drawing/managing cutted files efficiently
        """   
        self.__temp_dir_of_copied_files = self.directory
        if self.__count_selected == 1 and self.__clicked_file and not self.__clicked_file.name == '..':                                        
            self.__temp__copied_files = [self.__clicked_file]                 
        else:
            self.__temp__copied_files = []
            for f in self.files:                      
                if f.is_selected:
                    self.__temp__copied_files.append(f) 
                        
                        
    def paste(self):
        """
        Pastes the already selected and copied/cutted files.
        """
        if not len(self.__temp__copied_files) == 0 and os.path.exists(self.__temp_dir_of_copied_files):  # u never no if the user deleted anything from other file manager this is also something i haven't consider for the rest of the things and [...]
            if not self.__temp_dir_of_copied_files == self.directory:
                for f in self.__temp__copied_files:
                    f_path_name = self.__temp_dir_of_copied_files + sep + f.name
                    if os.path.isfile(f_path_name):   # Does 'file' exist?
                        shutil.copyfile(f_path_name,self.directory + sep + f.name, follow_symlinks=False)
                        if self.__is_cut:
                            os.remove(f_path_name) 
                    elif os.path.isdir(f_path_name):  # Does 'directory' exist?                
                        shutil.copytree(f_path_name,self.directory + sep + f.name, symlinks=True)
                        if self.__is_cut:
                            shutil.rmtree(f_path_name)                             
            else:
                pass # just duplicate the files 
            self.reload()
                        
    
    def delete(self):
        """
        Deletes the selected file(s). | Not fully implemented yet
        """
        if self.__count_selected == 1 and self.__clicked_file : 
            if not self.__clicked_file.name == '..': # checking under __delete_file too but nvm cause i have no time right now
                self.__delete_file(self.__clicked_file)
                temp_i = self.__index_of_clicked_file - 1
                self.reload()
                self.__index_of_clicked_file = temp_i
                self.__clicked_file = self.files[temp_i]
                self.__pre_clicked_file = None # hmm.. sus?
                self.select(self.__clicked_file)
        else: # if self.__count_selected > 1:  # Why do i even > 1 very sus
            if self.__clicked_file:
                temp_i = self.__index_of_clicked_file - self.__count_selected 
            else:
                temp_i = 0 # VERY SUS BUT NVM NOW
                
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
                    
    
    is_on_reaname_mode                         = False
    __on_second_loop_change_is_on_reaname_mode = False
    __temp_pre_name                            = ''
    __temp_name                                = ''
    __temp_i                                   = 0
    illegal_filename_characters                = ('<', '>', ':',  '/', '\\', '|', '?', '*')
    def handle_rename_events(self, event):  # At this momment i don't even care about optimizing anything... just kidding, you get the point, no free time
        if event == unicurses.KEY_LEFT:
            if not self.__temp_i == 0: self.__temp_i -= 1
        elif event == unicurses.KEY_RIGHT:
            if not self.__temp_i == len(self.__temp_name): self.__temp_i += 1
        elif event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
            if not self.__temp_i == 0:
                self.__temp_i -= 1
                self.__temp_name = self.__temp_name[0:self.__temp_i] + self.__temp_name[self.__temp_i+1:]
        elif unicurses.RCCHAR(event) in self.illegal_filename_characters:
            return
        elif event == 27 or event in (unicurses.KEY_ENTER,10):
            self.__temp_i = 0
            self.__on_second_loop_change_is_on_reaname_mode = True
            if not event == 27:
                os.rename(self.directory + sep + self.__clicked_file.name  , self.directory + sep + self.__temp_name)        
                self.__clicked_file.name = self.__temp_name
                self.resort()
                self.scroll_to_file(self.__clicked_file, True)
            else:
                self.__temp_name = self.__clicked_file.name
        else:
            self.__temp_name = self.__temp_name[0:self.__temp_i] + unicurses.RCCHAR(event) + self.__temp_name[self.__temp_i:]
            self.__temp_i += 1  
        self.__clicked_file.draw_name(self.pad,self.__temp_name,self.__temp_pre_name, self.__temp_i)
        self.__temp_pre_name = self.__temp_name
        #if event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
        #    pass
    
                        
    def __perform_menu_selected_action(self, action):  # TODO: USE DICT INSTEAD OF IF, ELIF
        if   action == 'Open'  : self.open  (self.__clicked_file)
        elif action == 'Cut'   : self.cut   ()
        elif action == 'Delete': self.delete()
        elif action == 'Copy'  : self.copy  ()
        elif action == 'Paste' : self.paste ()
        elif action == 'Rename': self.is_on_reaname_mode = True
        elif action == 'Reload': self.reload()
            
                            
    def handle_events(self, event): # wtf, ok .. works acceptably :P, TODO: REMOVE rrrrepeating code but nvm for now >:( xD
        if self.is_on_reaname_mode == True: # REDIRECT ALL KEYBOARD EVENTS 
            if not self.__on_second_loop_change_is_on_reaname_mode: 
                self.handle_rename_events(event)
                return
            else:
                self.__on_second_loop_change_is_on_reaname_mode = False
                self.is_on_reaname_mode = False
        
        action = self.menu.handle_keyboard_events(event)  # if performed the event   
        if action: # action-εστί που λεμε και στη βυζαντινη
            self.__perform_menu_selected_action(action)         
            return
        
        if event == self.events.get('KEY_MOUSE'): 
            id, x, y, z, bstate = unicurses.getmouse() 
            action = self.menu.handle_mouse_events(id, x, y, z, bstate)
            if action:
                self.__perform_menu_selected_action(action)
                return
            
            if bstate & self.events.get('BUTTON4_PRESSED'):
                self.scroll_pad(UP) 
            elif bstate & self.events.get('BUTTON5_PRESSED'):
                self.scroll_pad(DOWN)  
            elif (not IS_TERMUX) or (IS_TERMUX and not self.termux_touch_only): # because there are some times that long like presses might be translated to BUTTON1_PRESSED instead of CLICK
                if (bstate & self.events.get('BUTTON1_RELEASED')) or (bstate & self.events.get('BUTTON3_RELEASED')) or (unicurses.OPERATING_SYSTEM == 'Windows' and bstate & self.events.get('BUTTON1_DOUBLE_CLICKED')): # unicurses.OPERATING_SYSTEM == 'Windows' because issues with ncurses 
                    self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
                    self.__delay1 = time() - self.__delay1
                    sumed_time = time() - self.__start_time - self.__delay1 # yeah whatever
  
                    
                    if (self.__mouse_btn1_pressed_file == self.__clicked_file and not bstate & self.events.get('BUTTON_CTRL')) :
                        if not ((bstate & self.events.get('BUTTON3_RELEASED')) and self.__count_selected > 1 and  self.__clicked_file.is_selected): 
                            self.menu.delete()
                            self.deselect()
                        if (bstate & self.events.get('BUTTON3_RELEASED')):
                            self.menu.create(y,x)
                        if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..' and not self.__mouse_btn1_pressed_file.is_selected :
                            self.select(self.__mouse_btn1_pressed_file )
                        if (((sumed_time < self.double_click_DELAY) and (bstate & self.events.get('BUTTON1_RELEASED'))) or bstate & self.events.get('BUTTON1_DOUBLE_CLICKED')) and self.__clicked_file: #and count == 2  :
                            self.open(self.__clicked_file)
                    elif self.__clicked_file and self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file == self.__clicked_file: #and not self.__clicked_file.is_selected:
                        if os.path.isdir(self.directory + sep + self.__clicked_file.name): 
                            for f in self.files:
                                if f.is_selected:
                                    shutil.move(self.directory + sep + f.name, self.directory + sep + self.__clicked_file.name + sep + f.name)
                            self.__pre_clicked_file = None
                            self.reload()

                    self.__start_time = time()       
                elif (bstate & self.events.get('BUTTON1_PRESSED')) or (bstate & self.events.get('BUTTON3_PRESSED')):
                    self.__delay1 = time()
                    self.__mouse_btn1_pressed_file = self.get_tuifile_by_coordinates(y, x)
                    
                    if not bstate & self.events.get('BUTTON_CTRL') and self.__pre_clicked_file and self.__pre_clicked_file.is_selected and  self.__count_selected == 1:#and summ > self.double_click_DELAY:
                        self.deselect(self.__pre_clicked_file)
                        self.menu.delete()
                    if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..' :
                        if not self.__mouse_btn1_pressed_file.is_selected and not (bstate & self.events.get('BUTTON3_PRESSED')): 
                            self.select(self.__mouse_btn1_pressed_file)                   
                        elif bstate & self.events.get('BUTTON_CTRL') :#and summ > self.double_click_DELAY:
                            self.deselect(self.__mouse_btn1_pressed_file)
                            
                    self.__pre_clicked_file = self.__mouse_btn1_pressed_file 
            else:  # TERMUX 
                if bstate & self.events.get('BUTTON1_CLICKED') or bstate & self.events.get('BUTTON1_PRESSED'): # TERMUX                
                    self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True) 
                    
                    if not self.is_on_termux_select_mode: # bstate & BUTTON_CTRL :
                        self.deselect()
                            
                    if self.is_on_termux_select_mode and self.__clicked_file and not self.__clicked_file.name == '..' : # bstate & BUTTON_CTRL 
                        if not self.__clicked_file.is_selected : 
                            self.select(self.__clicked_file)
                        else:                   
                            self.deselect(self.__clicked_file)
                    elif self.__clicked_file:
                        if self.is_on_termux_select_mode: # AUTO COPY IF IN SELECT-MODE AND CLICKED ON  '..'
                            self.is_on_termux_select_mode = False
                            self.copy()
                        self.open(self.__clicked_file)
           
        elif event == unicurses.KEY_RESIZE: # maybe i will add a calculate_size() function for this code part that will call a function from the TUIWindowManager 
            new_lines, new_columns = unicurses.getmaxyx(self.parent.win)
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
               
            #if fileManager.visibleY > unicurses.getmaxy(fileManager.pad) - fileManager.visibleH + fileManager.Y:
                #fileManager.visibleY = unicurses.getmaxy(fileManager.pad) - fileManager.visibleH + fileManager.Y
            self.parent.lines   = new_lines
            self.parent.columns = new_columns
            self.resort()
            unicurses.touchwin(self.parent.win)
        
        elif event in self.events.get('KEY_BACKSPACE'):
            self.open(self.directory + sep + '..')
            
        elif event in self.events.get('KEY_ENTER'):
            if self.__count_selected == 1 and self.__clicked_file.is_selected:
                self.open(self.__clicked_file)
            
        elif event == self.events.get('KEY_HOME'):
            self.open(HOME_DIR) 
                   
        elif event == self.events.get('KEY_UP'):  # Not the most reliable way but nvm for now | A lot of REPEATING CODE but  nvm ffor now
            if not self.__index_of_clicked_file == None:
                for i in range(self.__index_of_clicked_file,0,-1):
                    if (self.files[i-1].y < self.files[self.__index_of_clicked_file].y) and (self.files[i-1].x <= self.files[self.__index_of_clicked_file].x):
                        self.deselect()
                        self.__index_of_clicked_file = i -1
                        self.__clicked_file = self.files[i-1]
                        self.__mouse_btn1_pressed_file = self.__clicked_file
                        self.__pre_clicked_file = self.__clicked_file
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
                        self.__mouse_btn1_pressed_file = self.__clicked_file
                        self.__pre_clicked_file = self.__clicked_file
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
                    self.__mouse_btn1_pressed_file = self.__clicked_file
                    self.__pre_clicked_file = self.__clicked_file
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
                    self.__mouse_btn1_pressed_file = self.__clicked_file
                    self.__pre_clicked_file = self.__clicked_file
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
                
        elif event == self.events.get('CTRL_R'): 
            self.is_on_reaname_mode = True
            self.__temp_name        = self.__clicked_file.name
            self.__temp_pre_name    = self.__temp_name
        elif event == self.events.get('KEY_DC'): self.delete()  # TODO: FIX ISSUE WHEN NAVIGATING trough link and deleting | Update i think i fixed it lol
        elif event == self.events.get('KEY_F5'): self.reload()  
        elif event == self.events.get('CTRL_C'): self.copy  ()  # or KEY_IC ? | copy selected files
        elif event == self.events.get('CTRL_X'): self.cut   ()  
        elif event == self.events.get('CTRL_V'): self.paste ()  # check if path the  same as self.directory maybe? 
        elif event == unicurses.CTRL('f'):
            pass # find
        
        elif unicurses.keyname(event) == self.events.get('ALT_DOWN'): 
            if self.menu.exists:
                self.menu.delete()
            else:
                self.menu.create(self.__clicked_file.y,self.__clicked_file.x +1)

        elif IS_TERMUX: # TERMUX ONLY, EASILY ACCESIBLE KEYBINDINGS  
            if unicurses.keyname(event) == self.events.get('CTRL_DOWN'): # 
                if self.is_on_termux_select_mode:  # hmm..
                    self.is_on_termux_select_mode = False
                    self.copy()
                else:
                    self.is_on_termux_select_mode = True 
            elif unicurses.keyname(event) == self.events.get('CTRL_LEFT'):
                if self.is_on_termux_select_mode:
                    self.is_on_termux_select_mode = False
                    self.cut()
                else:
                    self.__is_cut = True
            elif unicurses.keyname(event) == self.events.get('CTRL_UP'):
                self.paste()
            elif event == self.events.get('KEY_END'):
                if self.is_on_termux_select_mode:
                    self.is_on_termux_select_mode = False
                self.delete()
        #else:
        #    unicurses.waddstr(self.pad, unicurses.keyname(event))
        
        #TODO: return event\action or none if any performed 
