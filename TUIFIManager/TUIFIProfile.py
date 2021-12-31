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
        'JS▔█▔ █▃▃ \n'  
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
        ' ┃ $_   ┃ \n'
        ' ┇ BASH ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, 'vim'),
    '.cmd':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\>_┃ \n'
        ' ┇ CMD  ┇ \n'
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