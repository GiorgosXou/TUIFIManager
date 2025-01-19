#TODO: I NEED TO ADD GETTERS AND SETTERS FOR Y AND X BECAUSE THEY NEED unicurses.touchwin(self.parent.win)
#TODO: I NEED TO CHECK FOR WRITE/READ/EXECUTE PERMISSIONS (PREVENT EXCEPTIONS\ERRORS)

from     contextlib import contextmanager
from     send2trash import send2trash
from      functools import partial
from        pathlib import Path
from         typing import Optional, Final
from           time import time
from             os import sep, access, W_OK, R_OK
from           math import log10
from         typing import Union
from        os.path import basename
from       .TUIMenu import TUIMenu
from       .TUIFile import TUIFile
from      .TUIProps import TUIProps, convert_bytes
from   .TUItilities import WindowPad, Label, END_MOUSE, BEGIN_MOUSE, BEGIN_MOUSE, END_MOUSE, IS_WINDOWS, HOME_DIR, IS_TERMUX, TEMP_PATH, DEFAULT_BACKGROUND, clipboard # DEFAULT_BACKGROUND is imported from __main__
from  .TUIFIProfile import TUIFIProfiles, DEFAULT_PROFILE , DEFAULT_WITH, DEFAULT_OPENER, CONFIG_PATH, TUIFI_THEME, load_theme
import   subprocess
import    unicurses
import     warnings
import       shutil
import       signal
import         json
import          ast
import           re
import           os

__version__: Final[str] = "5.0.9"

PADDING_LEFT   = 2
PADDING_RIGHT  = 2
PADDING_TOP    = 1
PADDING_BOTTOM = 0

HAS_SINGLE_CLICK        = os.getenv('tuifi_has_single_click') == 'True'
SCROLL_SENSITIVITY      = int(os.getenv('tuifi_scroll_sensitivity'     , 2 if not IS_TERMUX else 1))
CTRL_SCROLL_SENSITIVITY = int(os.getenv('tuifi_ctrl_scroll_sensitivity', 7))

UP             = -      SCROLL_SENSITIVITY
DOWN           =        SCROLL_SENSITIVITY
CTRL_UP        = - CTRL_SCROLL_SENSITIVITY
CTRL_DOWN      =   CTRL_SCROLL_SENSITIVITY

STTY_EXISTS    = shutil.which('stty')

HAS_CD_ON_ESC  = os.getenv('tuifi_cd_on_esc') == 'True' or (IS_TERMUX and not os.getenv('tuifi_cd_on_esc') == 'False')
IS_DRAG_N_DROP = os.getenv('tuifi_synth_dnd') == 'True'
if IS_DRAG_N_DROP: 
    from   .TUISynthXDND  import SyntheticXDND
    from   PySide6.QtCore import QUrl
    import requests
    import mimetypes
    import base64


def stty_a(key=None):  # whatever [...]
    if not STTY_EXISTS:
        return None

    if not key:
        return [s.strip() for s in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';')[4:-3]] # risky? i've no idea.. thats why i've not done the same when "if key:"

    for sig in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';'):
        if sig.endswith(key):
            return sig.split('=')[0].strip()
    return None



class TUIFIManager(WindowPad):  # TODO: I need to create a TUIWindowManager class where i will manage all the anchor, resizing and positional stuff for future components (something like Visual-Studio's c#/vb's Winform's behaviour)
    """
    parent     (       win      ): Parent windows in which the Filemanager-pad is hosted.
    pad        ( Window pointer ): The window/Pad where the manager is hosted.
    anchor     ((bool), optional): Anchor refers to the position the Manager window has relative to the edges of the parent one. [top, bottom, left, right]
    y          (int   , optional): y-axis position of pad. Defaults to 0.
    x          (int   , optional): x-axis position of pad. Defaults to 0.
    directory  (str   , optional): Initital directory. Defaults to HOME_DIR which is $HOME or $UserProfile
    suffixes   (list  , optional): "Path expansion rules (file extensions to be found, eg. ['.txt', '.sh', ...]). Defaults to everything.
    sort_by    ([type], optional): [Not implemented yet]. Defaults to None.
    has_label  (bool  , optional): Creates a Label which displays informations about files
    draw_files (bool  , optional): "draws" files the moment of initialization (must unicurses.prefresh to show). Defaults to True.
    termux_touch_only      (bool, optional): if true: full touch, no mouse support else: full mouse half touch support. Defaults to True.
    auto_find_on_typing    (bool, optional): if true: when starting to type, automatically search else only if CTRL_F
    auto_command_on_typing (bool, optional): if true: when starting to type, automatically performs a command else only if space key is pressed
    vim_mode   (bool  , optional): If True: uses vim like keys to navigate. Defaults to False.
    is_focused (bool , optional): disables events
    show_hidden(bool , optional): Show hidden files (you can toggle them by using CTRL+H or use tuifi_show_hidden)
    """

    _instance_count = 0
    double_click_DELAY = 0.4

    def __init_variables(self):
        self.files              = []
        self.directory          = sep
        self.__count_selected   = 0
        self.vim_mode           = False
        self.info_label         = None
        self.basename           = ''
        self.is_in_command_mode = False
        self.__init_variables_for_find_mode   ()
        self.__init_event_variables_and_mouse ()
        self.__init_varibles_for_rename       ()
        self.__init_variables_for_find_mode   ()


    def info_label_clicked(self, *args):
        self.info_label._text = " COPIED DIRECTORY ON CLIPBOARD" if clipboard(self.directory) else " FAILED TO COPY DIRECTORY ON CLIPBOARD"


    def __init__(self, y=0, x=0, height=30, width=45, anchor=(False,False,False,False), directory=HOME_DIR, suffixes=[], sort_by=None, has_label=True, win=None, draw_files=True, termux_touch_only=True, auto_find_on_typing=True, auto_cmd_on_typing=False, vim_mode=False, is_focused=False, show_hidden=False):
        load_theme()
        TUIFIManager._instance_count += 1
        self.__init_variables()

        if has_label:
            height -= 1
            self.labelpad            = WindowPad(win,y+height,0,1,width, (False,anchor[1],anchor[2],anchor[3]))
            self.info_label          = Label(self.labelpad,0, 0, f'{f" {TUIFI_THEME} |" if TUIFI_THEME else ""} TUIFIManager {__version__} | Powered by uni-curses', 1, width, (False,anchor[1],anchor[2],anchor[3]), False, 9)
            self.info_label.style    = unicurses.A_REVERSE | unicurses.A_BOLD
            self.info_label.on_click = self.info_label_clicked
            warnings.showwarning     = self.custom_warning_handler

        super().__init__(win, y, x, height, width, anchor, is_focused)
        self.__order_method      = sort_by
        self.suffixes            = suffixes
        self.draw_files          = draw_files
        self.termux_touch_only   = termux_touch_only
        self.auto_find_on_typing = os.getenv('tuifi_auto_find_on_typing'   , str(auto_find_on_typing)) == 'True' 
        self.auto_cmd_on_typing  = os.getenv('tuifi_auto_command_on_typing', str(auto_cmd_on_typing )) == 'True' 
        self.show_hidden         = os.getenv('tuifi_show_hidden'           , str(    show_hidden    )) == 'True' 
        self.properties          = TUIProps ()
        self.menu                = TUIMenu  (on_choice=self.on_menu_choice ,
            items=(
                'Open       │ ENTER' ,
                'Cut        │ CTRL+X',
                'Copy       │ CTRL+C',
                'Paste      │ CTRL+V',
                'Delete     │ DELETE',
                'Rename     │ CTRL+R',
                'Reload     │ KEY_F5',
                'New File   │ CTRL+W',
                'New Folder │ CTRL+N',
                'Properties │ CTRL+P'),
        )
        self.load_order  ()
        if directory:
            self.directory = os.path.normpath(directory)
            self.load_files(directory, suffixes)
            if draw_files:
                self.draw()

        self.load_markers       ()
        self.load_commands      ()
        self.__set_normal_events()
        if not IS_WINDOWS and stty_a('^Z') : signal.signal(signal.SIGTSTP, self.suspend_proccess)
        if     IS_WINDOWS or  stty_a('^C') : signal.signal(signal.SIGINT , self.copy            ) # https://docs.microsoft.com/en-us/windows/console/ctrl-c-and-ctrl-break-signals
        if os.getenv('tuifi_vim_mode', str(vim_mode)) == 'True'   : self.toggle_vim_mode()
        if IS_DRAG_N_DROP: self.drag_and_drop = SyntheticXDND(self.handle_gui_to_tui_dropped_file, self.__get_selected_files) #NOTE: https://stackoverflow.com/a/14829479/11465149



    def refresh(self):
        if self.info_label: self.labelpad.refresh()
        if not (self.menu.is_focused or self.properties.is_focused):
            super().refresh(clear=False)
        self.menu.refresh()
        self.properties.refresh()


    def custom_warning_handler(self, message, category, filename, lineno, file=None, line=None):
        if "g_main_context_pop_thread_default: assertion" in str(message) :return # SyntheticXDND
        self.info_label.color_pair = 3
        self.info_label.style = unicurses.A_BOLD
        if category.__name__ == SyntaxWarning.__name__:
            self.__set_label_text(f" Please check Issue #111 | {category.__name__}: {message} at {filename}:{lineno}")
        else:
            self.__set_label_text(f" {category.__name__}: {message} at {filename}:{lineno}")
        self.info_label.color_pair = 2
        self.info_label.style = unicurses.A_REVERSE | unicurses.A_BOLD


    def suspend_proccess(self, signum, frame): # Kinda SuS but you know the deal...
        print(END_MOUSE)
        with self.suspend():
            os.kill(os.getpid(), signal.SIGSTOP)
        print(BEGIN_MOUSE)
        unicurses.clear()


    def save_last_state(self, cd=False):
        TUIFIManager._instance_count -= 1
        if TUIFIManager._instance_count == 0:
            if cd or HAS_CD_ON_ESC:
                with open(f'{TEMP_PATH}tuifi_last_path.txt', 'w') as file:
                    file.write(self.directory)
            self.save_markers()
            self.save_order  ()

    def __del__(self):
        self.save_last_state()

    def __handle_garbage(self): self.__del__()


    def __handle_focus_on_previour_dir(self, f, i):
        if self.__is_opening_previous_dir and f.name == self.basename:
            if not IS_TERMUX or not self.termux_touch_only:
                self.__index_of_clicked_file = i
                self.__clicked_file = f
                self.__pre_pressed_file = f # https://github.com/GiorgosXou/TUIFIManager/issues/96
            self.__scroll_to_file(f, not IS_TERMUX or not self.termux_touch_only)
            self.__is_opening_previous_dir = False


    def draw(self):
        unicurses.werase(self.pad)
        #self.refresh()
        if self.maxpLines < self.height:
            self.maxpLines = self.height
        unicurses.wresize(self.pad, self.maxpLines, self.width)
        for i,f in enumerate(self.files):
            f.draw(self.pad)
            self.__handle_focus_on_previour_dir(f,i)


    #def get_TUIFIProfile_by_key(self, key): # https://stackoverflow.com/a/2974082/11465149
        #return next((v for k, v in TUIFIProfiles.items() if (key == k) or (isinstance(k,tuple) and key in k)),FILE_profile)


    def get_profile(self, file_directory, new=False):
        if os.path.isdir(file_directory):
            count = 0
            temp_profile = TUIFIProfiles.get(':empty_folder')
            for suffix in ['/', *self.suffixes] if self.suffixes else ['']: # TODO: Make sure there's no Potential Windows issue? 
                for f in Path(file_directory + sep).glob('*'+suffix): # thankfully is a generator
                    count +=1
                    if count == 2:
                        return TUIFIProfiles.get(':folder')
            if count == 1 : 
                if os.path.isdir(f):
                    return TUIFIProfiles.get(':folder_subfolder')
                else:
                    return TUIFIProfiles.get(':folder_single_file')
        else:
            file_extension = os.path.splitext(file_directory)[1]
            file_extension = f'/{file_extension[1:]}' if file_extension else basename(file_directory)
            temp_profile   = TUIFIProfiles.get(file_extension.lower(),DEFAULT_PROFILE) # ..[-1] = extension
        return temp_profile


    # Let's not remove those yet, just in case
    # __max_h = 0
    # __count = 0
    # ___y    = PADDING_TOP
    # ___x    = PADDING_LEFT

    def __reset_coordinates(self):
        self.__max_h = 0
        self.__count = 0
        self.___y    = PADDING_TOP
        self.___x    = PADDING_LEFT


    def __set_coordinates(self, file, resize=False):
        tempX = (PADDING_LEFT + file.profile.width + PADDING_RIGHT)
        if self.___x > self.width + self.x - tempX + PADDING_RIGHT - self.x :
            self.___x  = PADDING_LEFT
            self.___y += self.__max_h + PADDING_TOP + PADDING_BOTTOM  # ... +1 because the next has to be below :P
            self.__count = 0
            self.__max_h = 0

        file.y = self.___y
        file.x = self.___x
        self.___x  += tempX
        self.__count += 1

        h = file.profile.height + file.name_height #len(f.chunkStr(f.name, f.profile.width).split('\n')) #total hight i might merge them  but nvm for now, i messed the up anyways
        if h > self.__max_h:
            self.__max_h = h
            if not resize: return
            if self.__count != 0:
                self.maxpLines = self.___y + self.__max_h + PADDING_TOP + PADDING_BOTTOM  + self.y
            else:
                self.maxpLines = self.___y + self.y
            if self.maxpLines < self.height:
                self.maxpLines = self.height
            unicurses.wresize(self.pad, self.maxpLines, self.width)


    def __is_valid_file(self, name):
        if not self.show_hidden and name.startswith('.'): return False
        if self.is_in_find_mode or self.__keep_search_results:
            if self.__temp_find_filename.islower():
                return self.__temp_find_filename in name.lower()
            else:
                return self.__temp_find_filename in name
        if self.suffixes and os.path.isfile(self.directory + sep + name):
            for s in self.suffixes:
                if name.endswith(s): return True
            return False
        return True


    def __load_file(self, name):
        is_link      = os.path.islink(self.directory + sep + name)
        filename     = name
        file_        = TUIFile(filename, self.___y, self.___x, self.get_profile(self.directory + sep + name), is_link=is_link)
        self.files.append(file_)
        self.__set_coordinates(file_)


    def load_files(self, directory, suffixes=[]):  # DON'T load and then don't show :P
        directory = os.path.realpath(os.path.normpath(directory))
        if not access(directory, R_OK):
            self.__set_label_text(f'NO READ PERMISSION: "{directory}"')
            return []
        if not os.path.isdir(directory):
            raise FileNotFoundError(f'DirectoryNotFound: "{directory}"')
        if not suffixes:
            suffixes = self.suffixes

        order = self.get_order_of(directory)
        self.is_order_reversed = order[1]
        self.basename = basename(self.directory)
        self.directory = directory
        self.files = []
        self.__reset_coordinates()
        self.__load_file('..')
        os.chdir(directory)
        for f in sorted(os.listdir(), key=order[0], reverse=order[1]): # key=os.path.getctime): # os.listdir(directory):
            if not self.__is_valid_file(f): continue
            self.__load_file(f)

        self.maxpLines = self.___y + self.y if self.__count == 0 else self.___y + self.__max_h + PADDING_TOP + PADDING_BOTTOM + self.y
        return self.files


    def resort(self): #draw_files=True # repeating code but nvm
        """In case of resize, call this function to resort/replace existing files to the new dimensions of pad

        Returns:
            list: self.files
        """
        unicurses.werase(self.pad)

        self.__reset_coordinates()
        for f in self.files:
            self.__set_coordinates(f, resize=True)
            f.draw(self.pad,redraw_icon=True)

        #unicurses.wresize(self.pad, self.maxpLines, self.width) # because it works doesn't also mean that i should do it like that

        #if self.position.iy >= unicurses.getmaxy(self.pad) - self.height + self.y:
            #self.position.iy = unicurses.getmaxy(self.pad) - self.height
        #if self.height + self.position.iy > y:
        #    self.position.iy -= self.height + self.position.iy - y  # NOT SURE AT ALL BUT IT WORKS LOL, actually NOP ):(
        #self.draw()
        #self.select(self.__clicked_file) #  ??????????????
        return self.files


    __keep_search_results = False # really bad practice but whatever lol (and i can't take advantage of is_in_find_mode because of error when moving files that ...)
    def reload(self,draw_files=True, keep_search_results=False):
        if not keep_search_results:
            self.__temp_find_filename = ''
        else:
            self.__keep_search_results = True
        self.position.iy                = 0
        self.__mouse_btn1_pressed_file  = None
        self.__pre_pressed_file         = None
        self.__clicked_file             = None
        self.__index_of_clicked_file    = None
        self.__pre_hov                  = None           
        self.__count_selected           = 0
        self.load_files(self.directory)
        self.__keep_search_results      = False
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


    def __try_open_with(self, directory: str, open_with: Optional[str], multiple=False) -> None:
        if not open_with: return

        dirs = []
        if multiple: # puke-able shit lol xD, sorry for that
            for f in self.files: # TODO: Save selected to a temp list becuase this is really costy! (decisions..) 
                if f.is_selected: 
                    if f.profile.open_with != DEFAULT_OPENER:
                        dirs.append(self.directory+sep+f.name)
                        open_with = DEFAULT_WITH
                    else:
                        self.__try_open_with(self.directory+sep+f.name, f.profile.open_with )
        else:
            dirs = [directory]

        if not dirs: return # Although not needed just in case for other DEFAULT_OPENERs

        print(END_MOUSE, end='\r')
        with self.suspend():
            proc = subprocess.Popen([open_with, *dirs], shell=IS_WINDOWS) # TODO: optional stdout=subprocess.DEVNULL when I'll add loading TUIFIProfiles from external file ?
            proc.wait()
        print(BEGIN_MOUSE, end='\r')
        return


    def __reset_open(self):
        if self.vim_mode and self.escape_event_consumed and not self.is_in_command_mode: # SuS SuS SuS SuS SuS damn that's so Sus lol | 2024-04-05 08:48:24 PM this was for keeping search/find/input mode after opening a folder but i didn't like it and removed it
            self.find()
        else:
            self.is_in_find_mode       = False # else content
            self.escape_event_consumed = False # else content
        self.__change_escape_event_consumed = False
        self.is_in_command_mode      = False
        self.__temp_findname         = ''
        self.__temp_find_filename    = '' # Ahh..
        self.__clicked_file          = None
        self.__pre_pressed_file      = None
        self.__index_of_clicked_file = None
        self.__pre_hov               = None
        self.__count_selected        = 0
        self.position.iy             = 0
        self.__order_method          = None


    __is_opening_previous_dir = False
    def open(self, directory, suffixes=[], _with=None):
        """
        `open()` is `load_files()` + `draw()`
        """
        if directory is None or not directory:
            return None

        if isinstance(directory, TUIFile):
            directory = self.directory + sep + directory.name

        if basename(directory) == '..':
            self.__is_opening_previous_dir = True

        if _with: 
            return self.__try_open_with(directory, _with)

        multiple = self.__count_selected > 1
        if not os.path.isdir(directory) or multiple: # if there is at least one file that it is not a directory OR multiple selected files that they are whatever, then: ... (Now it makes sense why `not isdir`)
            prof = f'/{os.path.splitext(directory)[1][1:]}'
            open_with = TUIFIProfiles.get(prof, DEFAULT_PROFILE).open_with
            return self.__try_open_with(directory, open_with, multiple) # TODO: check if the multiple selected files are folders and open them in new tabs

        if not self.load_files(directory, suffixes): return []
        if not self.is_in_find_mode: self.__set_label_text(f'[{len(self.files)-1:04}]' + (' [▼] ' if self.is_order_reversed else ' [▲] ') + directory ) # just because i know that len is stored as variable,  that's why i don;t count them in for loop
        self.__reset_open()
        self.draw()
        return self.files


    def navigate(self, *args):
        self.__count_selected = 0
        self.open(*args)


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
        if not tuifile:
            if self.__count_selected == 1:
                tuifile = self.__clicked_file
            elif self.__count_selected == 0:
                return
        if not tuifile: # If after above condtion is still not tuifile:
            for f in self.files:
                if f.is_selected:
                    f.is_selected = False
                    f.draw(self.pad)
            self.__count_selected = 0 # i can just -= 1 and break it if 0 :P
        elif tuifile.is_selected:
            tuifile.is_selected = False
            tuifile.draw(self.pad)
            self.__count_selected -=1


    def select(self, tuifile):
        if tuifile.is_selected:return
        self.__count_selected +=1
        #for y in range(tuifile.y, tuifile.y + tuifile.profile.height):
        #    mvwchgat(self.pad,y, tuifile.x, tuifile.profile.width,A_REVERSE,7)
        tuifile.is_selected = True
        tuifile.draw(self.pad)


    def select_all_files(self):
        for f in self.files[1:]:
            self.select(f)
        self.__set_label_text(f'[{self.__count_selected}] Files selected')


    if IS_DRAG_N_DROP:
        headers = { # just in case
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 
            'X-Requested-With': 'XMLHttpRequest'
        } 
        def save(self, path, filename, data):
            try:
                path = os.path.join(path, filename)
                f = open(path, 'wb')
                f.write(data)
                f.close()
                # block from create_new()
                self.__sub_handle_creation_of(filename, self.get_profile(path))
                self.__set_label_text(f'SAVED: "{filename}"')
                return True
            except Exception as e:
                self.__set_label_text(f"FAILED TO SAVE: { str(e) }")
                return False


        def get_available_filename(self,name):
            tmp_name = name
            i = 0
            while os.path.isfile(self.directory + sep + tmp_name):
                tmp_name = f'{i}_{name}'
                i += 1
            return tmp_name



        def download(self, url, out_path): # downloading github images from comments or posts seems to have issues ... those https://private-user-images...
            self.__set_label_text(f'DOWNLOADING: {url}')
            try:
                # self.__set_label_text(f'Downloading file ...')
                r = requests.get(url, headers=self.headers) # , stream=True
                # if r.headers.get('filename'):pass
                filename = ''
                extension = mimetypes.guess_extension(r.headers.get('content-type', '').split(';')[0]) # .split(';') is needed because there might be more after  https://stackoverflow.com/a/59575973/11465149
                content = r.headers.get('Content-Disposition')
                if content and not content.find('filename=') == -1:
                    filename = content.split('filename=')[1].split(';')[0]
                    if filename[0] in ('"', "'"):
                        filename = filename[1:-1]
                    if filename.strip() == '': # This happened with an image dropped from my stackoverflow profile (not the small ones)
                        filename = 'download'
                    if extension and filename.find('.') == -1: # hidden filenames without extension might be an issue\get-ignored :P
                        filename = filename + extension
                else:
                    filename = basename(url).split("?")[0].split(".",1)
                    if extension:
                        filename = filename[0] + extension
                    elif len(filename)>1:
                        filename = filename[0] + "." + filename[1]
                    else:
                        filename = "download"

                #TODO: if duplicate display a msg replace or something | or if duplicate check hashes and if the same ignore else ask?
                filename = self.get_available_filename(filename)

                return self.save(out_path, filename, r.content)
            except Exception as e:
                self.__set_label_text(f"FAILD TO DOWNLOAD: { str(e) }")
                return False



        def __get_selected_files(self): # I know it's not optimized at all, but ... anyways for now... I have a life too :P
            if self.__count_selected > 1: # don't simplify the condition cause it doesn't count __pre_pressed_file as selected until it becomes clicked (if i remember well pre_clicked means pressed but not released)
                f_list = []
                for f in self.files:
                    if f.is_selected:
                        f_list.append(QUrl.fromLocalFile(self.directory + sep + f.name))
                return f_list
            elif self.__pre_pressed_file:
                return [QUrl.fromLocalFile(self.directory + sep + self.__pre_pressed_file.name)]


        def handle_gui_to_tui_dropped_file(self, file_url, type): #TODO: Custom user actions on link patterns: eg. clone git, save at folder xy, etc. + TODO: if dropped on folder
            self.is_focused = False
            self.__set_label_text(f'DROPPED: {file_url}')
            if type == 1:
                name = os.path.basename(file_url)
                shutil.move(file_url, self.directory + sep + name)
                self.__sub_handle_creation_of(name, self.get_profile(file_url)) # TODO: for other non \file_extensions
                self.__set_label_text(f'MOVED: {name}')
                self.refresh() #for some reason refresh is needed that's SuS. Should look on download too
            elif type == 0:
                self.download(file_url, self.directory + sep)
            elif file_url.startswith('data:') and not file_url.find('base64') == -1:
                extension = mimetypes.guess_extension(file_url.split(';')[0].split(':')[1])
                filename = self.get_available_filename('download'+extension)
                self.save(self.directory, filename, base64.b64decode(file_url[file_url.find('4')+1:])) # 4 is from base64
            else:
                self.__set_label_text(f'DROPPED UNHANDLED: {file_url}')
            self.is_focused = True
                # r = requests.get(file_url) # , stream=True
                # r.headers.get('filename')
                # unicurses.mvwaddwstr(self.pad,0,0,f'is downloadable: {r.headers}')

                # from urllib.request import urlopen 
                # response = urlopen(file_url)
                # filename = response.headers.get_filename()
                # self.__set_label_text(f'{filename} <-----')
                



    def scroll_pad(self, y):
        if self.position.iy <= 0 and y < 0:
            self.position.iy = 0
            return
        if self.position.iy >= unicurses.getmaxy(self.pad) - self.height  and y > 0:
            self.position.iy = unicurses.getmaxy(self.pad) - self.height
            return
        self.position.iy += y


    def exit_to_self_directory(self):
        print(END_MOUSE)
        unicurses.endwin()
        self.save_last_state(cd=True) # it's self.__handle_garbage() but eew!
        exit()


    def load_order(self, path=CONFIG_PATH):
        path = path + sep + 'ORDER.csv'
        if not os.path.isfile(path) : return
        tmp_order_methods = {
            'getctime' : os.path.getctime,
            'getsize ' : os.path.getsize ,
            'getatime' : os.path.getatime,
            'getmtime' : os.path.getmtime,
            'none'     : None
        }
        with open(path, 'r') as file:
            for d in file:
                d = d.split(',')
                TUIFIManager.ordered_dirs[d[0]] = (tmp_order_methods[d[1]], True if d[2][:-1] == 'True' else False) # -1 to remove newline


    def save_order(self, path=CONFIG_PATH):
        if not TUIFIManager.__ordered_dirs_need_saving: return # prevent unnecessary saving
        with open(path + sep + 'ORDER.csv','w') as fp:
            for k, v in TUIFIManager.ordered_dirs.items():
                if os.path.isdir(k):
                    fp.write(k + ',' + (v[0].__name__ if v[0] else 'none') + f',{v[1]}\n')


    def get_order_of(self, directory):
        tmp_ordered_dir = TUIFIManager.ordered_dirs.get(directory)
        return (None, False) if not tmp_ordered_dir else tmp_ordered_dir


    is_order_reversed = False
    def ascend_order_switch(self, order_method=None):
        if not self.is_order_reversed: order_method = self.__order_method
        self.is_order_reversed = True
        self.switch_order_method(order_method)


    def descend_order_switch(self, order_method=None):
        if self.is_order_reversed: order_method = self.__order_method
        self.is_order_reversed = False
        self.switch_order_method(order_method)


    __ordered_dirs_need_saving = False
    ordered_dirs = {}
    def switch_order_method(self, order_method=None):
        TUIFIManager.__ordered_dirs_need_saving = True
        if order_method: 
            self.__order_method = order_method
            self.__set_label_text(('[▼] DESCENDING' if self.is_order_reversed else '[▲] ASCENDING') + ' ORDER')
        elif self.__order_method == None:
            self.__order_method = os.path.getctime
            self.__set_label_text(('[▼]' if self.is_order_reversed else '[▲]') + '[ORDERED] BY CHANGE TIME')
        elif self.__order_method == os.path.getctime: 
            self.__order_method = os.path.getsize 
            self.__set_label_text(('[▼]' if self.is_order_reversed else '[▲]') + '[ORDERED] BY SIZE')
        elif self.__order_method == os.path.getsize:
            self.__order_method = os.path.getatime
            self.__set_label_text(('[▼]' if self.is_order_reversed else '[▲]') + '[ORDERED] BY ACCESS TIME')
        elif self.__order_method == os.path.getatime:
            self.__order_method = os.path.getmtime
            self.__set_label_text(('[▼]' if self.is_order_reversed else '[▲]') + '[ORDERED] BY MODIFICATION TIME')
        else:
            self.__order_method = None # oreder default
            self.__set_label_text(('[▼]' if self.is_order_reversed else '[▲]') + '[ORDERED] BY NAME')

        if not self.is_order_reversed and self.__order_method == None: # prevent default mode to be saved 
            if TUIFIManager.ordered_dirs.get(self.directory): del TUIFIManager.ordered_dirs[self.directory]
        else:
            TUIFIManager.ordered_dirs[self.directory] = (self.__order_method, self.is_order_reversed)

        self.reload()


    def __init_event_variables_and_mouse(self):
        self.is_on_select_mode          = False
        self.__mouse_btn1_pressed_file  = None
        self.__pre_pressed_file         = None
        self.__pre_clicked_file         = None
        self.__clicked_file             = None
        self.__index_of_clicked_file    = None
        self.__start_time               = 0
        self.events = {}
        # hover variables
        self.__x = self.__y  = 0     # previous position
        self.hover_mode = False
        self.__pre_hov  = None # TODO: clear the value when directory change at open

        self.__index_of_alt_clicked_file     = None
        self.__index_of_pressed_file         = None


    __temp__copied_files       = []
    __temp_dir_of_copied_files = ''


    def __set_normal_events(self):
        self.events = {
            unicurses.KEY_UP        : self.__perform_key_up             ,
            unicurses.KEY_DOWN      : self.__perform_key_down           ,
            unicurses.KEY_LEFT      : self.__perform_key_left           ,
            unicurses.KEY_RIGHT     : self.__perform_key_right          ,
            unicurses.KEY_BTAB      : self.__perform_key_btab           ,
            unicurses.KEY_DC        : self.delete                       ,
            unicurses.KEY_F(5)      : self.reload                       ,
            unicurses.KEY_F(3)      : self.descend_order_switch         ,
            unicurses.KEY_F(1)      : self.ascend_order_switch          ,
            unicurses.CTRL('A')     : self.select_all_files             ,
            unicurses.CTRL('T')     : self.toggle_hidden_files          ,
            unicurses.CTRL('R')     : self.rename                       ,
            unicurses.CTRL('C')     : self.copy                         ,
            unicurses.CTRL('K')     : self.copy                         ,
            unicurses.CTRL('X')     : self.cut                          ,
            unicurses.CTRL('V')     : self.paste                        ,
            unicurses.CTRL('W')     : partial(self.create_new, 'file'  ),
            unicurses.CTRL('N')     : partial(self.create_new, 'folder'),
            unicurses.CTRL('F')     : self.find                         ,
            unicurses.CTRL('O')     : self.__open_DEFAULT_WITH          , # https://stackoverflow.com/a/33966657/11465149
            unicurses.CTRL('E')     : self.exit_to_self_directory       ,
            unicurses.CTRL('P')     : self.view_selected_file_properties,
            unicurses.KEY_HOME      : partial(self.navigate, HOME_DIR)  ,
            unicurses.KEY_ENTER     : self.__perform_key_enter          ,
            10                      : self.__perform_key_enter          ,
            unicurses.KEY_BACKSPACE : self.__navigate_to_previous_dir   ,
            8                       : self.__navigate_to_previous_dir   , # https://superuser.com/questions/212874/why-is-backspace-often-represented-with-h | TODO: I might remove it
            127                     : self.__navigate_to_previous_dir   ,
            263                     : self.__navigate_to_previous_dir   ,
            unicurses.KEY_RESIZE    : self.__handle_resize_event        ,
            32                      : self.command                      , # SPACEBAR
            27                      : self.__handle_garbage             , #NOTE: https://stackoverflow.com/a/14829479/11465149
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
                unicurses.CCHAR('o') : self.descend_order_switch         ,
                unicurses.CCHAR('O') : self.ascend_order_switch          ,
                unicurses.CCHAR('K') : self.__perform_key_enter          ,
                unicurses.CCHAR('J') : self.__navigate_to_previous_dir   ,
                unicurses.CCHAR('b') : self.__navigate_to_previous_dir   ,
                unicurses.CCHAR('H') : partial(self.navigate  , HOME_DIR),
                unicurses.CCHAR('w') : partial(self.create_new, 'file'  ),
                unicurses.CCHAR('W') : partial(self.create_new, 'folder'),
                unicurses.CCHAR('i') : self.find                         ,
                unicurses.CCHAR('R') : self.reload                       ,
                unicurses.CCHAR('e') : self.exit_to_self_directory       ,
                unicurses.CTRL ('D') : self.delete                       ,
            }) # TODO Map  events


    def toggle_hidden_files(self):
        self.show_hidden = not self.show_hidden
        self.reload()


    def __set_label_text(self, text):
        if self.info_label:
            self.info_label._text = text


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


    def __scroll_to_file(self, tuifile, select=False, deselect=False):
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


    def has_write_access(self, path):
        if not access(path, W_OK):
            self.__set_label_text('[ERROR] NO WRITE PERMISSION')
            return False
        return True


    __is_cut = False
    def cut(self):
        """
        Cut-copies the selected files | Not fully implemented yet
        """
        if not self.has_write_access(self.directory): return
        self.__is_cut = True  # TODO: DON'T FORGET TO CHANGE TERMUX CUT WHEN NEW VERSION[...]
        self.__stack_files_for_action()


    def copy(self, signum=None, frame=None):
        """
        Copies the selected files (ignore signum=None, frame=None [...]) | Not fully implemented yet
        """
        self.__is_cut = False
        self.__stack_files_for_action()


    def __set_label_on_copy(self,size):
        length = len(TUIFIManager.__temp__copied_files)
        text   = f'{length} files [~{convert_bytes(size)}]' if length > 1 else f'{TUIFIManager.__temp__copied_files[0].name}'
        action = 'CUTED' if self.__is_cut else 'COPIED'
        self.__set_label_text(f'[{action}]: {text}')


    def __stack_files_for_action(self):
        """
        this function is TEMPORARY and will be REMOVED,
        it will be present until i find a way of drawing/managing cutted files efficiently
        """
        if self.__count_selected == 0 or (self.__clicked_file and self.__clicked_file.name == '..') : return
        size = 0
        TUIFIManager.__temp_dir_of_copied_files = self.directory
        if self.__count_selected == 1:
            TUIFIManager.__temp__copied_files = [self.__clicked_file]
        else:
            TUIFIManager.__temp__copied_files = []
            for f in self.files:
                if f.is_selected:
                    TUIFIManager.__temp__copied_files.append(f)
                    size += os.path.getsize(self.directory + sep + f.name)
        self.__set_label_on_copy(size)


    def __duplicate(self):
        for f in TUIFIManager.__temp__copied_files:
            source      = TUIFIManager.__temp_dir_of_copied_files + sep + f.name
            destination = self.directory + sep
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
        for f in TUIFIManager.__temp__copied_files:
            source      = TUIFIManager.__temp_dir_of_copied_files + sep + f.name
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
        if not self.has_write_access(self.directory): return
        if len(TUIFIManager.__temp__copied_files) == 0 or not os.path.exists(TUIFIManager.__temp_dir_of_copied_files): return # u never no if the user deleted anything from other file manager this is also something i haven't consider for the rest of the things and [...]
        if TUIFIManager.__temp_dir_of_copied_files != self.directory: self.__copy_cut ()
        else                                                : self.__duplicate()
        self.reload(keep_search_results=True)


    def resort_reset_select(self, i):
        self.resort() # replaced -> self.reload(keep_search_results=True)
        self.__index_of_clicked_file = i
        self.__clicked_file          = self.files[i]
        self.__pre_pressed_file      = self.files[i]
        self.__pre_hov               = None           
        self.select(self.__clicked_file)


    def __delete_selected_file(self):
        # checking under __delete_file too but nvm cause i have no time right now
        if self.__clicked_file.name == '..': return 0
        self.__delete_file(self.__clicked_file)
        del self.files[self.__index_of_clicked_file]
        self.__set_label_text(f'[DELETED] "{self.__clicked_file.name}"')
        return self.__index_of_clicked_file - 1


    def __delete_multiple_selected_file(self):
        i=0
        tmp_count = self.__count_selected
        while True:
            if self.files[i].is_selected: # first file is never selected because it is the .. one
                self.__delete_file(self.files[i])
                del self.files[i]
                i-=1
                if self.__count_selected == 0:
                    break
            i+=1
        self.__set_label_text(f'[DELETED] {tmp_count} FILES')
        return i


    def delete(self):
        """
        Deletes the selected file(s). | Not fully implemented yet
        """
        if not self.has_write_access(self.directory): return
        if self.__count_selected == 1 and self.__clicked_file :
            fi = self.__delete_selected_file()
        elif self.__count_selected > 1:  # Why do i even > 1 very sus | 2024-07-10 Update: I do so because people might delete without any selection!
            fi = self.__delete_multiple_selected_file()
        else:
            self.__set_label_text(' NO FILE SELECTED TO DELETE')
            return
        self.resort_reset_select(fi)


    def load_markers(self, path=CONFIG_PATH):
        path = path + sep + 'MARKERS'
        if not os.path.isfile(path) : return
        with open(path, 'r') as file:
            TUIFIManager.markers = json.load(file)


    def save_markers(self, path=CONFIG_PATH):
        TUIFIManager.markers['`'] = self.directory
        with open(path + sep + 'MARKERS','w') as fp:
            fp.write(json.dumps(TUIFIManager.markers))


    def __mark_file_as_currently_clicked(self, i):
        self.__index_of_clicked_file   = i
        self.__clicked_file            = self.files[i]
        self.__mouse_btn1_pressed_file = self.__clicked_file
        self.__pre_pressed_file        = self.__clicked_file


    def clear_find_results(self):
        self.is_in_find_mode                = False
        self.__change_escape_event_consumed = True
        self.__temp_findname                = ''
        self.__clicked_file                 = self.files[0] # https://github.com/GiorgosXou/TUIFIManager/issues/25
        self.__index_of_clicked_file        = 0
        self.__set_label_text('[NORMAL]')
        self.load_files(self.directory)
        self.draw() # i might want to __scroll_to_file after that here too? or nah..


    def __init_variables_for_find_mode(self):
        self.__arrow_keys         = (unicurses.KEY_LEFT, unicurses.KEY_RIGHT, unicurses.KEY_DOWN, unicurses.KEY_UP)
        self.is_in_find_mode      = False
        self.__temp_findname      = ''
        self.__temp_find_filename = ''


    def handle_find_events(self,event): # TODO: FIX SUFFIXES WHEN DELETING, find_file
        if event == 27:
            if self.vim_mode:
                self.__change_escape_event_consumed = True
                self.is_in_find_mode                = False
                if self.__temp_findname != '': # When Escaping without searching anything
                    if len(self.files) == 1:  # if nothing is found (only folder ".." then reload at cancel)
                        self.reload()
                        self.__set_label_text('[NORMAL]')
                        return False
                    self.__index_of_clicked_file = 1
                    self.__clicked_file          = self.files[1]
                if not len(self.files) == 1 and not self.__clicked_file: # meaning at least 2 files exist and we haven't navigated to the previous folder while on search mode
                    self.__mark_file_as_currently_clicked(1)
                    self.select(self.__clicked_file)
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
        elif event in self.__arrow_keys or unicurses.CTRL(event) == event or event in (10, unicurses.KEY_ENTER): # unicurses.CTRL(event) seems to capture KEY_ENTER but just in case i'll include KEY_ENTER too...
            i = 0 if len(self.files) == 1 else 1
            self.__change_escape_event_consumed = True
            self.is_in_find_mode                = False
            if not self.__clicked_file: # meaning if enter was pressed and something opened then don't __mark_file_as_currently_clicked because it was handled by another method (eg. when navigating to the previous folder)
                self.__mark_file_as_currently_clicked(i) # I need to surppress when ".."
                self.select(self.__clicked_file)
            return False
        elif event == unicurses.KEY_MOUSE:
            return False # but handle this case at handle_mouse_events > above self.open(self.__clicked_file)
        elif event in (unicurses.KEY_RESIZE,unicurses.KEY_HOME , unicurses.KEY_DC) or unicurses.keyname(event) in ('kxOUT','kxIN'): # Ignore this shit :P
            return False
        else:
            self.__temp_findname += unicurses.RCCHAR(event)

        self.__pre_hov = None
        self.find_file(self.__temp_findname)
        self.__set_label_text(f'SEARCH: {self.__temp_findname}')
        i = 0 if len(self.files) == 1 else 1
        self.__mark_file_as_currently_clicked(i)

        self.__scroll_to_file(self.__clicked_file, True, True)
        return True


    def find_file(self, filename): # meh, slightly computationally expensive but easier to implement, whatever at least it does it's job lol
        self.__count_selected = 0
        self.__temp_find_filename = filename
        self.load_files(self.directory)
        self.draw()


    def find(self):
        self.__set_label_text('[INPUT]')
        self.is_in_find_mode = True
        self.escape_event_consumed = True
        self.__temp_findname = '' # just to make sure although it might not be need it


    def __refine_path(self, path):
        path = HOME_DIR       + path[1:] if path.startswith('~') else path
        path = self.directory + path[1:] if path.startswith('.') else path 
        path = os.path.realpath(os.path.normpath(path))
        return path


    def __cmd_open(self, **args):
        if args['directory']: 
            args['directory'] = self.__refine_path(args['directory'] )
            if os.path.isdir(args['directory']): self.__count_selected = 0
        else:
            args['directory'] = self.__clicked_file
        self.open(**args)


    def __cmd_stack(self, pattern):
        TUIFIManager.__temp__copied_files = []
        size = 0
        if pattern:
            for e in self.files:
                match = re.search(pattern, e.name)
                if match:
                    TUIFIManager.__temp__copied_files.append(e)
                    size += os.path.getsize(self.directory + sep + e.name)
        elif self.__clicked_file:
            size = os.path.getsize(self.directory + sep + self.__clicked_file.name)
            TUIFIManager.__temp__copied_files = [self.__clicked_file]
        if len(TUIFIManager.__temp__copied_files): 
            TUIFIManager.__temp_dir_of_copied_files = self.directory
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
    command_types  = { # TODO: maybe an open with sufixes?
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
                "yat | copy | 'pattern':'.+\\\\.txt'          |\n"               +
                "yy  | copy | 'pattern':None                |\n" 
            )
            f.close()
        f = open(conf_path, 'r')
        for line in f:
            ln = line.strip()
            if ln == '': continue
            ln = line.split('|') #  command, args, type, comment | using "|" because this is an __illegal_filename_characters
            TUIFIManager.command_events[ln[0].strip()] = (self.command_types[ln[1].strip()], ast.literal_eval('{'+ln[2].strip()+'}'), ln[3].strip())
        f.close()


    def __execute_cmd(self, cmd):
        return subprocess.Popen(cmd.split(), shell=IS_WINDOWS, stdout=subprocess.PIPE)[0]


    def __ignore_escape(self): self.consume_escape_once()

    markers = {}
    def __perform_hardcoded_cmd_events(self, event):
        character = unicurses.RCCHAR(event)
        if self.__temp_findname.startswith('y'):
            if len(self.__temp_findname) == 2:
                if   character == 'p': 
                    self.__set_label_text('[COPIED] File-path to clipboard'      if clipboard(str(self.directory+sep+self.__clicked_file.name if self.__clicked_file else self.directory)) else 'FAILD TO COPY TO CLIPBOARD')
                    self.__temp_findname = '' # to prevent blocking command mode I include those 2 lines 2 times, once here ...
                    self.__ignore_escape()
                elif character == 'd': 
                    self.__set_label_text('[COPIED] Directory-path to clipboard' if clipboard(str(self.directory)) else 'FAILD TO COPY TO CLIPBOARD')
                    self.__temp_findname = '' # ... and once here
                    self.__ignore_escape()
            return False
        if self.__temp_findname.startswith('f'):
            if len(self.__temp_findname) == 2:
                at = self.__index_of_clicked_file + 1 if self.__index_of_clicked_file else 0
                for i, tfl in enumerate(self.files[at:], start=at):
                    if tfl.name[0] in (character, character.upper()):
                        self.__scroll_to_file(self.files[i], True, True)
                        self.__mark_file_as_currently_clicked(i)
                        self.__set_label_on_file_selection(i,tfl)
                        self.__ignore_escape()
                        return False
                self.__set_label_text(f' Nothing was found forwards, starting with "{character}"')
                self.__ignore_escape()
            return False
        if self.__temp_findname.startswith('F'):
            if len(self.__temp_findname) == 2:
                at = self.__index_of_clicked_file if self.__index_of_clicked_file else 0
                for i, tfl in enumerate(reversed(self.files[:at])):
                    if tfl.name[0] in (character, character.upper()):
                        i = at-i-1
                        self.__scroll_to_file(self.files[i], True, True)
                        self.__mark_file_as_currently_clicked(i)
                        self.__set_label_on_file_selection(i,self.__clicked_file)
                        self.__ignore_escape()
                        return False
                self.__set_label_text(f' Nothing was found backwards, starting with "{character}"')
                self.__ignore_escape()
            return False
        if self.__temp_findname.startswith('m'):
            self.__set_label_text('[MARKER]')
            if len(self.__temp_findname) == 2:
                self.__set_label_text(f'[MARKER] SET TO [{character}]')
                TUIFIManager.markers[character] = self.directory
                self.__temp_findname = ''
                self.__ignore_escape()
            return True
        elif self.__temp_findname.startswith(('`',';')):
            self.__set_label_text('[GOTO MARKER]')
            if len(self.__temp_findname) == 2:
                path = TUIFIManager.markers.get(character)
                if path:
                    self.deselect()
                    self.open(path) # scroll to file maby too?
                else: 
                    self.__set_label_text('[MARKER] NOT FOUND')
                    self.__ignore_escape()
            return True
        # elif Z_EXISTS and self.__temp_findname.startswith('z'): # TODO: I've wanted to call z command but it says something about permissions and stopped trying
            
        return False


    def call_command(self,command):
        cmd = TUIFIManager.command_events.get(command)
        if not cmd: return False
        self.__change_escape_event_consumed = True # it has to be before cmd call
        cmd[0](self, **cmd[1])
        self.__temp_findname    = ''
        self.is_in_command_mode = False
        if cmd[2]: self.__set_label_text(cmd[2])
        return True


    def handle_command_events(self, event):
        self.__set_label_text('[COMMAND]')
        if event == 27:
            self.__change_escape_event_consumed = True
            self.is_in_command_mode = False
            self.__temp_findname    = ''
            self.__set_label_text('[NORMAL]')
        elif event in (unicurses.KEY_MOUSE, unicurses.KEY_RESIZE) or unicurses.keyname(event) in ('kxOUT','kxIN'):
            return False
        else:
            self.__temp_findname += unicurses.RCCHAR(event)
            self.__set_label_text(f'[COMMAND] {self.__temp_findname}')
        if self.__perform_hardcoded_cmd_events(event): return True
        self.call_command(self.__temp_findname)
        return True


    def command(self):
        self.__set_label_text('[COMMAND]')
        self.is_in_command_mode    = True
        self.escape_event_consumed = True
        self.__temp_findname = '' # just ot make sure although it might not be need it


    def rename(self):
        if self.__clicked_file and not self.__clicked_file == self.files[0]:
            self.__set_label_text(f'[RENAMING] {self.__clicked_file.name}')
            self.escape_event_consumed = True
            self.__clicked_file.draw_name(self.pad, self.__clicked_file.name, '', 0, unicurses.A_UNDERLINE)  # Yeah ok, whatever
            self.__temp_name        = self.__clicked_file.name
            self.__temp_pre_name    = self.__temp_name
            self.__first_pass       = True


    def __init_varibles_for_rename(self):
        self.escape_event_consumed          = False
        self.__first_pass                   = True
        self.__change_escape_event_consumed = False  # on second loop
        self.__temp_pre_name                = ''
        self.__temp_name                    = ''
        self.__temp_i                       = 0


    __illegal_filename_characters  = ('<', '>', ':',  '/', '\\', '|', '?', '*', '"')
    def handle_rename_events(self, event):  # At this momment i don't even care about optimizing anything... just kidding, you get the point, no free time | TODO: change event == ... to self.events.get(...)
        if event == unicurses.KEY_LEFT:
            if self.__temp_i != 0: self.__temp_i -= 1
        elif event == unicurses.KEY_RIGHT:
            if self.__temp_i != len(self.__temp_name): self.__temp_i += 1
        elif event in (27, unicurses.KEY_ENTER, 10) or (event == unicurses.KEY_MOUSE and (self.get_mouse()[5] & unicurses.BUTTON1_PRESSED)) : # TODO: clicks to act as enter
            new_path_name                       = self.directory + sep + self.__temp_name
            self.__temp_i                       = 0
            self.__change_escape_event_consumed = True
            if  event != 27 and self.__temp_name.strip() != '' and not os.path.exists(new_path_name):
                os.rename(self.directory + sep + self.__clicked_file.name, new_path_name)
                self.__set_label_text(f'RENAMED: "{self.__clicked_file.name}" to "{self.__temp_name}"')
                self.__clicked_file.name    = self.__temp_name
                self.__clicked_file.profile = self.get_profile(new_path_name)
                self.resort()
                self.__scroll_to_file(self.__clicked_file, True, True)
            else:
                self.__temp_name = self.__clicked_file.name
        elif unicurses.RCCHAR(event) in TUIFIManager.__illegal_filename_characters or event == unicurses.KEY_MOUSE or unicurses.keyname(event) in ('kxOUT','kxIN'):
            return
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
        self.__clicked_file.draw_name(self.pad,self.__temp_name,self.__temp_pre_name, self.__temp_i)
        self.__temp_pre_name = self.__temp_name
        self.__first_pass    = False
        #if event in (unicurses.KEY_BACKSPACE, 8, 127, 263):
        #    pass


    def __sub_handle_creation_of(self, filename, profile):
        self.deselect()
        self.__clicked_file = TUIFile(filename, profile=profile)
        self.__pre_pressed_file = self.__clicked_file # https://github.com/GiorgosXou/TUIFIManager/issues/98
        self.__index_of_clicked_file = self.__index_of_clicked_file if self.__index_of_clicked_file else 1
        self.files.insert(self.__index_of_clicked_file, self.__clicked_file) # condition added because if self.__index_of_clicked_file is None and create a file it fails
        self.resort()
        self.__scroll_to_file(self.__clicked_file,True) # removed deselect=True thanks to `self.__index_of_clicked_file =...` but just in case I let this here


    def create_new(self,_type='folder'): # temporary implementation but nvm
        if not self.has_write_access(self.directory): return
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

        self.__sub_handle_creation_of(filename, TUIFIProfiles.get(f':{_type}'))
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
        info = f'[{convert_bytes(os.path.getsize(path))}]' if os.path.isfile(path) else ''
        offset = self.__int_len(max(len(self.files),999)) + 3 + self.__int_len(index) + 3 + len(info) + 2
        self.info_label.text = f'[{len(self.files) - 1:04}] [{index}] {path[max(len(path) - self.info_label.width + offset, 0):]} {info}'
        # just because i know that len is stored as variable,  that's why i don;t count them in for loop


    def view_selected_file_properties(self):
        if self.__count_selected == 1:
            self.properties.create_tui_for([self.__clicked_file], self.directory)
        elif self.__count_selected > 1:
            self.properties.create_tui_for(self.files, self.directory)

    def __open_clicked_file(self):
        self.open(self.__clicked_file)


    __menu_select_actions = (
        __open_clicked_file           ,
        cut                           ,
        copy                          ,
        paste                         ,
        delete                        ,
        rename                        ,
        reload                        ,
        create_new_file               ,
        create_new_folder             ,
        view_selected_file_properties # lambda *args : None
    )
    def on_menu_choice(self, action):
        TUIFIManager.__menu_select_actions[action](self)


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


    def __handle_hover_mode(self, y, x):
        if not self.hover_mode: return
        tmp_id_of_hov_file, tmp_hov_file = self.get_tuifile_by_coordinates(y,x, return_enumerator=True)
        if tmp_hov_file and tmp_id_of_hov_file and not tmp_hov_file.is_selected: 
            self.__set_label_on_file_selection(tmp_id_of_hov_file,tmp_hov_file)
            # tmp_hov_file.is_selected = True
            tmp_hov_file.draw_effect(self.pad, effect=0)
            if self.__pre_hov and self.__pre_hov != tmp_hov_file:
                # self.__pre_hov.is_selected = False
                self.__pre_hov.draw(self.pad)
            self.__pre_hov = tmp_hov_file
        elif self.__pre_hov:
            self.__pre_hov.draw(self.pad)
            self.__pre_hov = None



    def __handle_mouse_events(self, event): # I know it's a messy code ... lol
        if event != unicurses.KEY_MOUSE: return False
        in_range, id, x, y, z, bstate = self.get_mouse()
        if not IS_WINDOWS and not in_range: return True # TODO: https://github.com/GiorgosXou/TUIFIManager/issues/49
        if self.__x != x or self.__y != y: self.hover_mode = True #hover mode

        if   not self.hover_mode and (bstate & unicurses.BUTTON4_PRESSED): self.scroll_pad(UP   if not bstate & unicurses.BUTTON_CTRL else CTRL_UP  )
        elif not self.hover_mode and (bstate & unicurses.BUTTON5_PRESSED): self.scroll_pad(DOWN if not bstate & unicurses.BUTTON_CTRL else CTRL_DOWN)
        elif not IS_TERMUX or not self.termux_touch_only: # because there are some times that long like presses might be translated to BUTTON1_PRESSED instead of CLICK
            self.__handle_hover_mode(y,x)
            if (bstate & unicurses.BUTTON1_RELEASED) or (bstate & unicurses.BUTTON3_RELEASED) or (unicurses.OPERATING_SYSTEM == 'Windows' and bstate & unicurses.BUTTON1_DOUBLE_CLICKED): # unicurses.OPERATING_SYSTEM == 'Windows' because issues with ncurses
                if self.hover_mode: return True
                self.__index_of_clicked_file, self.__clicked_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)
                self.__delay1 = time() - self.__delay1
                sumed_time    = time() - self.__start_time - self.__delay1 # yeah whatever
                if self.__clicked_file: self.__set_label_on_file_selection() # Hell, pain on my eyes, lol

                if self.__count_selected == 1: # for BUTTON_ALT\BUTTON_SHIFT selection
                    self.__index_of_alt_clicked_file = self.__index_of_clicked_file
                elif self.__clicked_file and not self.__clicked_file.name == '..':
                    self.__set_label_text(f'[{self.__count_selected}] Files selected')

                if self.__mouse_btn1_pressed_file == self.__clicked_file and not (bstate & unicurses.BUTTON_CTRL or bstate & unicurses.BUTTON_ALT or bstate & unicurses.BUTTON_SHIFT):
                    if not ((bstate & unicurses.BUTTON3_RELEASED) and self.__count_selected > 1 and self.__clicked_file and self.__clicked_file.is_selected):
                        self.menu.delete()
                        self.deselect()
                    if bstate & unicurses.BUTTON3_RELEASED:
                        self.menu.create(y,x)
                    if self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file.name == '..' and not self.__mouse_btn1_pressed_file.is_selected :
                        self.select(self.__mouse_btn1_pressed_file )
                    if (((HAS_SINGLE_CLICK or (sumed_time < self.double_click_DELAY)) and (bstate & unicurses.BUTTON1_RELEASED) and (HAS_SINGLE_CLICK or (self.__pre_clicked_file == self.__clicked_file) )) or bstate & unicurses.BUTTON1_DOUBLE_CLICKED) and self.__clicked_file: #and count == 2  :
                        self.is_in_find_mode       = False # due to __is_valid_file 
                        self.escape_event_consumed = False
                        self.open(self.__clicked_file)
                elif self.__clicked_file and self.__mouse_btn1_pressed_file and not self.__mouse_btn1_pressed_file == self.__clicked_file and not self.__clicked_file.is_selected: # this `and not self.__clicked_file.is_selected:` was needed because __clicked_file isn't marked as selected until "drop event" ends | tldr prevents from dropping files into itself
                    if os.path.isdir(self.directory + sep + self.__clicked_file.name) and self.has_write_access(self.directory) and self.has_write_access(self.directory + sep + self.__clicked_file.name):
                        i=0 # taken from __delete_multiple_selected_file
                        folder_index = None
                        while True:
                            if self.files[i].is_selected: # first file is never selected because it is the .. one
                                fname = self.files[i].name
                                shutil.move(self.directory + sep + fname, self.directory + sep + self.__clicked_file.name + sep + fname)
                                self.__count_selected -=1
                                del self.files[i]
                                i-=1
                                if self.__count_selected == 0 and not folder_index == None:
                                    break
                            elif self.files[i] == self.__clicked_file:
                                folder_index = i
                                if self.__count_selected == 0:
                                    break
                            i+=1
                        self.resort_reset_select(folder_index)

                self.__pre_clicked_file = self.__clicked_file
                self.__start_time = time()
            elif (bstate & unicurses.BUTTON1_PRESSED) or (bstate & unicurses.BUTTON3_PRESSED):
                self.__delay1 = time()
                self.__index_of_pressed_file, self.__mouse_btn1_pressed_file = self.get_tuifile_by_coordinates(y, x, return_enumerator=True)

                if not bstate & unicurses.BUTTON_CTRL and self.__pre_pressed_file and self.__pre_pressed_file.is_selected:#and summ > self.double_click_DELAY:
                    if self.__count_selected == 1:
                        self.deselect(self.__pre_pressed_file)
                        self.menu.delete()
                if bstate & unicurses.BUTTON_ALT or bstate & unicurses.BUTTON_SHIFT: 
                        self.deselect()

                if self.__mouse_btn1_pressed_file and self.__mouse_btn1_pressed_file.name != '..':
                    if not self.__mouse_btn1_pressed_file.is_selected and not (bstate & unicurses.BUTTON3_PRESSED):
                        if (bstate & unicurses.BUTTON_ALT or bstate & unicurses.BUTTON_SHIFT) and self.__index_of_alt_clicked_file:
                            start = min(self.__index_of_alt_clicked_file, self.__index_of_pressed_file)
                            end   = max(self.__index_of_alt_clicked_file, self.__index_of_pressed_file)
                            for f in self.files[start:end+1]: # __index_of_alt_clicked_file acts as the index of the pre-clicked file | that "+1" it's so weird....
                                self.select(f)
                            # self.select(self.files[end])
                        self.select(self.__mouse_btn1_pressed_file)
                    elif bstate & unicurses.BUTTON_CTRL :#and summ > self.double_click_DELAY:
                        self.deselect(self.__mouse_btn1_pressed_file)

                self.__pre_pressed_file = self.__mouse_btn1_pressed_file
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
        unicurses.touchwin(self.parent.win)


    def consume_escape_once(self):
        self.__change_escape_event_consumed = True # not sure if this line is necessary.. surely not for __perform_hardcoded_cmd_events
        self.escape_event_consumed = True
        self.is_in_command_mode = False

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


    def __navigate_to_previous_dir(self):
        self.navigate(self.directory + sep + '..')


    def __open_DEFAULT_WITH(self): # opens folder 
        self.open(self.__clicked_file, _with=DEFAULT_WITH)


    def __perform_key_enter(self):
        # if self.__count_selected == 1 and self.__clicked_file.is_selected:
        self.open(self.__clicked_file)


    def __reset_index_of_clicked_file(self) -> Union[bool,None]:
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
        self.__pre_pressed_file        = self.__clicked_file
        self.__scroll_to_file(self.__clicked_file, True)
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


    def __perform_key_btab(self): # TODO: Multiple files shifttab if needed
        if self.__clicked_file and self.__clicked_file.name != '..' and self.has_write_access(self.directory) and self.has_write_access(self.directory + sep + '..'):
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
        if event == 0 or not self.is_focused            : return # https://github.com/GiorgosXou/TUIFIManager/issues/24
        if unicurses.keyname(event) in ('kxOUT','kxIN') : return # https://github.com/GiorgosXou/TUIFIManager/issues/81
        if self.__is_escape_consumed(event)             : return
        if self.properties.handle_events(event): self.consume_escape_once(); return
        if self.menu      .handle_events(event):
            if event == 27: self.consume_escape_once() # the escape condition is necessary for preventing issues with renaming after creation of "new file/folder"
            return
        if self.labelpad: 
            self.labelpad.handle_events(event)

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
- 2023-07-29 03:09:22 AM TODO: ctrl+i or o for navigation to last edited or exited place | Icons | Tabs | Undo redo | Sort | click-drag select multiple | windows unicurses recompile dlls | prevent errors by checking permissions | zz midle word
- 2022-12-19 01:15:32 AM REMINDER: THE REASON WHY I USED self.position.iy INSTEAD OF self.iy IS BECAUSE CHANGING IT THAT WAY DOESN'T REDRAW THE WINDOW
- 2022-12-21 08:23:25 PM REMINDER: What if i rename .. folder?
"""
