from .TUIFIProfile import TUIFIProfiles
from  .TUItilities import Border, WindowPad, Label, clipboard, IS_WINDOWS, lock
from      .TUIFile import TUIFile, VISIBLE_FILENAME_LINES
from      datetime import datetime
from       os.path import basename, sep, join, getsize
from          copy import copy
from            os import stat, walk
import unicurses
import threading
if not IS_WINDOWS:
    from pwd import getpwuid



size_units = ('bytes', 'KB', 'MB', 'GB', 'TB')
def convert_bytes(num): #WARN: https://stackoverflow.com/a/63839503/11465149 | https://stackoverflow.com/a/78117390/11465149
    step_unit = 1000.0
    for x in size_units:
        if num < step_unit:
            if x[0] == 'b': return "%i %s" % (num, x)
            return "%3.1f %s" % (num, x)
        num /= step_unit



class TUIProps(WindowPad):
    def __init__(self, border=Border(), on_choice=lambda *args : None ):
        super().__init__(border=border, height=12+VISIBLE_FILENAME_LINES, width=35, anchor=(True, True, True, True))
        self.is_locked = False
        unicurses.wbkgd(self.pad,unicurses.COLOR_PAIR(9))
        self.maxheight = 12 + VISIBLE_FILENAME_LINES
        self.minheight = 12 + VISIBLE_FILENAME_LINES
        self.maxwidth  = 35
        self.minwidth  = 35
        self.exists = False
        # self.picturebox = PictureBoxMono(self, y=2,x=3)
        Label(self,1,2,"MODIFIED:", color=9, style=unicurses.A_BOLD)
        Label(self,2,2,"ACCESSED:", color=9,                       )
        Label(self,3,2,"CHANGED :", color=9, style=unicurses.A_DIM )
        self.label4 = Label(self,1,12,"", wrap_text=True,  style=unicurses.A_BOLD)
        self.label5 = Label(self,2,12,"", wrap_text=True,                        )
        self.label6 = Label(self,3,12,"", wrap_text=True,  style=unicurses.A_DIM )

        self.label3 = Label(self,5,15,"SIZE:", color=9, wrap_text=True,  style=unicurses.A_BOLD)
        self.label2 = Label(self,6,15,"OPEN:", color=9, wrap_text=True,                        )
        self.label1 = Label(self,7,15,"INODE", color=9, wrap_text=True,  style=unicurses.A_DIM )
        self.label7 = Label(self,5,21,"", wrap_text=True,  style=unicurses.A_BOLD)
        self.label8 = Label(self,6,21,"", wrap_text=True,                        )
        self.label9 = Label(self,7,21,"", wrap_text=True,  style=unicurses.A_DIM )

        self.label  = Label(self,self.height-2,1,"", color=9, width=self.width-2, style=unicurses.A_REVERSE|unicurses.A_BOLD)


    def get_directory_size(self, directory):
        total_size = 0
        # Traverse the directory tree
        for dirpath, dirnames, filenames in walk(directory):
            if not self.exists: break
            for f in filenames:
                if not self.exists: break
                fp = join(dirpath, f)
                try:
                    total_size += getsize(fp)
                except OSError as e:
                    print(f"Error getting size for {fp}: {e}")
            # if not self.is_locked:
            self.label7.text = convert_bytes(total_size)


    def __get_size(self, directory:str, size_offset, files_num_offset):
        # Traverse the directory tree
        for dirpath, dirnames, filenames in walk(directory):
            if not self.exists: break
            for f in filenames:
                if not self.exists: break
                fp = join(dirpath, f)
                try:
                    size_offset += getsize(fp)
                    files_num_offset +=1
                except OSError as e:
                    print(f"Error getting size for {fp}: {e}")
            # if not self.is_locked:
            self.label7.text = convert_bytes(size_offset)
        return size_offset, files_num_offset


    if not IS_WINDOWS:
        def get_owner(self, uid): return getpwuid(uid).pw_name
    else:
        def get_owner(self, uid): return uid


    def __adjust_ui_positions_based_on(self, tuifile:TUIFile):
        self.label1.position.x = tuifile.x + tuifile.profile.width + 2 # to take into consideration icon packs of differect sizes i guess
        self.label2.position.x = tuifile.x + tuifile.profile.width + 2
        self.label3.position.x = tuifile.x + tuifile.profile.width + 2
        self.label7.position.x = tuifile.x + tuifile.profile.width + 2 + 6# to take into consideration icon packs of differect sizes i guess
        self.label8.position.x = tuifile.x + tuifile.profile.width + 2 + 6
        self.label9.position.x = tuifile.x + tuifile.profile.width + 2 + 6


    def __set_tuifile_datetimes_from_stats(self, info):
        self.label4._text = self.mdt = datetime.fromtimestamp(info.st_mtime).strftime('%d/%m/%Y - %H:%M:%S') # todo: windows deprecation?
        self.label5._text = self.adt = datetime.fromtimestamp(info.st_atime).strftime('%d/%m/%Y - %H:%M:%S')
        self.label6._text = self.cdt = datetime.fromtimestamp(info.st_ctime).strftime('%d/%m/%Y - %H:%M:%S')


    def __set_datetimes(self, min_m, min_a, min_c, max_m, max_a, max_c):
        self.label4._text = self.mdt = datetime.fromtimestamp(min_m).strftime('%d/%m/%y -> ') + datetime.fromtimestamp(max_m).strftime('%d/%m/%y')# todo: windows deprecation?
        self.label5._text = self.adt = datetime.fromtimestamp(min_a).strftime('%d/%m/%y -> ') + datetime.fromtimestamp(max_a).strftime('%d/%m/%y')
        self.label6._text = self.cdt = datetime.fromtimestamp(min_c).strftime('%d/%m/%y -> ') + datetime.fromtimestamp(max_c).strftime('%d/%m/%y')


    def __set_multiple_properties_of(self, tuifiles, directory):
        self.label1._text = "FILES" 
        self.label8._text = "MULTI"
        self.label ._text = ""
        self.open_with    = ""
        info = None
        self.path = ""
        M_dt = 0  
        A_dt = 0  
        C_dt = 0  
        m_dt = 99999999999 # yeah in 3114 you may need to replace it with sys.maxint which I hesitate a bit to replace with it for now...
        a_dt = 99999999999
        c_dt = 99999999999
        self.bytes = 0
        i = 0
        fnum = 0
        for tfl in tuifiles:
            if not tfl.is_selected: continue
            self.path = f'{directory}{sep}{tfl.name}'
            info = stat(self.path)

            if M_dt < info.st_mtime: M_dt = info.st_mtime
            if A_dt < info.st_atime: A_dt = info.st_atime
            if C_dt < info.st_ctime: C_dt = info.st_ctime
            if m_dt > info.st_mtime: m_dt = info.st_mtime
            if a_dt > info.st_atime: a_dt = info.st_atime
            if c_dt > info.st_ctime: c_dt = info.st_ctime

            self.__set_datetimes(m_dt, a_dt, c_dt, M_dt, A_dt, C_dt)

            if tfl.profile.open_with: # aka folder
                self.bytes += info.st_size
            else:
                self.bytes, fnum = self.__get_size(self.path, self.bytes, fnum)
            i+=1
            fnum+=1
            self.label9._text = str(fnum)
            self.label ._text = f' BYTES: {self.bytes}'
            self.label7. text = convert_bytes(self.bytes)
        return info


    def __set_single___properties_of(self, tuifile, directory):
        self.label1._text = "INODE" 
        self.open_with = tuifile.profile.open_with if tuifile.profile.open_with else "TUIFI"
        self.label8._text = basename(self.open_with) 
        self.path = f'{directory}{sep}{tuifile.name}'
        info = stat(self.path)
        self.bytes = 0
        fnum = 0
        self.inode = info.st_ino
        self.label9._text = str(self.inode)
        self.__set_tuifile_datetimes_from_stats(info)
        if tuifile.profile.open_with: # aka folder
            self.bytes += info.st_size
        else:
            self.bytes, fnum = self.__get_size(self.path, self.bytes, fnum) # fnum+=1
        self.label._text = f' OWNER: {self.get_owner(info.st_uid)}'
        self.label7. text = convert_bytes(self.bytes)


    def __draw_profile_of(self, tuifile:TUIFile):
        tuifile.is_selected = False
        tuifile.draw(self.pad, 5,3) # might replace it with PictureBoxMono in the future
        tuifile.draw_effect(self.pad, effect=0)


    def __set_properties_of(self, tuifiles, directory:str):
        tmp_tuifile = copy(tuifiles[0]) if len(tuifiles) == 1 else TUIFile('SELECTIONS', profile=TUIFIProfiles[":all"])
        self.__draw_profile_of(tmp_tuifile)
        self.__adjust_ui_positions_based_on(tmp_tuifile)

        if len(tuifiles) > 1: self.__set_multiple_properties_of(tuifiles, directory)
        else                : self.__set_single___properties_of(tmp_tuifile, directory)

        self.is_focused = False # seems to be necessary for resolving an issue the first time ctrl+p is pressed when tuifi first runs
        self.refresh()


    def create_tui_for(self, tuifiles:list[TUIFile], directory:str): # kinda the same as TUIMenu's create
        if self.exists: unicurses.werase(self.pad)

        self.inode = None
        self.mdt   = None
        self.adt   = None
        self.cdt   = None

        self.exists = True
        self.center()
        t = threading.Thread(target=self.__set_properties_of,args=(tuifiles,directory))
        t.start()
        return


    def delete(self):
        if self.exists:
            with lock:
                unicurses.werase(self.pad) # for tfl draw
            self.__it   = 0
            self.exists = False
            self.is_focused = False
        return True


    def refresh(self, redraw_parent=False):
        if self.exists:# and not self.is_locked: 
            super().refresh(redraw_parent=redraw_parent, clear=False)
            self.is_focused = True


    def handle_resize(self, redraw_parent=True, redraw_border=True):
        self.is_focused = False; 
        return super().handle_resize(redraw_parent, redraw_border)


    def handle_events(self, event):
        if not self.exists: return False
        if event == 27                  : return self.delete()
        if event == unicurses.KEY_MOUSE : return self.__handle_special_mouse_events(event)
        if event == unicurses.KEY_RESIZE: return self.handle_resize()
            
        event_consumed = super().handle_events(event)

        if   event == unicurses.CCHAR('s'): return clipboard(str(self.bytes   ));
        elif event == unicurses.CCHAR('i'): return clipboard(str(self.inode   ));
        elif event == unicurses.CCHAR('o'): return clipboard(    self.open_with);
        elif event == unicurses.CCHAR('m'): return clipboard(    self.mdt      );
        elif event == unicurses.CCHAR('a'): return clipboard(    self.adt      );
        elif event == unicurses.CCHAR('c'): return clipboard(    self.cdt      );

        if not event_consumed: self.delete()
        return event_consumed


    def __handle_special_mouse_events(self, event):
        in_range, id, x, y, z, bstate = self.get_mouse()
        if (bstate & unicurses.BUTTON4_PRESSED) or (bstate & unicurses.BUTTON5_PRESSED): # Scroll
            self.is_focused = False # it gets to True imidiatly after
            return False
        if bstate & unicurses.BUTTON1_RELEASED and not (self.x <= x < self.x + self.width and self.y <= y < self.y + self.height):
            self.delete() #unicurses.ungetmouse(id, x, y, z, bstate )
        self.__x, self.__y = x,y
        return True
