from unicurses import OPERATING_SYSTEM
from shutil    import which



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



DEFAULT_OPENER = 'start' if 'Windows' == OPERATING_SYSTEM else 'open' if 'Darwin' == OPERATING_SYSTEM  else 'xdg-open'   # meh.. # TODO: make an enviromental variable insted of those 2 vars, for everything
DEFAULT_EDITOR = which('nvim') or which('emacs') or which('vim') or which('micro') or which('nano')  or DEFAULT_OPENER 

TUIFIProfiles = { # TODO: open zip rar and etc. files on __init__.py as if they where kind of folders?
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
    '.xlsx':TUIFIProfile((
        ' ┏━━━━┳┳┓ \n'
        ' ┃██▓░┣╋┫ \n'
        ' ┃EXCEL╋┫ \n' 
        ' ╰━━━━┻┻┛ ' 
    ),5, DEFAULT_OPENER),
    '.ino':TUIFIProfile((
        ' ╭━┳┳┳++╮ \n' 
        ' ┃ARDINO┃ \n' 
        ' ┃╭╯╰╯+╮┃ \n' 
        ' ╰┻━━┻┻┻╯ '
    ),4, DEFAULT_EDITOR),
    'file':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇┛FILE ┃ \n'  # 𝗙𝗜𝗟𝗘
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.h':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▂▂█ ┃ \n'  
        ' ┃ █▔▔█ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.c':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.cpp':TUIFIProfile((
        ' ┏━━━━++┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, DEFAULT_EDITOR),
    '.js':TUIFIProfile(( 
        '  ▃▃▃ ▃▃▃ \n'
        'JS▔█▔ █▃▃ \n'  
        ' ▃ █  ▔▔█ \n'
        ' ▀▀▀  ▀▀▀ '
    ),2, DEFAULT_EDITOR),
    '.html':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ HTML ┃ \n'  
        ' ┃ </ > ┃ \n'
        ' ╰━━━━━━╯ ' 
    ),2, DEFAULT_EDITOR),
    '.vb':TUIFIProfile(( 
        ' █ █ █▀▆  \n'
        ' █ █ █▀▆  \n'  
        ' ▀▃▀ █▃▀  \n'
        '          '                         
    ),4, DEFAULT_EDITOR),
    '.vbs':TUIFIProfile(( 
        '▃ ▃ ▃▃  ▃▃\n'
        '█ █ █▃█ █▃\n'  
        '▀▃▀ █▃▀ ▃█\n'
        '          '                         
    ),4, DEFAULT_EDITOR),
    '.md':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┃█▀▅▀▄/┇ \n'  
        ' ┃DOWN//┃ \n'
        ' ╰━━━━━━┛ ' 
    ),4, DEFAULT_EDITOR),
    '.json':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┏┇┏┏┓┓┃ \n'
        ' ┃┇┛JSON┃ \n'
        ' ┗━━━━┛━┛ '
    ),1, DEFAULT_EDITOR),
    '.lua':TUIFIProfile(( 
        '▃  ▃ ▃ ▃▃▃\n'
        '█  █ █ █▃█\n'  
        '█▃▖█▃█ █ █\n'
        '          '                         
    ),4, DEFAULT_EDITOR),
    '.java':TUIFIProfile(( 
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'  
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '                         
    ),3, DEFAULT_EDITOR),
    '.jar':TUIFIProfile(( 
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'  
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '                         
    ),1, DEFAULT_EDITOR),
    '.cs':TUIFIProfile(( 
        '▃▃▃▃  ▃ ▃ \n'
        '█▔▔▔ ▀█▀█▀\n'  
        '█▃▃▃ ▀█▀█▀\n'
        '▔▔▔▔      '
    ),5, DEFAULT_EDITOR),
    '.fs':TUIFIProfile(( 
        '▃▃▃▃  ▃ ▃ \n'
        '█▃▃  ▀█▀█▀\n'  
        '█    ▀█▀█▀\n'
        '▔         '
    ),4, DEFAULT_EDITOR),
    '.go':TUIFIProfile(( 
        '▄▄▄▄ ▄▄▄▄-\n'
        '█ ▄▄ █ ▒█/\n'  
        '█▃▃█/█▃▃█/\n'
        '▔▔▔▔ ▔▔▔▔ '
    ),4, DEFAULT_EDITOR),
    '.rs':TUIFIProfile(( 
        ' ▅▅▅▅▄▃▂  \n'
        '  █▄▃▃▟▛  \n'  
        ' ▃█▃ ▀▆▄▅ \n'
        ' ▔▔▔   ▔  '
    ),3, DEFAULT_EDITOR),
    '.py':TUIFIProfile(( 
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒·   █▒ \n'
        '          '
    ),2, DEFAULT_EDITOR),
    '.txt':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┏┇┃☵☲┃┇ \n'
        ' ┃┇┛┃☲☵┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),1, DEFAULT_EDITOR),
    '.css':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃CSS┃▅▅┃ \n'
        ' ┃┇▒▒┃☲☰┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_EDITOR),
    '.scss':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃SCS┃▅▅┃ \n'
        ' ┃┇▒▒┃S☲┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_EDITOR),
    '.pdf':TUIFIProfile((
        ' ╭━━━━╮━╮ \n'
        ' ┃PDF┃☲ ┃ \n'
        ' ┃┇▒█┃▒▒┃ \n'
        ' ┗━━━━━━╯ '
    ),3, DEFAULT_OPENER),
    '.bin':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃☴☱☶☵ ∟┇ \n'
        ' ┇☱☶ BIN┃ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_OPENER),
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
    ),2, DEFAULT_OPENER),
    '.dll':TUIFIProfile((
        ' ╭━┓━┓╭━┓ \n'
        ' │D┃L┃│L┃ \n'
        ' │█┃▒││▓╿ \n'
        ' ╰━┘━┘╰━┘ ' 
    ),2, DEFAULT_OPENER),
    '.rar':TUIFIProfile((
        ' ▃▃RAR▃▃╮ \n'
        ' ▒▒░ ░▒▒┃ \n'
        ' ▓▓░ ░▓▓┃ \n'
        ' ▀▀░ ░▀▀┘ '
    ),2, DEFAULT_OPENER),
    '.zip':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' ZIP░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '.tar':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '.gz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '.xz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '.bz2':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '.zst':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    
    '.gif':TUIFIProfile((
        ' ┏━━━┳┳┳┓ \n'
        ' ┃GIF:∵◖┇ \n'
        ' ┠┓░▃_▓▆┇ \n'
        ' ╰━━━┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    
    '.mp4':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MP4∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '.3gp':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇3GP∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    
    '.avi':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇AVI∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '.webm':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇WEBM∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '.ogv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇OGV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '.mov':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MOV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '.jpg':TUIFIProfile(( 
        ' ┏━━━JPG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.png':TUIFIProfile(( 
        ' ┏━━━PNG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.jpeg':TUIFIProfile(( 
        ' ┏━━JPEG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.bmp':TUIFIProfile(( 
        ' ┏━━━BMP┓ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.webp':TUIFIProfile(( 
        ' ┏━━WEBP╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.tiff':TUIFIProfile(( 
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.tif':TUIFIProfile(( 
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.tga':TUIFIProfile(( 
        ' ┏━TARGA╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.heif':TUIFIProfile(( 
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.heifs':TUIFIProfile(( 
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '.heic':TUIFIProfile(( 
        ' ┏━━HEIC╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    
    '.mp3':TUIFIProfile(( 
        ' ╭┓━━━━┏╮ \n'
        ' ┣╯MP3♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ╰┛━━━━┗╯ '
    ),8, DEFAULT_OPENER),
    '.wav':TUIFIProfile(( 
        ' ╭┓━━━━┏╮ \n'
        ' ┣╯WAV♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ╰┛━━━━┗╯ '
    ),8, DEFAULT_OPENER),
    '.mid':TUIFIProfile(( 
        ' ╭┓━━━━┏╮ \n'
        ' ┣╯MID♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ╰┛━━━━┗╯ '
    ),8, DEFAULT_OPENER),
    '.aac':TUIFIProfile(( 
        ' ╭┓━━━━┏╮ \n'
        ' ┣╯AAC♪╰┫ \n'
        ' ┇┓♯⦇⦈♯┏┇ \n'
        ' ╰┛━━━━┗╯ '
    ),8, DEFAULT_OPENER),
    
    '.psd':TUIFIProfile((
        ' ╭▃▃▃ ▃▃╮ \n'
        ' ┃█▂█ █▂┃ \n'
        ' ┃█   ▃█┃ \n'
        ' ┗━PSD━━┛ '
    ),4, DEFAULT_OPENER),
    '.mdf':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃┇DB╭▒█┫ \n'
        ' ┠┇██┻▓▒┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_OPENER),
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