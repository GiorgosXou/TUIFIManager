#TODO: I NEED TO ADD GETTERS AND SETTERS FOR Y AND X BECAUSE THEY NEED unicurses.touchwin(self.parent.win)
#TODO: I NEED TO CHECK FOR WRITE/READ/EXECUTE PERMISSIONS (PREVENT EXCEPTIONS\ERRORS) 

from     contextlib import contextmanager
from        pathlib import Path
from           time import time
from             os import  sep
from           math import log10
from       .TUIMenu import    * 
from       .TUIFile import    *
from  .TUIFIProfile import    * 
from   .TUItilities import    * 
import   subprocess
import    unicurses  
import       shutil
import       signal
import           os


PADDING_LEFT   = 2
PADDING_RIGHT  = 2
PADDING_TOP    = 1
PADDING_BOTTOM = 0

STTY_EXISTS = shutil.which('stty')
IS_WINDOWS  = True if 'Windows' == unicurses.OPERATING_SYSTEM else False
HOME_DIR    = os.getenv('UserProfile') if IS_WINDOWS else os.getenv('HOME')
IS_TERMUX   = True if 'com.termux' in HOME_DIR else False

UP   = -1
DOWN =  1



def stty_a(key=None):  # whatever [...] 
    if STTY_EXISTS:
        if key:
            for sig in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';'):
                if sig.endswith(key):
                    return sig.split('=')[0].strip()
                    break
        else:
            return [s.strip() for s in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';')[4:-3]] # risky? i've no idea.. thats why i've not done the same when "if key:"
    return None



class TUIFIManager(Component):  # TODO: I need to create a TUIWindowManager class where i will manage all the anchor, resizing and positional stuff for future components (something like Visual-Studio's c#/vb's Winform's behaviour)
    """ 
    parent     (       win      ): Parent windows in which the Filemanager-pad is hosted. 
    pad        ( Window pointer ): The window/Pad where the manager is hosted.
    anchor     ((bool), optional): Anchor refers to the position the Manager window has relative to the edges of the parent one. [top, bottom, left, right]
    y          (int   , optional): y-axis position of pad. Defaults to 0.
    x          (int   , optional): x-axis position of pad. Defaults to 0.
    directory  (str   , optional): Initital directory. Defaults to HOME_DIR which is $HOME or $UserProfile
    suffixes   (list  , optional): "Path expansion rules (file patterns to be found). Defaults to ['*'].
    sort_by    ([type], optional): [Not implemented yet]. Defaults to None.
    has_label  (bool  , optional): Creates a Label which displays informations about files
    draw_files (bool  , optional): "draws" files the moment of initialization (must unicurses.prefresh to show). Defaults to True.
    termux_touch_only   (bool, optional): if true: full touch, no mouse support else: full mouse half touch support. Defaults to True.
    auto_find_on_typing (bool, optional): if true: when starting to type, automatically search else only if CTRL_F
    vim_mode   (bool  , optional): If True: uses vim like keys to navigate. Defaults to False. 
    color_pair_offset   (int,  optional): Initializes\\Uses color-pairs from the offset an on | `unicurses.COLOR_PAIR(color_pair...+i)`
    is_focused (bool , optional): disables events
    """  
    
    files              = []
    pad                = None  # for now only pads
    directory          = sep
    __count_selected   = 0
    double_click_DELAY = 0.4 
    vim_mode           = False
    info_label         = None
    
    def __init__(self, y=0, x=0, height=30, width=45, anchor=(False,False,False,False), directory=HOME_DIR, suffixes=['*'], sort_by=None, has_label=True,win=None, draw_files=True, termux_touch_only=True, auto_find_on_typing=True, vim_mode=False, color_pair_offset=0, is_focused=False):
        if has_label:
            height -= 1
            self.info_label       = Label(y+height, x, 1, width, (False,anchor[1],anchor[2],anchor[3]), '', color_pair_offset, win)
            self.info_label.style = unicurses.A_REVERSE | unicurses.A_BOLD 

        super().__init__(win, y, x, height, width, anchor, is_focused, color_pair_offset) 
        self.suffixes            = suffixes
        self.draw_files          = draw_files
        self.termux_touch_only   = termux_touch_only
        self.auto_find_on_typing = auto_find_on_typing
        self.menu                = TUIMenu(color_pair_offset=color_pair_offset)

        if directory:
            self.directory = os.path.normpath(directory)
            self.load_files(directory, suffixes, sort_by)
            if draw_files:
                self.draw()

        if stty_a('^C') or unicurses.OPERATING_SYSTEM == 'Windows': signal.signal(signal.SIGINT,self.copy) # https://docs.microsoft.com/en-us/windows/console/ctrl-c-and-ctrl-break-signals
        if os.getenv('tuifi_vim_mode', str(vim_mode)) == 'True'   : self.toggle_vim_mode()
    
    
    
    def draw(self):
        unicurses.werase(self.pad)
        #self.refresh()
        if self.maxpLines < self.height:
            self.maxpLines = self.height 
        unicurses.wresize(self.pad, self.maxpLines, self.width)
        for f in self.files:
            f.draw(self.pad, color_pair_offset=self.color_pair_offset)
    
    
    #def get_TUIFIProfile_by_key(self, key): # https://stackoverflow.com/a/2974082/11465149       
        #return next((v for k, v in TUIFIProfiles.items() if (key == k) or (isinstance(k,tuple) and key in k)),FILE_profile)
        
    
    def get_profile(self, file_directory, new=False):
        if os.path.isdir(file_directory):
            temp_profile = TUIFIProfiles.get(':empty_folder')
            for suffix in self.suffixes:
                if len(list(Path(file_directory + sep).glob(suffix))) != 0:
                    temp_profile = TUIFIProfiles.get(':folder')
                    break
        else:
            file_extension = os.path.splitext(file_directory)[1]
            if not file_extension: 
                file_extension = os.path.basename(file_directory) 
            else:
                file_extension = '/' + file_extension[1:]
            temp_profile = TUIFIProfiles.get(file_extension.lower(),DEFAULT_PROFILE) # ..[-1] = extension  
        return temp_profile
    
    
    def load_files(self, directory, suffixes=None, sort_by=None):  # DON'T load and then don't show :P
        directory = os.path.realpath(os.path.normpath(directory))
        if not os.path.isdir(directory):
            raise Exception('DirectoryNotFound: "' + directory + '"') 
        if suffixes == None: 
            suffixes = self.suffixes 
        
        self.directory = directory
        self.files = []
        glob_files = []
        glob_files.append(directory + sep + '..')
        for suffix in suffixes:
            glob_files.extend(Path(directory + sep).glob(suffix))
        
        max_h, pCOLS, count, y, x = 0, self.width, 0, PADDING_TOP, PADDING_LEFT 
        for f in glob_files:
            f            = str(f)
            is_link      = os.path.islink(f)
            filename     = f.split(sep)[-1]
            file_        = TUIFile(filename, y, x, self.get_profile(f), is_link=is_link)
            tempX        = (PADDING_LEFT + file_.profile.width + PADDING_RIGHT)
            self.files.append(file_)
            
            if x > pCOLS-tempX + PADDING_RIGHT - self.x :
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
            self.maxpLines = y + max_h + PADDING_TOP + PADDING_BOTTOM + self.y     
        else:
            self.maxpLines = y + self.y

        if not self.is_in_find_mode: self.__set_label_text(f'[{len(glob_files)-1:04}] {directory}') # just because i know that len is stored as variable,  that's why i don;t count them in for loop
        return self.files
    
    
    def resort(self): #draw_files=True # repeating code but nvm 
        """In case of resize, call this function to resort/replace existing files to the new dimensions of pad 

        Returns:
            list: self.files
        """
        unicurses.werase(self.pad)
            
        max_h, pCOLS, count, y, x = 0, self.width, 0, PADDING_TOP, PADDING_LEFT 
        for f in self.files:
            tempX = (PADDING_LEFT + f.profile.width + PADDING_RIGHT)
            if x > pCOLS-tempX + PADDING_RIGHT - self.x :
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
                    self.maxpLines = y + max_h + PADDING_TOP + PADDING_BOTTOM  + self.y
                else:
                    self.maxpLines = y + self.y 
                if self.maxpLines < self.height:
                    self.maxpLines = self.height 
                unicurses.wresize(self.pad, self.maxpLines, self.width) 
                
            f.draw(self.pad,redraw_icon=True, color_pair_offset=self.color_pair_offset)
            
        #unicurses.wresize(self.pad, self.maxpLines, self.width) # because it works doesn't also mean that i should do it like that  

        #if self.position.iy >= unicurses.getmaxy(self.pad) - self.height + self.y:
            #self.position.iy = unicurses.getmaxy(self.pad) - self.height
        #if self.height + self.position.iy > y:
        #    self.position.iy -= self.height + self.position.iy - y  # NOT SURE AT ALL BUT IT WORKS LOL, actually NOP ):(            
        #self.draw() 
        #self.select(self.__clicked_file) #  ??????????????
        return self.files
        
    
    def reload(self,draw_files=True):
        self.position.iy             = 0
        self.__clicked_file          = None
        self.__index_of_clicked_file = None
        self.load_files(self.directory)
        if draw_files:
            self.draw()
    
    
    @contextmanager
    def suspend(self):
        """
        Suspend curses in order to open another subprocess in the terminal.
        """
        try:
            unicurses.endwin()
            yield
        finally:
            unicurses.doupdate()
    
    
    def open(self, directory, suffixes=None, sort_by=None, _with=None):
        """
        `open()` is `load_files()` + `draw()`
        """
        if directory in (None,''):
            return None
        if isinstance(directory,TUIFile):
            directory = self.directory + sep + directory.name
        if not os.path.isdir(directory) or _with:
            open_with = TUIFIProfiles.get('/'+os.path.splitext(directory)[1][1:],DEFAULT_PROFILE).open_with if not _with else _with
            if open_with:
                with self.suspend():
                    proc = subprocess.Popen([open_with, directory], shell=IS_WINDOWS)
                    proc.wait()
                
                #if STTY_EXISTS:  # Meh..
                #    os.system('stty sane')
                #os.execl(sys.argv[0], sys.argv[0], self.directory)  # Meeeeeeeh
                
                #subprocess.call(['tuifi', self.directory])  # sys.executable, __file__
                #subprocess.call(['micro', directory])   
            return None

        self.is_in_find_mode                = False
        self.__change_escape_event_consumed = False
        self.escape_event_consumed          = False
        self.__temp_findname                = ''
        self.__clicked_file          = None
        self.__pre_clicked_file      = None
        self.__index_of_clicked_file = None
        self.__count_selected        = 0
        self.position.iy             = 0
        self.load_files(directory, suffixes, sort_by)
        self.draw()
        return self.files
    

    def refresh(self):
        super().refresh()
        if self.info_label:
            self.info_label.refresh()
        self.menu.refresh()


    def get_tuifile_by_name(self, name):
        return next((f for f in self.files if f.name == name), None)
    
    
    def get_tuifile_by_coordinates(self, y, x, relative_to_pad=False, return_enumerator=False):
        if not relative_to_pad:
            y += self.position.iy - self.y
            x -= self.x 
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
                    f.draw(self.pad, color_pair_offset=self.color_pair_offset)     
            self.__count_selected = 0 # i can just -= 1 and break it if 0 :P
        else:
            tuifile.is_selected = False
            tuifile.draw(self.pad, color_pair_offset=self.color_pair_offset)
            self.__count_selected -=1
                  
        
    def select(self, tuifile):
        self.__count_selected +=1
        if not tuifile: 
            return
        #for y in range(tuifile.y, tuifile.y + tuifile.profile.height):
        #    mvwchgat(self.pad,y, tuifile.x, tuifile.profile.width,A_REVERSE,7)
        tuifile.is_selected = True
        tuifile.draw(self.pad, color_pair_offset=self.color_pair_offset)
                
    
    def scroll_pad(self, y):
        if self.position.iy == 0 and y < 0:
            return
        if self.position.iy >= unicurses.getmaxy(self.pad) - self.height  and y > 0:
            return
        self.position.iy += y
    
    
    is_on_termux_select_mode   = False
    __mouse_btn1_pressed_file  = None
    __pre_clicked_file         = None
    __clicked_file             = None
    __index_of_clicked_file    = None
    __start_time               = 0
    __temp__copied_files       = [] 
    __temp_dir_of_copied_files = ''
        
    events = { # Disable or replace Events if you want (with 0x11111111? and None for CTRL(x)? i think) | UPDATE: lol wtf i did, i could just used them instead of if-elif pointing to functions but ... | lol i said the same thing on an UPDATE comment
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
        #'ALT_LEFT'              : 'kLFT3'                                ,
        'KEY_F5'                : unicurses.KEY_F(5)                     ,
        'CTRL_R'                : unicurses.CTRL('R')                    ,
        'CTRL_X'                : unicurses.CTRL('X')                    ,  
        'CTRL_C'                : unicurses.CTRL('C')                    ,  
        'CTRL_K'                : unicurses.CTRL('K')                    ,  
        'CTRL_V'                : unicurses.CTRL('V')                    ,  
        'CTRL_N'                : unicurses.CTRL('N')                    ,  
        'CTRL_W'                : unicurses.CTRL('W')                    , 
        'CTRL_F'                : unicurses.CTRL('F')                    , 
        'CTRL_O'                : unicurses.CTRL('O')                    , # https://stackoverflow.com/a/33966657/11465149
        'CTRL_S'                : unicurses.CTRL('S')                    , # TODO: SELECT
    }  
    def toggle_vim_mode(self): # TODO: Use it in rename and find or something
        if self.vim_mode:
            self.vim_mode = False
            # TODO revert events Map 
        else:
            self.vim_mode = True
            self.auto_find_on_typing = False 
            self.events['KEY_ENTER']     = (unicurses.CCHAR('o'), unicurses.CCHAR('K'), unicurses.KEY_ENTER, 10) 
            self.events['KEY_BACKSPACE'] = (unicurses.CCHAR('b'), unicurses.CCHAR('J')) 
            self.events['KEY_UP'   ]     =  unicurses.CCHAR('k') 
            self.events['KEY_DOWN' ]     =  unicurses.CCHAR('j') 
            self.events['KEY_LEFT' ]     =  unicurses.CCHAR('h') 
            self.events['KEY_RIGHT']     =  unicurses.CCHAR('l') 
            self.events['CTRL_O'   ]     =  unicurses.CCHAR('O')
            self.events['KEY_HOME' ]     =  unicurses.CCHAR('H')
            self.events['CTRL_X'   ]     =  unicurses.CCHAR('c')
            self.events['CTRL_C'   ]     =  unicurses.CCHAR('y')
            self.events['CTRL_W'   ]     =  unicurses.CCHAR('w')
            self.events['CTRL_N'   ]     =  unicurses.CCHAR('W')
            self.events['CTRL_V'   ]     =  unicurses.CCHAR('p')
            self.events['CTRL_R'   ]     =  unicurses.CCHAR('r')
            self.events['CTRL_F'   ]     =  unicurses.CCHAR('i')
            self.events['KEY_DC'   ]     =  unicurses. CTRL('d')
            self.events['CTRL_S'   ]     =  unicurses.CCHAR('s') # TODO: select
            # TODO Map  events 


    def __set_label_text(self, text):
        if self.info_label:
            self.info_label.text = text


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
        if deselect:
            self.deselect()
        if select:
            self.select(tuifile)
        if tuifile.y - PADDING_TOP < self.position.iy :
            self.position.iy = tuifile.y - PADDING_TOP
            return
        temp_sum_of_Y__y_and_height_of_tuifile = self.y + tuifile.y + tuifile.profile.height + tuifile.name_height + PADDING_TOP
        temp_sum_of_visible_H_and_Y =  self.height + self.position.iy                       
        if temp_sum_of_Y__y_and_height_of_tuifile > temp_sum_of_visible_H_and_Y  :
            self.position.iy += temp_sum_of_Y__y_and_height_of_tuifile - (temp_sum_of_visible_H_and_Y )
  
  
    __is_cut = False
    def cut(self):
        """
        Cut-copies the selected files | Not fully implemented yet
        """
        self.__is_cut = True  # TODO: DON'T FORGET TO CHANGE TERMUX CUT WHEN NEW VERSION[...]
        self.__stack_files_for_action()
        
         
    def copy(self, signum=None, frame=None):
        """
        Copies the selected files (ignore signum=None, frame=None [...]) | Not fully implemented yet
        """ 
        self.__is_cut = False
        self.__stack_files_for_action()    


    def __stack_files_for_action(self):
        """
        this function is TEMPOTATY and will be REMOVED, 
        it will be pressent until i find a way of drawing/managing cutted files efficiently
        """   
        if self.__count_selected == 0 or (self.__clicked_file and self.__clicked_file.name == '..') : return
        size = 0
        self.__temp_dir_of_copied_files = self.directory
        if self.__count_selected == 1:
            self.__temp__copied_files = [self.__clicked_file]                 
        else:
            self.__temp__copied_files = []
            for f in self.files:                      
                if f.is_selected:
                    self.__temp__copied_files.append(f) 
                    size += os.path.getsize(self.directory + sep + f.name)

        length = len(self.__temp__copied_files)
        text   = f'{length} files [{size} bytes]' if length > 1 else f'{self.__clicked_file.name}'
        action = 'CUTED' if self.__is_cut else 'COPIED'
        self.__set_label_text(f'[{action}]: {text}')
                        
                        
    def __duplicate(self):
        for f in self.__temp__copied_files:
            source      = self.__temp_dir_of_copied_files + sep + f.name
            destination = self.directory                  + sep 
            i = 1 
            if os.path.isfile(source):        # Does 'file' exist? 
                method_copy = shutil.copyfile
                exists      = os.path.isfile
            elif os.path.isdir(source):       # Does 'directory' exist?                
                method_copy = shutil.copytree
                exists      = os.path.isdir
            else:                             # if source doesn't exist continue with loop
                continue
            while exists(f'{destination}{i}_{f.name}'):
                i += 1
            method_copy(source, f'{destination}{i}_{f.name}')


    def __copy_cut(self):
        for f in self.__temp__copied_files:
            source      = self.__temp_dir_of_copied_files + sep + f.name
            destination = self.directory                  + sep + f.name
            if os.path.isfile(source):   # Does 'file' exist?
                if not self.__is_cut: shutil.copyfile(source, destination, follow_symlinks=False)
                else                : shutil.move    (source, destination)
            elif os.path.isdir(source):  # Does 'directory' exist?                
                if not self.__is_cut: shutil.copytree(source, destination, symlinks=True)
                else                : shutil.move    (source, destination)


    def paste(self): # TODO: ask to check if overwrite on copy
        """
        Pastes the already selected and copied/cutted files.
        """
        if len(self.__temp__copied_files) == 0 or not os.path.exists(self.__temp_dir_of_copied_files): return # u never no if the user deleted anything from other file manager this is also something i haven't consider for the rest of the things and [...]
        if not self.__temp_dir_of_copied_files == self.directory: self.__copy_cut ()
        else                                                    : self.__duplicate()
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
                self.__clicked_file          = self.files[temp_i]
                self.__pre_clicked_file      = None # hmm.. sus?
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
                        self.__clicked_file          = self.files[temp_i]
                        self.__pre_clicked_file      = None # hmm.. sus
                        self.select(self.__clicked_file)
                        break
   
   
    def clear_find_results(self):
        self.is_in_find_mode                = False
        self.__change_escape_event_consumed = True
        self.__temp_findname                = ''
        self.__clicked_file                 = self.files[0] # https://github.com/GiorgosXou/TUIFIManager/issues/25
        self.__index_of_clicked_file        = 0
        self.load_files(self.directory)
        self.draw() # i might want to scroll_to_file after that here too? or nah..
        
   
    __mouse_keys = (events.get('BUTTON1_DOUBLE_CLICKED'),events.get('KEY_MOUSE'),events.get('BUTTON4_PRESSED'),events.get('BUTTON5_PRESSED'),events.get('BUTTON1_PRESSED'),events.get('BUTTON1_RELEASED'),events.get('BUTTON1_CLICKED'),events.get('BUTTON3_PRESSED'),events.get('BUTTON3_RELEASED' ))
    __arrow_keys = (events.get('KEY_UP'), events.get('KEY_DOWN'), events.get('KEY_LEFT'), events.get('KEY_RIGHT') )
    is_in_find_mode = False
    __temp_findname = ''
    def handle_find_events(self,event): # TODO: FIX SUFFIXES WHEN DELETING, find_file
        if event == 27: 
            if self.vim_mode:
                i = 0 if len(self.files) == 1 else 1
                self.__change_escape_event_consumed = True
                self.is_in_find_mode                = False
                self.__index_of_clicked_file        = i
                self.__clicked_file                 = self.files[i]
                self.__set_label_text('[NORMAL]')
                return False
            self.clear_find_results()
            return True 
        elif event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
            if len(self.__temp_findname) > 1:
                self.__temp_findname = self.__temp_findname[:-1]
            else:
                self.clear_find_results()
                return True
        elif event in self.__arrow_keys or unicurses.CTRL(event) == event:
            i = 0 if len(self.files) == 1 else 1
            self.__change_escape_event_consumed = True
            self.is_in_find_mode                = False
            self.__index_of_clicked_file        = i
            self.__clicked_file                 = self.files[i]
            return False
        elif event in (unicurses.KEY_ENTER,10) or event == unicurses.KEY_RESIZE or event in self.__mouse_keys or event == unicurses.KEY_HOME: # Ignore this shit :P
            return False
        else:
            self.__temp_findname += unicurses.RCCHAR(event)

        self.find_file(self.__temp_findname)
        self.__set_label_text(f'SEAERCH: {self.__temp_findname}')
        i = 0 if len(self.files) == 1 else 1
        self.__clicked_file          = self.files[i]
        self.__index_of_clicked_file = i

        self.scroll_to_file(self.__clicked_file, True, True)    
        return True
    

    def find_file(self, filename): # meh, slightly computationally expensive but easier to implement, whatever at least it does it's job lol 
        suffs = []
        for suf in self.suffixes:
            suffs.append(suf.replace('*', '*' + filename + '*'))
        self.load_files(self.directory, suffs) 
        self.draw()


    def find(self):
        self.__set_label_text('[INPUT]')
        self.is_in_find_mode = True
        self.escape_event_consumed = True
        self.__temp_findname = '' # just ot make sure although it might not be need it


    def rename(self):
        if self.__clicked_file: 
            self.__set_label_text(f'[RENAMING] {self.__clicked_file.name}')
            self.escape_event_consumed = True
            self.__clicked_file.draw_name(self.pad, self.__clicked_file.name, '', 0, unicurses.A_UNDERLINE, self.color_pair_offset)  # Yeah ok, whatever
            self.__temp_name        = self.__clicked_file.name
            self.__temp_pre_name    = self.__temp_name
            self.__first_pass       = True
                    
    
    escape_event_consumed          = False
    __first_pass                   = True
    __change_escape_event_consumed = False  # on second loop 
    __temp_pre_name                = ''
    __temp_name                    = ''
    __temp_i                       = 0
    __illegal_filename_characters  = ('<', '>', ':',  '/', '\\', '|', '?', '*', '"')
    def handle_rename_events(self, event):  # At this momment i don't even care about optimizing anything... just kidding, you get the point, no free time | TODO: change event == ... to self.events.get(...)
        if event == unicurses.KEY_LEFT:
            if not self.__temp_i == 0: self.__temp_i -= 1
        elif event == unicurses.KEY_RIGHT:
            if not self.__temp_i == len(self.__temp_name): self.__temp_i += 1
        elif unicurses.RCCHAR(event) in self.__illegal_filename_characters:
            return 
        elif event == 27 or event in (unicurses.KEY_ENTER,10):
            self.__temp_i                       = 0
            self.__change_escape_event_consumed = True
            new_path_name                       = self.directory + sep + self.__temp_name
            if not event == 27 and not self.__temp_name.strip() == '' and not os.path.exists(new_path_name):  
                os.rename(self.directory + sep + self.__clicked_file.name, new_path_name)        
                self.__clicked_file.name    = self.__temp_name
                self.__clicked_file.profile = self.get_profile(new_path_name)
                self.resort()
                self.scroll_to_file(self.__clicked_file, True, True)
            else:
                self.__temp_name = self.__clicked_file.name
        elif event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
            if not self.__temp_i == 0:
                self.__temp_i -= 1
                self.__temp_name = self.__temp_name[0:self.__temp_i] + self.__temp_name[self.__temp_i+1:]                
            elif self.__first_pass:
                self.__temp_name = ''    
        elif event == unicurses.KEY_HOME:
            self.__temp_i = 0
        elif event == unicurses.KEY_END:
            self.__temp_i = len(self.__temp_name)
        elif self.__first_pass:
            self.__temp_name = unicurses.RCCHAR(event)
            self.__temp_i += 1  
        else:
            self.__temp_name = self.__temp_name[0:self.__temp_i] + unicurses.RCCHAR(event) + self.__temp_name[self.__temp_i:]
            self.__temp_i += 1  
        self.__clicked_file.draw_name(self.pad,self.__temp_name,self.__temp_pre_name, self.__temp_i, color_pair_offset=self.color_pair_offset)
        self.__temp_pre_name = self.__temp_name
        self.__first_pass    = False
        #if event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
        #    pass
    
    
    def create_new(self,_type='folder'): # temporary implementation but nvm      
        i, j = '', 0
        if _type == 'folder': exists = os.path.isdir
        else                : exists = os.path.isfile 
        while exists(self.directory + sep + 'New ' + _type + i):  
            i = ' (' + str(j) + ')'
            j += 1 
        filename = 'New ' + _type + i
        if _type == 'folder': 
            os.mkdir(self.directory + sep + filename)
            _type = 'empty_folder'
        else                : 
            open(self.directory + sep + filename, 'w').close()
        self.deselect()
        self.__clicked_file = TUIFile(filename, profile=TUIFIProfiles.get(':'+_type))
        self.__index_of_clicked_file = 1
        self.files.insert(1,self.__clicked_file)
        self.resort()
        self.scroll_to_file(self.__clicked_file,True,True)
        self.rename()
    

    def __int_len(self, n): # https://stackoverflow.com/a/2189827/11465149
        return int(log10(n))+1 if n != 0 else 0

    def __set_label_on_file_selection(self):
        if not self.info_label: return
        path = self.directory + sep + self.__clicked_file.name
        if os.path.isfile(path):
            info = f'[{os.path.getsize(path)} bytes]'
        else:
            info = ''
        offset = self.__int_len(max(len(self.files),999)) + 3 + self.__int_len(self.__index_of_clicked_file) + 3 + len(info) + 2
        self.info_label.text = f'[{len(self.files)-1:04}] [{self.__index_of_clicked_file}] { path[max(len(path)-self.info_label.width + offset,0):len(path)]} {info}' # just because i know that len is stored as variable,  that's why i don;t count them in for loop

                        
    def __perform_menu_selected_action(self, action):  # TODO: USE DICT INSTEAD OF IF, ELIF
        if   action == 'Open'      : self.open  (self.__clicked_file)
        elif action == 'Cut'       : self.cut   ()
        elif action == 'Delete'    : self.delete()
        elif action == 'Copy'      : self.copy  ()
        elif action == 'Paste'     : self.paste ()
        elif action == 'Rename'    : self.rename()
        elif action == 'New File'  : self.create_new('file')
        elif action == 'New Folder': self.create_new('folder')
        elif action == 'Reload'    : self.reload()
            
                            
    def handle_events(self, event): # wtf, ok .. works acceptably :P, TODO: REMOVE rrrrepeating code but nvm for now >:( xD  | UPDATE: WHAT HAVE I DONE, WHY SO MANY IF AND NOT JSUT A DIRCT WITH FUNCTIONS
        if event == 0 or not self.is_focused: return  # https://github.com/GiorgosXou/TUIFIManager/issues/24 
        if self.escape_event_consumed == True: # REDIRECT ALL KEYBOARD EVENTS 
            if not self.__change_escape_event_consumed: 
                if self.is_in_find_mode:
                    if self.handle_find_events(event): 
                        return
                else:
                    self.handle_rename_events(event) 
                    return
            else:
                self.__change_escape_event_consumed = False
                self.escape_event_consumed = False
        
        action = self.menu.handle_keyboard_events(event)  # if performed the event   
        if action: # action-εστί που λεμε και στη βυζαντινη
            self.__perform_menu_selected_action(action)         
            return
        
        if event == self.events.get('KEY_MOUSE'): 
            in_range, id, x, y, z, bstate = self.get_mouse()
            if not in_range: return
            action = self.menu.handle_mouse_events(id, x, y, z, bstate)
            if action:
                self.__perform_menu_selected_action(action)
                return
            

            if bstate & self.events.get('BUTTON4_PRESSED'):
                self.scroll_pad(UP) 
            elif bstate & self.events.get('BUTTON5_PRESSED'):
                self.scroll_pad(DOWN)  
                # ------------ SORRY FOR THAT MESS BELLOW I LL FIX IT AT SOME POINT -------------------
            elif (not IS_TERMUX) or (IS_TERMUX and not self.termux_touch_only): # because there are some times that long like presses might be translated to BUTTON1_PRESSED instead of CLICK
                if (bstate & self.events.get('BUTTON1_RELEASED')) or (bstate & self.events.get('BUTTON3_RELEASED')) or (unicurses.OPERATING_SYSTEM == 'Windows' and bstate & self.events.get('BUTTON1_DOUBLE_CLICKED')): # unicurses.OPERATING_SYSTEM == 'Windows' because issues with ncurses 
                    self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
                    self.__delay1 = time() - self.__delay1
                    sumed_time = time() - self.__start_time - self.__delay1 # yeah whatever
                    if self.__clicked_file: self.__set_label_on_file_selection() # Hell, pain on my eyes, lol
                    
                    if (self.__mouse_btn1_pressed_file == self.__clicked_file and not bstate & self.events.get('BUTTON_CTRL')) :
                        if not ((bstate & self.events.get('BUTTON3_RELEASED')) and self.__count_selected > 1 and self.__clicked_file and self.__clicked_file.is_selected): 
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
            self.handle_resize(False)
            self.resort()
            if self.info_label:
                self.info_label.handle_resize(False)
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
                        self.__index_of_clicked_file   = i -1
                        self.__clicked_file            = self.files[i-1]
                        self.__mouse_btn1_pressed_file = self.__clicked_file
                        self.__pre_clicked_file        = self.__clicked_file
                        self.scroll_to_file(self.__clicked_file, True)
                        break
                self.__set_label_on_file_selection()
            else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                self.select(self.files[0])
                self.__clicked_file = self.files[0]
                self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_DOWN'):
            if not self.__index_of_clicked_file == None:
                for i in range(self.__index_of_clicked_file,len(self.files)-1):
                    if (self.files[i+1].y > self.files[self.__index_of_clicked_file].y) and (self.files[i+1].x >= self.files[self.__index_of_clicked_file].x):
                        self.deselect()
                        self.__index_of_clicked_file   = i +1
                        self.__clicked_file            = self.files[i+1]
                        self.__mouse_btn1_pressed_file = self.__clicked_file
                        self.__pre_clicked_file        = self.__clicked_file
                        self.scroll_to_file(self.__clicked_file, True)
                        break
                self.__set_label_on_file_selection()
            else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                self.select(self.files[0])
                self.__clicked_file = self.files[0]
                self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_RIGHT'): # __arrow_key_navigation
            if not self.__index_of_clicked_file == len(self.files) - 1:
                if not self.__index_of_clicked_file == None:
                    self.deselect()
                    self.__index_of_clicked_file   = self.__index_of_clicked_file +1
                    self.__clicked_file            = self.files[self.__index_of_clicked_file]
                    self.__mouse_btn1_pressed_file = self.__clicked_file
                    self.__pre_clicked_file        = self.__clicked_file
                    self.scroll_to_file(self.__clicked_file, True)
                    self.__set_label_on_file_selection()
                else: # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
                    self.select(self.files[0])
                    self.__clicked_file = self.files[0]
                    self.__index_of_clicked_file = 0
                
        elif event == self.events.get('KEY_LEFT'):
            if not self.__index_of_clicked_file == 0:
                if not self.__index_of_clicked_file == None:
                    self.deselect()
                    self.__index_of_clicked_file   = self.__index_of_clicked_file -1
                    self.__clicked_file            = self.files[self.__index_of_clicked_file]
                    self.__mouse_btn1_pressed_file = self.__clicked_file
                    self.__pre_clicked_file        = self.__clicked_file
                    self.scroll_to_file(self.__clicked_file, True)
                    self.__set_label_on_file_selection()
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
                
        elif event == self.events.get('CTRL_R'): self.rename()
        elif event == self.events.get('KEY_DC'): self.delete()  # TODO: FIX ISSUE WHEN NAVIGATING trough link and deleting | Update i think i fixed it lol
        elif event == self.events.get('KEY_F5'): self.reload()  
        elif event == self.events.get('CTRL_C'): self.copy  ()  # or KEY_IC ? | copy selected files
        elif event == self.events.get('CTRL_K'): self.copy  () 
        elif event == self.events.get('CTRL_X'): self.cut   ()  
        elif event == self.events.get('CTRL_V'): self.paste ()  # check if path the  same as self.directory maybe?
        elif event == self.events.get('CTRL_W'): self.create_new('file')
        elif event == self.events.get('CTRL_N'): self.create_new('folder')        
        elif event == self.events.get('CTRL_F'): self.find() # Not tested, but i think it works | to enable find mode and consume escape event
        elif event == self.events.get('CTRL_O'): self.open(self.__clicked_file, _with=DEFAULT_WITH) 

        #     VVVVVVVVVVVV TEMPORARY FIX
        # elif not IS_TERMUX and event == 526: # self.events.get('ALT_DOWN'): # unicurses.keyname(event) TODO: FIX unicurses keyname that returns None if no decode()
        #     if self.menu.exists:
        #         self.menu.delete()
        #     else:
        #         self.menu.create(self.__clicked_file.y,self.__clicked_file.x +1)

        else:
            if IS_TERMUX: # TERMUX ONLY, EASILY ACCESIBLE KEYBINDINGS  
                if unicurses.keyname(event) == self.events.get('CTRL_DOWN'): # 
                    if self.is_on_termux_select_mode:  # hmm..
                        self.is_on_termux_select_mode = False
                        self.copy()
                        return
                    else:
                        self.is_on_termux_select_mode = True 
                        return
                elif unicurses.keyname(event) == self.events.get('CTRL_LEFT'):
                    if self.is_on_termux_select_mode:
                        self.is_on_termux_select_mode = False
                        self.cut()
                        return
                    else:
                        self.__is_cut = True
                        return
                elif unicurses.keyname(event) == self.events.get('CTRL_UP'):
                    self.paste()
                    return
                elif event == self.events.get('KEY_END'):
                    if self.is_on_termux_select_mode:
                        self.is_on_termux_select_mode = False
                    self.delete()
                    return
            
            # this thing i think it will mess up alot with the customization so i'll itroduce a variable auto_find_on_typing
            if self.auto_find_on_typing and event != 27:
                self.find() # to enable find mode and consume escape event
                self.handle_find_events(event)
                
        #else: # TODO: SEARCH FOR FILENAME AND DRAW FINDINGS or i can just open the same folder with suffixes by replacing all * with ('*' + str + '*')? lazy way but cool one too xD | search mode when typing | lol i have an elif IS_TERMUX
            #unicurses.waddstr(self.pad, unicurses.keyname(event))
            
        #TODO: return event\action or none if any performed 


"""
- 2022-12-19 01:15:32 AM REMINDER: THE REASON WHY I USED self.position.iy INSTEAD OF self.iy IS BECAUSE CHANGING IT THAT WAY DOESN'T REDRAW THE WINDOW
- 2022-12-21 08:23:25 PM REMINDER: What if i rename .. folder?
"""
