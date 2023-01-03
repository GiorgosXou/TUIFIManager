import unicurses

from .TUIFIProfile import TUIFIProfile, LINK_SYMBOL, LINK_SYMBOL_COLOR, DEFAULT_PROFILE


class TUIFile:
    profile = DEFAULT_PROFILE
    #h,w = 4,11 # 10
    x,y         = 0,0
    name_height = 1
    is_selected = False
    is_cut      = False # This is pointless for now, until i find a way of efficiently drawing/managing cuted  files


    def chunk_str(self, text, n):
        base = '\n'.join(text[i:i+n] for i in range(0, len(text), n))
        self.name_height = base.count('\n') + 1
        return base


    def __init__(self, name, y=0, x=0, profile=DEFAULT_PROFILE, name_color=1, is_link=False):
        assert isinstance(profile, TUIFIProfile),'profile needs to be of type class TUIFIProfile'
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


    def draw_name(self, atpad, name, prename, chgatXY, attr=unicurses.A_NORMAL, color_pair_offset=0):  # fuck, lol
        """
        DON'T USE IT
        """
        y = chgatXY // self.profile.width
        x = chgatXY - y * (self.profile.width)
        for offY, ln in enumerate(self.chunk_str(f'{prename} ', self.profile.width).split('\n'), self.profile.height):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ' ' * len(ln)) # A_BOLD | 
        for offY, ln in enumerate(self.chunk_str(name,self.profile.width).split('\n'), self.profile.height):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.name_color + color_pair_offset) | attr) # A_BOLD | 
        unicurses.mvwchgat(atpad,self.y + self.profile.height + y, self.x +x, 1, unicurses.A_NORMAL, 6 + color_pair_offset)


    def __draw_file(self, atpad, color_pair_offset=0):
        for offY, ln in enumerate((self.profile.text + '\n').split('\n')):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.profile.color_map + color_pair_offset) ) 
        for offY, ln in enumerate(self.chunk_str(self.name,self.profile.width).split('\n'), offY):
            unicurses.mvwaddwstr(atpad,offY + self.y,self.x, ln, unicurses.COLOR_PAIR(self.name_color + color_pair_offset) )                  

        if self.is_link: # no idea why but mvwadd_wch misbehaves ...
            unicurses.mvwaddwstr(atpad, self.y + self.profile.height -1 , self.x + self.profile.width -1, LINK_SYMBOL, unicurses.COLOR_PAIR(LINK_SYMBOL_COLOR + color_pair_offset))  # | A_BOLD


    def __perform_effect(self, atpad, effect, color_map, redraw_icon=False, include_name=False):
        if redraw_icon:self.__draw_file(atpad)
        for y in range(self.y, self.y + self.profile.height):
            unicurses.mvwchgat(atpad,y, self.x, self.profile.width, effect, color_map)

        if not include_name: # meh
            effect    = unicurses.A_NORMAL
            color_map = self.name_color

        for offY, ln in enumerate(self.chunk_str(self.name,self.profile.width).split('\n'), self.profile.height):
            unicurses.mvwchgat(atpad,offY + self.y, self.x, len(ln), effect, color_map)
        # unicurses.mvwchgat(atpad,self.y + self.profile.height + y, self.x +x, 1, unicurses.A_NORMAL, 6 + color_pair_offset)


    def reverse_effect   (self, atpad, redraw_icon=False, color_pair_offset=0, include_name=False): self.__perform_effect(atpad, unicurses.A_REVERSE, 7 + color_pair_offset                      , redraw_icon, include_name)
    def dim_effect       (self, atpad, redraw_icon=False, color_pair_offset=0, include_name=False): self.__perform_effect(atpad, unicurses.A_DIM    , 1 + color_pair_offset                      , redraw_icon, include_name)
    def dim_color_effect (self, atpad,                    color_pair_offset=0, include_name=False): self.__perform_effect(atpad, unicurses.A_DIM    , self.profile.color_map + color_pair_offset , False      , include_name)
    def bold_color_effect(self, atpad,                    color_pair_offset=0, include_name=False): self.__perform_effect(atpad, unicurses.A_BOLD   , self.profile.color_map + color_pair_offset , False      , include_name)
             

    def draw_effect(self,atpad, y=None, x=None, redraw_icon=False, color_pair_offset=0, effect=None, include_name=True):
        if y: self.y = y
        if x: self.x = x
        if   effect == 0: self.bold_color_effect(atpad,               color_pair_offset, include_name)
        elif effect == 1: self.dim_color_effect (atpad,               color_pair_offset, include_name)
        elif effect == 2: self.reverse_effect   (atpad, redraw_icon , color_pair_offset, include_name)
        elif effect == 3: self.dim_effect       (atpad, redraw_icon , color_pair_offset, include_name)


    def draw(self,atpad, y=None, x=None, redraw_icon=False, color_pair_offset=0): #  na valw NEW giati sto resort() xanei to icon kai text h kati tetoio !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if y: self.y = y
        if x: self.x = x

        if self.is_selected: self.reverse_effect(atpad, redraw_icon , color_pair_offset)
        elif self.is_cut   : self.dim_effect    (atpad, redraw_icon , color_pair_offset)
        else:
            self.__draw_file(atpad, color_pair_offset)
            if self.is_hidden: self.dim_color_effect(atpad, color_pair_offset)
