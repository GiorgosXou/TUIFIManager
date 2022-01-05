class TUIFIProfile: #█┇▓┃▒┃░┃ 
    """
    Profile/Icon/Type
    """
    def __init__(self, text, color_map=1, open_with=None):
        self.text         = text
        self.color_map    = color_map  # I know it's not but i will in the future maybe?
        self.open_with    = open_with 
        temp_profileSplit = self.text.split('\n')
        self.width        = len(max(temp_profileSplit, key=len))
        self.height       = len(temp_profileSplit)
        #self.open_with    = ['']



DEFAULT_EDITOR       = 'vim'
DEFAULT_UNCOMPRESSOR = 'vim'

TUIFIProfiles = {
    'folder':TUIFIProfile((
        ' █████▒⎫⎫ \n'
        ' █████▒▐┇ \n'
        ' █████▒▐┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),2),
    'empty_folder':TUIFIProfile((
        ' █████ ⎫⎫ \n'
        ' █████ ┇┇ \n'
        ' █████ ┃┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),2),
    'file':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇┛FILE ┃ \n'  # 𝗙𝗜𝗟𝗘
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.c':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▃▃▃ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.cpp':TUIFIProfile((
        ' ┏━━━━++┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▃▃▃ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.js':TUIFIProfile(( 
        '  ▃▃▃ ▃▃▃ \n'
        'JS▔█▔ █▃▃ \n'  
        ' ▃ █  ▔▔█ \n'
        ' ▀▀▀  ▀▀▀ '
    ),2, DEFAULT_EDITOR),
    '.vb':TUIFIProfile(( 
        ' ▆ ▆ █▀▆  \n'
        ' █ █ █▀▆  \n'  
        ' █ █ █▃▀  \n'
        '  ▀       '                         
    ),4, DEFAULT_EDITOR),
    '.cs':TUIFIProfile(( 
        '▃▃▃▃  ▃ ▃ \n'
        '█▔▔▔ ▀█▀█▀\n'  
        '█▃▃▃ ▀█▀█▀\n'
        '▔▔▔▔      '
    ),5, DEFAULT_EDITOR),
    '.txt':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┏┇┃☵☲┃┇ \n'
        ' ┃┇┛┃☲☵┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),1, DEFAULT_EDITOR),
    '.css':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃CSS┃██┃ \n'
        ' ┃┇▒▒┃☲☰┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_EDITOR),
    '.pdf':TUIFIProfile((
        ' ╭━━━━╮━╮ \n'
        ' ┃PDF┃☲ ┃ \n'
        ' ┃┇▒█┃▒▒┃ \n'
        ' ┗━━━━━━╯ '
    ),3),
    '.bin':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃☴☱☶☵ ∟┇ \n'
        ' ┇☱☶ BIN┃ \n'
        ' ╰━━━━━━╯ '
    ),2),
    '.sh':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ $_   ┃ \n'
        ' ┇ BASH ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '.cmd':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\>_┃ \n'
        ' ┇ CMD  ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '.bat':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\>_┃ \n'
        ' ┇ BAT  ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '.so':TUIFIProfile((
        ' ╭━┓━┓╭━┓ \n'
        ' │S┃O┃│Ξ┃ \n'
        ' │█┃▒││▓╿ \n'
        ' ╰━┘━┘╰━┘ ' 
    ),2),
    '.dll':TUIFIProfile((
        ' ╭━┓━┓╭━┓ \n'
        ' │D┃L┃│L┃ \n'
        ' │█┃▒││▓╿ \n'
        ' ╰━┘━┘╰━┘ ' 
    ),2),
    '.rar':TUIFIProfile((
        ' ▃▃RAR▃▃╮ \n'
        ' ▒▒░ ░▒▒┃ \n'
        ' ▓▓░ ░▓▓┃ \n'
        ' ▀▀░ ░▀▀┘ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.zip':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' ZIP░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.tar':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.gz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.xz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.bz2':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.zst':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2,DEFAULT_UNCOMPRESSOR),
    '.gif':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃GIF╭▒█┫ \n'
        ' ┠┇██┤☍ ┃ \n'
        ' ┗━━━━━━╯ '
    ),2),
    '.mp4':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MP4∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    '.3gp':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇3GP∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    
    '.avi':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇AVI∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    '.webm':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇WEBM∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    '.ogv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇OGG∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    '.mov':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MOV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2),
    '.jpg':TUIFIProfile(( 
        ' ┏━━━JPG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2),
    '.png':TUIFIProfile(( 
        ' ┏━━━PNG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2),
    '.jpeg':TUIFIProfile(( 
        ' ┏━━JPEG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2),
    '.bmp':TUIFIProfile(( 
        ' ┏━━━BMP┓ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.webp':TUIFIProfile(( 
        ' ┏━━WEBP╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.tiff':TUIFIProfile(( 
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.tif':TUIFIProfile(( 
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.tga':TUIFIProfile(( 
        ' ┏━TARGA╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.heif':TUIFIProfile(( 
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.heifs':TUIFIProfile(( 
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.heic':TUIFIProfile(( 
        ' ┏━━HEIC╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2),
    '.mp3':TUIFIProfile(( 
        ' ┏┓━━━━┏┓ \n'
        ' ┣╯MP3♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ┗┛━━━━┗┛ '
    ),8),
    '.wav':TUIFIProfile(( 
        ' ┏┓━━━━┏┓ \n'
        ' ┣╯WAV♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ┗┛━━━━┗┛ '
    ),8),
    '.mid':TUIFIProfile(( 
        ' ┏┓━━━━┏┓ \n'
        ' ┣╯MID♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ┗┛━━━━┗┛ '
    ),8),
    '.aac':TUIFIProfile(( 
        ' ┏┓━━━━┏┓ \n'
        ' ┣╯AAC♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ┗┛━━━━┗┛ '
    ),8),
    '.psd':TUIFIProfile((
        ' ╭▃▃▃ ▃▃╮ \n'
        ' ┃█ █ █▃┃ \n'
        ' ┃█▔▔ ▃█┃ \n'
        ' ┗━PSD━━┛ '
    ),4),
    '.mdf':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃┇DB╭▒█┫ \n'
        ' ┠┇██┻▓▒┃ \n'
        ' ┗━━━╯━━╯ '
    ),2),
    '.tuifi':TUIFIProfile((
        '             \                                      [            \n' 
        '              @                 ⟡                  ╢             \n' 
        '      /       ╣▒                                  ]▒       \     \n' 
        '     ╔       ]Ñ▒                                  ╟╣┐       ▓    \n' 
        '    ╢╣       ╣▓            √          t            ▓╣       ▓╣   \n' 
        '   ▓╣▒╖    ╓╫╜           ╥▓   #TUIFI   ▓@           ╙▓╖    ╔╣╢║  \n' 
        '   ▓▓▓▓  ,p▓,,,,,,      ╜╙▓▄╖,      ,╓╥╜╙╙    ,,,,,,,,▓▓,  ▀▓▓╣U \n' 
        '   ▀▓Ö   ╙█▓▓▓▓▓▓╢╫╣▓▓▓▓▓╦, ▀▓▓╗  g╢▓╝ ,╓H╢╢╢╢╢╢▓▓▓▓▓▓▒▓╜   ]▓▓  \n' 
        '    ▓▓▓╦╥╖ ╙╙╙╙`     `""▀▓▓@ ▐█▓L]▓╫╛ Æ▒╨╜"       ""╙╙` ╓╖∩▒▒▓   \n' 
        ' ╒▓▒╜""╙▀▓▓                ▀  █▒Γ▐▓▓  ╩                ▓╢╜""╙▀█╫L\n' 
        ' ▐▌`      └╝                  ▓▒` █▓                  ╜       └█▓\n' 
        '▐▓                            ▓▒  █╢                           ▐▓\n' 
        ' ▐Γ                            ╛  ▐"                           ▐[\n' 
        ' ¬U                                                            jU\n' 
        '  C                                                            j \n' 
        '   L                                                          ]  \n'
        '                                                                 '     
    ),2)     
}
DEFAULT_PROFILE   = TUIFIProfiles['file'] 
LINK_SYMBOL       = '↩'  # Potential:⤶ ⤾ ↲ ⎌ ☍ ⧉ 
LINK_SYMBOL_COLOR = 1