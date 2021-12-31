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
        ' ┃┋┃┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, 'vim'),
    '.c':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▃▃▃ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, 'vim'),
    '.cpp':TUIFIProfile((
        ' ┏━━━━++┓ \n'
        ' ┇ █▀▀▀ ┃ \n'  
        ' ┃ █▃▃▃ ┃ \n'
        ' ┗━━━━━━┛ ' 
    ),2, 'vim'),
    '.js':TUIFIProfile(( 
        '  ▃▃▃ ▃▃▃ \n'
        '  ▔█▔ █▃▃ \n'  
        ' ▃ █  ▔▔█ \n'
        ' ▀▀▀  ▀▀▀ '
    ),2, 'vim'),
    '.vb':TUIFIProfile(( 
        ' ▆ ▆ █▀▆  \n'
        ' █ █ █▀▆  \n'  
        ' █ █ █▃▀  \n'
        '  ▀       '                         
    ),8, 'vim'),
    '.cs':TUIFIProfile(( 
        '▃▃▃▃  ▃ ▃ \n'
        '█▔▔▔ ▀█▀█▀\n'  
        '█▃▃▃ ▀█▀█▀\n'
        '▔▔▔▔      '
    ),5, 'vim'),
    '.txt':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┏┇┃☵☲┃┇ \n'
        ' ┃┇┛┃☲☵┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),1, 'vim'),
    '.css':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃CSS┃██┃ \n'
        ' ┃┇▒▒┃☲☰┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, 'vim'),
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
        ' ┃ $ █  ┃ \n'
        ' ┇ SHELL┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.bash':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ $ █  ┃ \n'
        ' ┇ BASH ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.zsh':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ % █  ┃ \n'
        ' ┇ ZSH  ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.fish':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ ><>  ┃ \n'
        ' ┇ FISH ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.cmd':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\>_┃ \n'
        ' ┇ CMD  ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.bat':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\>_┃ \n'
        ' ┇ BAT  ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
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
    ),2),
    '.zip':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' ZIP░░▀▀▀ '
    ),2),
    '.tar':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2),
    '.tar.gz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2),
    '.tar.xz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2),
    '.tar.bz2':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2),
    '.tar.zst':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n' 
        ' ▓▓▓░░▓▓▓ \n' 
        ' TAR░░▀▀▀ '
    ),2),
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
    '.mov':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MOV∴∵◖┇ \n'
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
    '.jpg':TUIFIProfile(( 
        ' ┏━━JPEG╮ \n'
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
        ' ┏━━━BMP╮ \n'
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
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇MP3 ┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.wav':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇WAVE┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.ogg':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇OGG ┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.oga':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇OGG ┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.flac':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇FLAC┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.aac':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇AAC ┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.aiff':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇AIFF┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
    '.opus':TUIFIProfile((
        '  ╭━━━━╮  \n'
        '  ┃    ┃  \n'
        '  ┇OPUS┇  \n'
        ' ◖╹    ╹◗ '
    ),2),
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
