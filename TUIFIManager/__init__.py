#TODO: I NEED TO ADD GETTERS AND SETTERS FOR Y AND X BECAUSE THEY NEED unicurses.touchwin(self.parent.win)
#TODO: I NEED TO CHECK FOR WRITE/READ/EXECUTE PERMISSIONS (PREVENT EXCEPTIONS\ERRORS)

from     contextlib import contextmanager
from     send2trash import send2trash
from      functools import partial
from        pathlib import Path
from         typing import Optional, Final
from           time import time
from             os import sep
from           math import log10
from       .TUIMenu import TUIMenu
from       .TUIFile import TUIFile
from   .TUItilities import Component    , Label, END_MOUSE, BEGIN_MOUSE
from  .TUIFIProfile import TUIFIProfiles, DEFAULT_PROFILE , DEFAULT_WITH
import   subprocess
import    unicurses
import       shutil
import       signal
import          ast
import           re
import           os

__version__: Final[str] = "2.3.4"

PADDING_LEFT   = 2
PADDING_RIGHT  = 2
PADDING_TOP    = 1
PADDING_BOTTOM = 0

STTY_EXISTS    = shutil.which('stty')
IS_WINDOWS     = unicurses.OPERATING_SYSTEM == 'Windows'
HOME_DIR       = os.getenv('UserProfile') if IS_WINDOWS else os.getenv('HOME')
CONFIG_PATH    = os.getenv('tuifi_config_path',f'{HOME_DIR}{sep}.config{sep}tuifi')
IS_TERMUX      = 'com.termux' in HOME_DIR

UP             = -1
DOWN           =  1



def stty_a(key=None):  # whatever [...]
    if not STTY_EXISTS:
        return None

    if not key:
        return [s.strip() for s in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';')[4:-3]] # risky? i've no idea.. thats why i've not done the same when "if key:"

    for sig in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';'):
        if sig.endswith(key):
            return sig.split('=')[0].strip()
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

    def __init__(self, y=0, x=0, height=30, width=45, anchor=(False,False,False,False), directory=HOME_DIR, suffixes=None, sort_by=None, has_label=True, win=None, draw_files=True, termux_touch_only=True, auto_find_on_typing=True, vim_mode=False, color_pair_offset=0, is_focused=False):
        if suffixes is None:
            suffixes = ['*']

        if has_label:
            height -= 1
            self.info_label       = Label(y+height, x, 1, width, (False,anchor[1],anchor[2],anchor[3]), '', color_pair_offset, win)
            self.info_label.style = unicurses.A_REVERSE | unicurses.A_BOLD

        super().__init__(win, y, x, height, width, anchor, is_focused, color_pair_offset)
        self.suffixes            = suffixes
        self.draw_files          = draw_files
        self.termux_touch_only   = termux_touch_only
        self.auto_find_on_typing = os.getenv('tuifi_auto_find_on_typing'   , str(auto_find_on_typing)) == 'True' 
        self.auto_cmd_on_typing  = os.getenv('tuifi_auto_command_on_typing', 'False')                  == 'True' 
        self.menu                = TUIMenu(color_pair_offset=color_pair_offset)

        if directory:
            self.directory = os.path.normpath(directory)
            self.load_files(directory, suffixes, sort_by)
            if draw_files:
                self.draw()

        self.load_commands      ()
        self.__set_normal_events()
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
                if list(Path(file_directory + sep).glob(suffix)):
                    temp_profile = TUIFIProfiles.get(':folder')
                    break
        else:
            file_extension = os.path.splitext(file_directory)[1]
            file_extension = f'/{file_extension[1:]}' if file_extension else os.path.basename(file_directory)
            temp_profile   = TUIFIProfiles.get(file_extension.lower(),DEFAULT_PROFILE) # ..[-1] = extension
        return temp_profile


    def load_files(self, directory, suffixes=None, sort_by=None):  # DON'T load and then don't show :P
        directory = os.path.realpath(os.path.normpath(directory))
        if not os.path.isdir(directory):
            raise FileNotFoundError(f'DirectoryNotFound: "{directory}"')
        if suffixes is None:
            suffixes = self.suffixes

        self.directory = directory
        self.files = []
        glob_files = [directory + sep + '..']
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

        self.maxpLines = y + self.y if count == 0 else y + max_h + PADDING_TOP + PADDING_BOTTOM + self.y
        if not self.is_in_find_mode: self.__set_label_text(f'[{len(self.files)-1:04}] {directory}') # just because i know that len is stored as variable,  that's why i don;t count them in for loop
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
                if count != 0:
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
        self.__pre_hov               = None           
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


    def __try_open_file_with(self, directory: str, open_with: Optional[str]) -> None:
        if not open_with:
            return self.__set_label_on_file_selection()
        print(END_MOUSE, end='\r')
        with self.suspend():
            proc = subprocess.Popen([open_with, directory], shell=IS_WINDOWS)
            proc.wait()
        print(BEGIN_MOUSE, end='\r')
        self.__set_label_on_file_selection()
        return


    def open(self, directory, suffixes=None, sort_by=None, _with=None):
        """
        `open()` is `load_files()` + `draw()`
        """
        if directory is None or not directory:
            return None

        if isinstance(directory, TUIFile):
            directory = self.directory + sep + directory.name

        if _with:
            return self.__try_open_file_with(directory, _with)

        if not os.path.isdir(directory):
            prof = f'/{os.path.splitext(directory)[1][1:]}'
            open_with = TUIFIProfiles.get(prof, DEFAULT_PROFILE).open_with
            return self.__try_open_file_with(directory, open_with)

        if self.vim_mode and self.escape_event_consumed and not self.is_in_command_mode: # SuS SuS SuS SuS SuS damn that's so Sus lol
            self.find()
        else:
            self.is_in_find_mode       = False
            self.escape_event_consumed = False
        self.__change_escape_event_consumed = False
        self.is_in_command_mode      = False
        self.__temp_findname         = ''
        self.__clicked_file          = None
        self.__pre_clicked_file      = None
        self.__index_of_clicked_file = None
        self.__pre_hov               = None
        self.__count_selected        = 0
        self.position.iy             = 0
        self.load_files(directory, suffixes, sort_by)
        self.draw()
        return self.files


    def refresh(self):
        super().refresh()
        self.menu.refresh()
        if self.info_label:
            self.info_label.refresh()


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


    is_on_select_mode          = False
    __mouse_btn1_pressed_file  = None
    __pre_clicked_file         = None
    __clicked_file             = None
    __index_of_clicked_file    = None
    __start_time               = 0
    __temp__copied_files       = []
    __temp_dir_of_copied_files = ''

    events = {}
    def __set_normal_events(self):
        self.events = {
            unicurses.KEY_UP        : self.__perform_key_up   ,
            unicurses.KEY_DOWN      : self.__perform_key_down ,
            unicurses.KEY_LEFT      : self.__perform_key_left ,
            unicurses.KEY_RIGHT     : self.__perform_key_right,
            unicurses.KEY_BTAB      : self.__perform_key_btab,
            unicurses.KEY_DC        : self.delete,
            unicurses.KEY_F(5)      : self.reload,
            unicurses.CTRL('R')     : self.rename,
            unicurses.CTRL('C')     : self.copy  ,
            unicurses.CTRL('K')     : self.copy  ,
            unicurses.CTRL('X')     : self.cut   ,
            unicurses.CTRL('V')     : self.paste ,
            unicurses.CTRL('W')     : partial(self.create_new, 'file'  ),
            unicurses.CTRL('N')     : partial(self.create_new, 'folder'),
            unicurses.CTRL('F')     : self.find  ,
            unicurses.CTRL('O')     : self.__open_DEFAULT_WITH, # https://stackoverflow.com/a/33966657/11465149
            unicurses.KEY_HOME      : partial(self.open, HOME_DIR),
            unicurses.KEY_ENTER     : self.__perform_key_enter  ,
            10                      : self.__perform_key_enter  ,
            unicurses.KEY_BACKSPACE : self.__open_previous_dir,
            8                       : self.__open_previous_dir,
            127                     : self.__open_previous_dir,
            263                     : self.__open_previous_dir,
            unicurses.KEY_RESIZE    : self.__handle_resize_event,
            32                      : self.command              , # SPACEBAR
        }

    def toggle_vim_mode(self): # TODO: Use it in rename and find or something
        if self.vim_mode:
            self.vim_mode = False
            # TODO revert events Map
        else:
            self.vim_mode = True
            self.auto_find_on_typing = False
            self.auto_cmd_on_typing  = True
            self.events.update({ # TODO: Add s for select via keyboard
                unicurses.CCHAR('k') : self.__perform_key_up             ,
                unicurses.CCHAR('j') : self.__perform_key_down           ,
                unicurses.CCHAR('h') : self.__perform_key_left           ,
                unicurses.CCHAR('l') : self.__perform_key_right          ,
                unicurses.CCHAR('r') : self.rename                       ,
                unicurses.CCHAR('c') : self.cut                          ,
                unicurses.CCHAR('p') : self.paste                        ,
                unicurses.CCHAR('O') : self.__open_DEFAULT_WITH          ,
                unicurses.CCHAR('K') : self.__perform_key_enter          ,
                unicurses.CCHAR('J') : self.__open_previous_dir          ,
                unicurses.CCHAR('b') : self.__open_previous_dir          ,
                unicurses.CCHAR('H') : partial(self.open      , HOME_DIR),
                unicurses.CCHAR('w') : partial(self.create_new, 'file'  ),
                unicurses.CCHAR('W') : partial(self.create_new, 'folder'),
                unicurses.CCHAR('i') : self.find                         ,
                unicurses.CCHAR('O') : self.__open_DEFAULT_WITH          , # https://stackoverflow.com/a/33966657/11465149
                unicurses.CTRL ('D') : self.delete                       ,
            }) # TODO Map  events


    def __set_label_text(self, text):
        if self.info_label:
            self.info_label.text = text


    def __delete_file(self,file):
        if isinstance(file, TUIFile):
            file = self.directory + sep + file.name
        elif not isinstance(file, str):
            raise TypeError('TUIFileTypeError: file must be of type string or TUIFile.')
        if os.path.isfile(file): # checking if exists too.
            if IS_TERMUX: os.remove (file)
            else        : send2trash(file)
        elif os.path.exists(file) and not file.endswith(f'{sep}..'): # "and not .." whatever
            if IS_TERMUX: shutil.rmtree(file)
            else        : send2trash   (file)
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


    def __set_label_on_copy(self,size):
        length = len(self.__temp__copied_files)
        text   = f'{length} files [{size} bytes]' if length > 1 else f'{self.__temp__copied_files[0].name}'  
        action = 'CUTED' if self.__is_cut else 'COPIED'
        self.__set_label_text(f'[{action}]: {text}')


    def __stack_files_for_action(self):
        """
        this function is TEMPORARY and will be REMOVED,
        it will be present until i find a way of drawing/managing cutted files efficiently
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
        self.__set_label_on_copy(size)


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


    def paste(self):  # TODO: ask to check if overwrite on copy
        """
        Pastes the already selected and copied/cutted files.
        """
        if len(self.__temp__copied_files) == 0 or not os.path.exists(self.__temp_dir_of_copied_files): return # u never no if the user deleted anything from other file manager this is also something i haven't consider for the rest of the things and [...]
        if self.__temp_dir_of_copied_files != self.directory: self.__copy_cut ()
        else                                                : self.__duplicate()
        self.reload()


    def delete(self):
        """
        Deletes the selected file(s). | Not fully implemented yet
        """
        if self.__count_selected == 1 and self.__clicked_file :
            # checking under __delete_file too but nvm cause i have no time right now
            if self.__clicked_file.name != '..':
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


    __arrow_keys = (unicurses.KEY_LEFT, unicurses.KEY_RIGHT, unicurses.KEY_DOWN, unicurses.KEY_UP)
    is_in_find_mode = False
    __temp_findname = ''
    def handle_find_events(self,event): # TODO: FIX SUFFIXES WHEN DELETING, find_file
        if event == 27:
            if self.vim_mode:
                self.__change_escape_event_consumed = True
                self.is_in_find_mode                = False
                if self.__temp_findname != '': # When Escaping without searching anything
                    i = 0 if len(self.files) == 1 else 1
                    self.__index_of_clicked_file = i
                    self.__clicked_file          = self.files[i]
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
        elif event in (unicurses.KEY_ENTER,10,unicurses.KEY_RESIZE,unicurses.KEY_MOUSE,unicurses.KEY_HOME): # Ignore this shit :P
            return False
        else:
            self.__temp_findname += unicurses.RCCHAR(event)

        self.find_file(self.__temp_findname)
        self.__set_label_text(f'SEARCH: {self.__temp_findname}')
        i = 0 if len(self.files) == 1 else 1
        self.__clicked_file          = self.files[i]
        self.__index_of_clicked_file = i

        self.scroll_to_file(self.__clicked_file, True, True)
        return True


    def find_file(self, filename): # meh, slightly computationally expensive but easier to implement, whatever at least it does it's job lol
        suffs = [suf.replace('*', f'*{filename}*') for suf in self.suffixes]
        self.load_files(self.directory, suffs)
        self.draw()


    def find(self):
        self.__set_label_text('[INPUT]')
        self.is_in_find_mode = True
        self.escape_event_consumed = True
        self.__temp_findname = '' # just ot make sure although it might not be need it


    def __refine_path(self, path):
        path = HOME_DIR       + path[1:] if path.startswith('~') else path
        path = self.directory + path[1:] if path.startswith('.') else path 
        path = os.path.realpath(os.path.normpath(path))
        return path


    def __cmd_open(self, **args):
        if args['directory']: 
            args['directory'] = self.__refine_path(args['directory'] )
        else:
            args['directory'] = self.__clicked_file
        self.open(**args)


    def __cmd_stack(self, pattern):
        self.__temp__copied_files = []
        size = 0
        if pattern:
            for e in self.files:
                match = re.search(pattern, e.name)
                if match:
                    self.__temp__copied_files.append(e)
                    size += os.path.getsize(self.directory + sep + e.name)
        elif self.__clicked_file:
            size = os.path.getsize(self.directory + sep + self.__clicked_file.name)
            self.__temp__copied_files = [self.__clicked_file]
        if len(self.__temp__copied_files): 
            self.__set_label_on_copy(size)
        else:
            self.__set_label_text('FILES NOT FOUND')


    def __cmd_copy(self, pattern=None):
        self.__is_cut = False
        self.__cmd_stack(pattern)


    def __cmd_cut(self, pattern):
        self.__is_cut = True
        self.__cmd_stack(pattern)


    def __cmd_delete(self, pattern):
        pass


    command_events = {}
    command_types  = {
        'delete' : __cmd_delete , 
        'open'   : __cmd_open   , 
        'copy'   : __cmd_copy   ,
        'cut'    : __cmd_cut    ,
        'find'   : find_file    ,
    }
    def load_commands(self, path=CONFIG_PATH):
        os.makedirs(path, exist_ok=True)
        conf_path = path + sep + 'cmds.conf'
        if not os.path.isfile(conf_path): 
            f = open(conf_path, 'w')
            f.write(
                "gt  | open | 'directory':'~/.config/tuifi' | - tuifi -\n"       +
                "gh  | open | 'directory':'~/'              | - Home -\n"        +
                "owv | open | 'directory':None,'_with':'vim'|Opened With Vim\n"  +
                "yat | copy | 'pattern':'.+\.txt'           |\n"                 +
                "yy  | copy | 'pattern':None                |\n" 
            )
            f.close()
        f = open(conf_path, 'r')
        for line in f:
            ln = line.strip()
            if ln == '': continue
            ln = line.split('|') #  command, args, type, comment | using "|" because this is an __illegal_filename_characters
            self.command_events[ln[0].strip()] = (self.command_types[ln[1].strip()], ast.literal_eval('{'+ln[2].strip()+'}'), ln[3].strip())
        f.close()


    marker_stack = {}
    def __perform_static_cmd_events(self, event):
        if self.__temp_findname.startswith('m'):
            self.__set_label_text('[MARKER]')
            if len(self.__temp_findname) == 2:
                marker = unicurses.RCCHAR(event)
                self.__set_label_text(f'[MARKER] SET TO [{marker}]')
                self.marker_stack[marker]           = self.directory
                self.__temp_findname                = ''
                self.__change_escape_event_consumed = True
                self.is_in_command_mode             = False
            return True
        elif self.__temp_findname.startswith(('`',';')):
            self.__set_label_text('[GOTO MARKER]')
            if len(self.__temp_findname) == 2:
                marker = unicurses.RCCHAR(event)
                dir    = self.marker_stack.get(marker) 
                if dir: 
                    self.open(dir) # scroll to file maby too?
                else: 
                    self.__set_label_text('[MARKER] NOT FOUND')
                    self.__change_escape_event_consumed = True
                    self.is_in_command_mode             = False
            return True
        return False


    is_in_command_mode = False
    def handle_command_events(self, event):
        self.__set_label_text('[COMMAND]')
        if event == 27:
            self.__change_escape_event_consumed = True
            self.is_in_command_mode = False
            self.__temp_findname    = ''
            self.__set_label_text('[NORMAL]')
        else:
            self.__temp_findname += unicurses.RCCHAR(event)
            self.__set_label_text(f'[COMMAND] {self.__temp_findname}')
        if self.__perform_static_cmd_events(event): return True
        cmd = self.command_events.get(self.__temp_findname)
        if cmd:
            self.__change_escape_event_consumed = True # it has to be before cmd call
            cmd[0](self, **cmd[1])
            self.__temp_findname    = ''
            self.is_in_command_mode = False
            if cmd[2]: self.__set_label_text(cmd[2])
        return True


    def command(self):
        self.__set_label_text('[COMMAND]')
        self.is_in_command_mode    = True
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
            if self.__temp_i != 0: self.__temp_i -= 1
        elif event == unicurses.KEY_RIGHT:
            if self.__temp_i != len(self.__temp_name): self.__temp_i += 1
        elif unicurses.RCCHAR(event) in self.__illegal_filename_characters or event == unicurses.KEY_MOUSE:
            return
        elif event in (27, unicurses.KEY_ENTER, 10):
            new_path_name                       = self.directory + sep + self.__temp_name
            self.__temp_i                       = 0
            self.__change_escape_event_consumed = True
            if  event != 27 and self.__temp_name.strip() != '' and not os.path.exists(new_path_name):
                os.rename(self.directory + sep + self.__clicked_file.name, new_path_name)
                self.__clicked_file.name    = self.__temp_name
                self.__clicked_file.profile = self.get_profile(new_path_name)
                self.resort()
                self.scroll_to_file(self.__clicked_file, True, True)
            else:
                self.__temp_name = self.__clicked_file.name
        elif event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
            if self.__temp_i != 0:
                self.__temp_i   -= 1
                self.__temp_name = self.__temp_name[:self.__temp_i] + self.__temp_name[self.__temp_i+1:]
            elif self.__first_pass:
                self.__temp_name = ''
        elif event == unicurses.KEY_HOME: self.__temp_i = 0
        elif event == unicurses.KEY_END : self.__temp_i = len(self.__temp_name)
        elif self.__first_pass:
            self.__temp_name = unicurses.RCCHAR(event)
            self.__temp_i += 1
        else:
            self.__temp_name = self.__temp_name[:self.__temp_i] + unicurses.RCCHAR(event) + self.__temp_name[self.__temp_i:]
            self.__temp_i += 1
        self.__clicked_file.draw_name(self.pad,self.__temp_name,self.__temp_pre_name, self.__temp_i, color_pair_offset=self.color_pair_offset)
        self.__temp_pre_name = self.__temp_name
        self.__first_pass    = False
        #if event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
        #    pass


    def create_new(self,_type='folder'): # temporary implementation but nvm
        i, j = '', 0
        exists = os.path.isdir if _type == 'folder' else os.path.isfile

        while exists(self.directory + sep + 'New ' + _type + i):
            i = f' ({str(j)})'
            j += 1
        filename = f'New {_type}{i}'
        if _type == 'folder':
            os.mkdir(self.directory + sep + filename)
            _type = 'empty_folder'
        else                :
            open(self.directory + sep + filename, 'w').close()
        self.deselect()
        self.__clicked_file = TUIFile(filename, profile=TUIFIProfiles.get(f':{_type}'))
        self.__index_of_clicked_file = 1
        self.files.insert(1,self.__clicked_file)
        self.resort()
        self.scroll_to_file(self.__clicked_file,True,True)
        self.rename()


    def create_new_file  (self): self.create_new('file'  )
    def create_new_folder(self): self.create_new('folder')

    def __int_len(self, n): # https://stackoverflow.com/a/2189827/11465149
        return int(log10(n))+1 if n != 0 else 0

    def __set_label_on_file_selection(self, index=None, file=None):
        if not self.info_label: return
        file = file if file else self.__clicked_file
        index= index if index else self.__index_of_clicked_file
        path = self.directory + sep + file.name
        info = f'[{os.path.getsize(path)} bytes]' if os.path.isfile(path) else ''
        offset = self.__int_len(max(len(self.files),999)) + 3 + self.__int_len(index) + 3 + len(info) + 2
        self.info_label.text = f'[{len(self.files) - 1:04}] [{index}] {path[max(len(path) - self.info_label.width + offset, 0):]} {info}'
        # just because i know that len is stored as variable,  that's why i don;t count them in for loop

    def __open_clicked_file(self):
        return self.open(self.__clicked_file)


    __menu_select_actions = {
        'Open'      : __open_clicked_file           ,
        'Cut'       : cut                           ,
        'Delete'    : delete                        ,
        'Copy'      : copy                          ,
        'Paste'     : paste                         ,
        'Rename'    : rename                        ,
        'New File'  : create_new_file               ,
        'New Folder': create_new_folder             ,
        'Reload'    : reload                        ,
    }
    def __perform_menu_selected_action(self, action):
        if not action : return False
        action_func = self.__menu_select_actions.get(action)
        if action_func: action_func(self) # don't change this, it has to return true even if no action_func() performed else it doesn't overide the events
        return True


    def __handle_termux_touch_events(self, bstate, y, x): # termux needs to implement CTRL + CLICK
        if not (bstate & unicurses.BUTTON1_CLICKED or bstate & unicurses.BUTTON1_PRESSED): return False
        self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
        if not self.is_on_select_mode: self.deselect()

        if self.is_on_select_mode and self.__clicked_file and self.__clicked_file.name != '..' : # bstate & BUTTON_CTRL
            if not self.__clicked_file.is_selected : self.select  (self.__clicked_file)
            else                                   : self.deselect(self.__clicked_file)
        elif self.__clicked_file:
            if self.is_on_select_mode: # AUTO COPY IF IN SELECT-MODE AND CLICKED ON  '..'
                self.is_on_select_mode = False
                self.copy()
            self.open(self.__clicked_file)
        return True


    __x = __y  = 0     # previous position
    hover_mode = False
    __pre_hov  = None # TODO: clear the value when directory change at open
    def __handle_hover_mode(self, y, x):
        if not self.hover_mode: return
        tmp_id_of_hov_file, tmp_hov_file = self.get_tuifile_by_coordinates(y,x, return_enumerator=True)
        if tmp_hov_file and tmp_id_of_hov_file and not tmp_hov_file.is_selected: 
            self.__set_label_on_file_selection(tmp_id_of_hov_file,tmp_hov_file)
            # tmp_hov_file.is_selected = True
            tmp_hov_file.draw_effect(self.pad, color_pair_offset=self.color_pair_offset, effect=0)
            if self.__pre_hov and self.__pre_hov != tmp_hov_file:
                # self.__pre_hov.is_selected = False
                self.__pre_hov.draw(self.pad, color_pair_offset=self.color_pair_offset)
            self.__pre_hov = tmp_hov_file
        elif self.__pre_hov:
            self.__pre_hov.draw(self.pad, color_pair_offset=self.color_pair_offset)
            self.__pre_hov = None



    def __handle_mouse_events(self, event):
        if event != unicurses.KEY_MOUSE: return False
        in_range, id, x, y, z, bstate = self.get_mouse()
        if not IS_WINDOWS and not in_range: return True # TODO: https://github.com/GiorgosXou/TUIFIManager/issues/49
        if self.__perform_menu_selected_action(self.menu.handle_mouse_events(id, x, y, z, bstate)): return True
        if self.__x != x or self.__y != y: self.hover_mode = True #hover mode

        if   not self.hover_mode and (bstate & unicurses.BUTTON4_PRESSED): self.scroll_pad(UP  )
        elif not self.hover_mode and (bstate & unicurses.BUTTON5_PRESSED): self.scroll_pad(DOWN)
        elif not IS_TERMUX or not self.termux_touch_only: # because there are some times that long like presses might be translated to BUTTON1_PRESSED instead of CLICK
            self.__handle_hover_mode(y,x)
            if (bstate & unicurses.BUTTON1_RELEASED) or (bstate & unicurses.BUTTON3_RELEASED) or (unicurses.OPERATING_SYSTEM == 'Windows' and bstate & unicurses.BUTTON1_DOUBLE_CLICKED): # unicurses.OPERATING_SYSTEM == 'Windows' because issues with ncurses
                if self.hover_mode: return True
                self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
                self.__delay1 = time() - self.__delay1
                sumed_time    = time() - self.__start_time - self.__delay1 # yeah whatever
                if self.__clicked_file: self.__set_label_on_file_selection() # Hell, pain on my eyes, lol

                if self.__mouse_btn1_pressed_file == self.__clicked_file and not bstate & unicurses.BUTTON_CTRL:
                    if not ((bstate & unicurses.BUTTON3_RELEASED) and self.__count_selected > 1 and self.__clicked_file and self.__clicked_file.is_selected):
                        self.menu.delete()
                        self.deselect()
                    if bstate & unicurses.BUTTON3_RELEASED:
                        self.menu.create(y,x)
                    if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..' and not self.__mouse_btn1_pressed_file.is_selected :
                        self.select(self.__mouse_btn1_pressed_file )
                    if (((sumed_time < self.double_click_DELAY) and (bstate & unicurses.BUTTON1_RELEASED)) or bstate & unicurses.BUTTON1_DOUBLE_CLICKED) and self.__clicked_file: #and count == 2  :
                        self.open(self.__clicked_file)
                elif self.__clicked_file and self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file == self.__clicked_file: #and not self.__clicked_file.is_selected:
                    if os.path.isdir(self.directory + sep + self.__clicked_file.name):
                        for f in self.files:
                            if f.is_selected:
                                shutil.move(self.directory + sep + f.name, self.directory + sep + self.__clicked_file.name + sep + f.name)
                        self.__pre_clicked_file = None
                        self.reload()

                self.__start_time = time()
            elif (bstate & unicurses.BUTTON1_PRESSED) or (bstate & unicurses.BUTTON3_PRESSED):
                self.__delay1 = time()
                self.__mouse_btn1_pressed_file = self.get_tuifile_by_coordinates(y, x)

                if not bstate & unicurses.BUTTON_CTRL and self.__pre_clicked_file and self.__pre_clicked_file.is_selected and  self.__count_selected == 1:#and summ > self.double_click_DELAY:
                    self.deselect(self.__pre_clicked_file)
                    self.menu.delete()
                if self.__mouse_btn1_pressed_file and self.__mouse_btn1_pressed_file.name != '..':
                    if not self.__mouse_btn1_pressed_file.is_selected and not (bstate & unicurses.BUTTON3_PRESSED):
                        self.select(self.__mouse_btn1_pressed_file)
                    elif bstate & unicurses.BUTTON_CTRL :#and summ > self.double_click_DELAY:
                        self.deselect(self.__mouse_btn1_pressed_file)

                self.__pre_clicked_file = self.__mouse_btn1_pressed_file
        else: self.__handle_termux_touch_events(bstate, y, x)

        self.__x, self.__y = x,y
        self.hover_mode = False
        return True


    def __handle_termux_keyboard_events(self, event):
        if not IS_TERMUX: return False # TERMUX ONLY, EASILY ACCESSIBLE KEYBINDINGS
        if unicurses.keyname(event) == 'kDN5': # CTRL_DOWN
            if self.is_on_select_mode:  # hmm..
                self.is_on_select_mode = False
                self.__set_label_text('[EXITED SELECT MODE]')
                self.copy()
            else:
                self.is_on_select_mode = True
                self.__set_label_text('[ENTERED SELECT MODE]')
            return True
        elif unicurses.keyname(event) == 'kLFT5': # CTRL_LEFT
            if self.is_on_select_mode:
                self.is_on_select_mode = False
                self.__set_label_text('[EXITED SELECT MODE]')
                self.cut()
            else:
                self.__is_cut = True
            return True
        elif unicurses.keyname(event) == 'kUP5': # CTRL_UP
            self.paste()
            return True
        elif event == unicurses.KEY_END:
            if self.is_on_select_mode:
                self.is_on_select_mode = False
            self.delete()
            return True
        return False


    def __handle_resize_event(self):
        self.handle_resize(False)
        self.resort()
        if self.info_label: self.info_label.handle_resize(False)
        unicurses.touchwin(self.parent.win)


    def __is_escape_consumed(self,event):
        if not self.escape_event_consumed: return False # REDIRECT ALL KEYBOARD EVENTS
        if self.__change_escape_event_consumed:
            self.__change_escape_event_consumed = False
            self.escape_event_consumed          = False
        elif self.is_in_find_mode   : return self.handle_find_events   (event)
        elif self.is_in_command_mode: return self.handle_command_events(event)
        else:
            self.handle_rename_events(event)
            return True
        return False


    def __return(self):
        return True


    def __open_previous_dir(self):
        self.open(self.directory + sep + '..'),


    def __open_DEFAULT_WITH(self): # opens folder 
        self.open(self.__clicked_file, _with=DEFAULT_WITH)


    def __perform_key_enter(self):
        if self.__count_selected == 1 and self.__clicked_file.is_selected:
            self.open(self.__clicked_file)


    def __reset_index_of_clicked_file(self) -> None:
        if self.__index_of_clicked_file is not None: return False # sus, maybe elif len(self.files) == 2 ? in case of any issue  with "folder" ".."
        self.select(self.files[0])
        self.__clicked_file = self.files[0]
        self.__index_of_clicked_file = 0
        return True


    def __change_index_of_clicked_file(self, index: int) -> None:
        self.deselect()
        self.__index_of_clicked_file   = index
        self.__clicked_file            = self.files[index]
        self.__mouse_btn1_pressed_file = self.__clicked_file
        self.__pre_clicked_file        = self.__clicked_file
        self.scroll_to_file(self.__clicked_file, True)
        self.__set_label_on_file_selection()


    def __perform_key_up(self):
        if self.__reset_index_of_clicked_file(): return
        for i in range(self.__index_of_clicked_file, 0, -1):
            if (self.files[i - 1].y < self.files[self.__index_of_clicked_file].y) and (self.files[i - 1].x <= self.files[self.__index_of_clicked_file].x):
                self.__change_index_of_clicked_file(i - 1)
                break


    def __perform_key_down(self):
        if self.__reset_index_of_clicked_file(): return
        for i in range(self.__index_of_clicked_file, len(self.files) - 1):
            if (self.files[i + 1].y > self.files[self.__index_of_clicked_file].y) and (self.files[i + 1].x >= self.files[self.__index_of_clicked_file].x):
                self.__change_index_of_clicked_file(i + 1)
                break


    def __perform_key_right(self):
        if self.__index_of_clicked_file == len(self.files) - 1: return
        if self.__reset_index_of_clicked_file()               : return
        self.__change_index_of_clicked_file(self.__index_of_clicked_file + 1)


    def __perform_key_left(self):
        if self.__index_of_clicked_file == 0   : return
        if self.__reset_index_of_clicked_file(): return
        self.__change_index_of_clicked_file(self.__index_of_clicked_file - 1)


    def __perform_key_btab(self):
        if self.__clicked_file and self.__clicked_file.name != '..':
            shutil.move(self.directory + sep + self.__clicked_file.name, self.directory + sep + '..' + sep + self.__clicked_file.name)
            temp_i = self.__index_of_clicked_file - 1
            self.reload()
            self.__index_of_clicked_file = temp_i
            self.__clicked_file = self.files[temp_i]
            self.select(self.__clicked_file)

    def __handle_alt_down(self, event):
        if 'kDN3' != unicurses.keyname(event): return False
        if self.menu.exists: self.menu.delete()
        else               : self.menu.create(self.__clicked_file.y,self.__clicked_file.x +1)
        return True


    def handle_events(self, event): # wtf, ok .. works acceptably :P, TODO: REMOVE rrrrepeating code but nvm for now >:( xD  | UPDATE: WHAT HAVE I DONE, WHY SO MANY IF AND NOT JSUT A DIRCT WITH FUNCTIONS
        if event == 0 or not self.is_focused                                           : return  # https://github.com/GiorgosXou/TUIFIManager/issues/24
        if self.__is_escape_consumed(event)                                            : return
        if self.__perform_menu_selected_action(self.menu.handle_keyboard_events(event)): return

        if self.events.get(event, self.__return)() != True : return # Is this too bad of a practice? let me know
        if self.__handle_mouse_events          (event) : return
        if self.__handle_alt_down              (event) : return
        if self.__handle_termux_keyboard_events(event) : return
        if self.auto_cmd_on_typing and event != 27:
            self.command()
            self.handle_events(event)
        elif self.auto_find_on_typing and event != 27: # this thing i think it will mess up alot with the customization so i'll itroduce a variable auto_find_on_typing
            self.find() # to enable find mode and consume escape event
            self.handle_find_events(event)


            #unicurses.waddstr(self.pad, unicurses.keyname(event))
        #TODO: return event\action or none if any performed


"""
- 2022-12-19 01:15:32 AM REMINDER: THE REASON WHY I USED self.position.iy INSTEAD OF self.iy IS BECAUSE CHANGING IT THAT WAY DOESN'T REDRAW THE WINDOW
- 2022-12-21 08:23:25 PM REMINDER: What if i rename .. folder?
"""
