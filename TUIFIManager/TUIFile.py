import unicurses
from .TUIFIProfile import TUIFIProfile, LINK_SYMBOL, LINK_SYMBOL_COLOR, DEFAULT_PROFILE
from .TUItilities  import DIM, BLD
from os import getenv


VISIBLE_FILENAME_LINES  = int(getenv('tuifi_visible_filename_lines', 4))



class TUIFile:
    #h,w = 4,11 # 10

    def chunk_str(self, text, n):
        base = '\n'.join(text[i:i+n] for i in range(0, len(text), n))
        self.name_height = base.count('\n') + 1 if base.count('\n') + 1 < VISIBLE_FILENAME_LINES  else VISIBLE_FILENAME_LINES
        return base


    def __init__(self, name, y=0, x=0, profile=DEFAULT_PROFILE, name_color=3, is_link=False):
        assert isinstance(profile, TUIFIProfile),'profile needs to be of type class TUIFIProfile'
        self.is_selected = False
        self.is_cut      = False # This is pointless for now, until i find a way of efficiently drawing/managing cuted  files
        self.name_color  = name_color
        self.profile     = profile
        self.y           = y
        self.x           = x
        self.name        = name
        self.is_link     = is_link
        self.is_hidden   = name.startswith('.')
        self.chunk_str(name, self.profile.width)


    def clear(self,atpad):
        pass


    def draw_name(self, atpad, name, prename, chgatXY, attr=unicurses.A_NORMAL):  # fuck, lol
        """
        DON'T USE IT
        """
        offXY = (VISIBLE_FILENAME_LINES * self.profile.width)
        if VISIBLE_FILENAME_LINES and chgatXY >= offXY:
            prename = prename[chgatXY - offXY +1:]
            name = name[chgatXY - offXY +1:]
            chgatXY = 0 + offXY -1

        y = chgatXY // self.profile.width
        x = chgatXY - y * (self.profile.width)

        for offY, ln in enumerate(self.chunk_str(f'{prename} ', self.profile.width).split('\n')[:VISIBLE_FILENAME_LINES], self.profile.height):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ' ' * len(ln)) # A_BOLD | 
        for offY, ln in enumerate(self.chunk_str(name,self.profile.width).split('\n')[:VISIBLE_FILENAME_LINES], self.profile.height):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.name_color ) | attr) # A_BOLD | 
        unicurses.mvwchgat(atpad,self.y + self.profile.height + y, self.x +x, 1, unicurses.A_NORMAL, 1 )


    def __draw_file(self, atpad):
        for offY, ln in enumerate((self.profile.text + '\n').split('\n')):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.profile.color_map ) ) 
        for offY, ln in enumerate(self.chunk_str(self.name,self.profile.width).split('\n')[:VISIBLE_FILENAME_LINES], offY):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.name_color ) )                  

        if self.is_link: # no idea why but mvwadd_wch misbehaves ...
            unicurses.mvwaddwstr(atpad, self.y + self.profile.height -1 , self.x + self.profile.width -1, LINK_SYMBOL, unicurses.COLOR_PAIR(LINK_SYMBOL_COLOR ))  # | A_BOLD


    def __perform_effect(self, atpad, effect, color_map, redraw_icon=False, include_name=False):
        if redraw_icon:self.__draw_file(atpad)
        for y in range(self.y, self.y + self.profile.height):
            unicurses.mvwchgat(atpad,y, self.x, self.profile.width, effect, color_map)

        if not include_name: # meh
            effect    = unicurses.A_NORMAL
            color_map = self.name_color

        for offY, ln in enumerate(self.chunk_str(self.name,self.profile.width).split('\n')[:VISIBLE_FILENAME_LINES], self.profile.height):
            unicurses.mvwchgat(atpad,offY + self.y, self.x, len(ln), effect, color_map)
        # unicurses.mvwchgat(atpad,self.y + self.profile.height + y, self.x +x, 3, unicurses.A_NORMAL, 6 )


    def reverse_effect   (self, atpad, redraw_icon=False, include_name=False): self.__perform_effect(atpad, unicurses.A_REVERSE, 2 , redraw_icon, include_name)
    def dim_effect       (self, atpad, redraw_icon=False, include_name=False): self.__perform_effect(atpad, *DIM(3)               , redraw_icon, include_name) # I think this was supposed to be used for "cutted", I might remove it
    def dim_color_effect (self, atpad,                    include_name=False): self.__perform_effect(atpad, *DIM(self.profile.color_map), False, include_name)
    def bold_color_effect(self, atpad,                    include_name=False): self.__perform_effect(atpad, *BLD(self.profile.color_map), False, include_name)
             

    def draw_effect(self,atpad, y=None, x=None, redraw_icon=False, effect=None, include_name=True):
        if y: self.y = y
        if x: self.x = x
        if   effect == 0: self.bold_color_effect(atpad,               include_name)
        elif effect == 1: self.dim_color_effect (atpad,               include_name)
        elif effect == 2: self.reverse_effect   (atpad, redraw_icon , include_name)
        elif effect == 3: self.dim_effect       (atpad, redraw_icon , include_name)


    def draw(self,atpad, y=None, x=None, redraw_icon=False): #  na valw NEW giati sto resort() xanei to icon kai text h kati tetoio !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if y: self.y = y
        if x: self.x = x

        if self.is_selected: self.reverse_effect(atpad, redraw_icon)
        elif self.is_cut   : self.dim_effect    (atpad, redraw_icon)
        else:
            self.__draw_file(atpad)
            if self.is_hidden: self.dim_color_effect(atpad)
