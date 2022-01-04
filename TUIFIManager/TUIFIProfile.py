import os
import json 



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



TUIFIProfiles = {}

def load_config(): # create if not load_config | I feel a bit ashamed of this code below but nvm, i've no time for optimizations and etc. right now  
    path = os.path.dirname(os.path.abspath(__file__))   
    file = path + os.sep + 'tuifi_config.json' 
    if not os.path.isfile(file):
        with open(file, "w") as outfile:
            json.dump({
                'folder':((
                    ' █████▒⎫⎫ \n'
                    ' █████▒▐┇ \n'
                    ' █████▒▐┃ \n'
                    ' ▀▀▀▀▀  ┘ '
                ),2),
                'empty_folder':((
                    ' █████ ⎫⎫ \n'
                    ' █████ ┇┇ \n'
                    ' █████ ┃┃ \n'
                    ' ▀▀▀▀▀  ┘ '
                ),2),
                'file':((
                    ' ┏┏━━━━┓┓ \n'
                    ' ┇┛FILE ┃ \n'  # 𝗙𝗜𝗟𝗘
                    ' ┃┋┇┃┃┇┋┃ \n'
                    ' ┗━━━━━━┛ ' 
                ),2, 'vim'),
                '.c':((
                    ' ┏━━━━━━┓ \n'
                    ' ┇ █▀▀▀ ┃ \n'  
                    ' ┃ █▃▃▃ ┃ \n'
                    ' ┗━━━━━━┛ ' 
                ),2, 'vim'),
                '.cpp':((
                    ' ┏━━━━++┓ \n'
                    ' ┇ █▀▀▀ ┃ \n'  
                    ' ┃ █▃▃▃ ┃ \n'
                    ' ┗━━━━━━┛ ' 
                ),2, 'vim'),
                '.js':(( 
                    '  ▃▃▃ ▃▃▃ \n'
                    'JS▔█▔ █▃▃ \n'  
                    ' ▃ █  ▔▔█ \n'
                    ' ▀▀▀  ▀▀▀ '
                ),2, 'vim'),
                '.vb':(( 
                    ' ▆ ▆ █▀▆  \n'
                    ' █ █ █▀▆  \n'  
                    ' █ █ █▃▀  \n'
                    '  ▀       '                         
                ),4, 'vim'),
                '.cs':(( 
                    '▃▃▃▃  ▃ ▃ \n'
                    '█▔▔▔ ▀█▀█▀\n'  
                    '█▃▃▃ ▀█▀█▀\n'
                    '▔▔▔▔      '
                ),5, 'vim'),
                '.txt':((
                    ' ┏━━┓┓┓┓┓ \n'
                    ' ┃┏┇┃☵☲┃┇ \n'
                    ' ┃┇┛┃☲☵┃┃ \n'
                    ' ┗━━┛━━┛┛ '
                ),1, 'vim'),
                '.css':((
                    ' ╭━━━━╮╮╮ \n'
                    ' ┃CSS┃██┃ \n'
                    ' ┃┇▒▒┃☲☰┃ \n'
                    ' ┗━━━╯━━╯ '
                ),2, 'vim'),
                '.pdf':((
                    ' ╭━━━━╮━╮ \n'
                    ' ┃PDF┃☲ ┃ \n'
                    ' ┃┇▒█┃▒▒┃ \n'
                    ' ┗━━━━━━╯ '
                ),3),
                '.bin':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃☴☱☶☵ ∟┇ \n'
                    ' ┇☱☶ BIN┃ \n'
                    ' ╰━━━━━━╯ '
                ),2),
                '.sh':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃ $_   ┃ \n'
                    ' ┇ BASH ┇ \n'
                    ' ╰━━━━━━╯ '
                ),2, 'vim'),
                '.cmd':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃ C:\>_┃ \n'
                    ' ┇ CMD  ┇ \n'
                    ' ╰━━━━━━╯ '
                ),2, 'vim'),
                '.bat':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃ C:\>_┃ \n'
                    ' ┇ BAT  ┇ \n'
                    ' ╰━━━━━━╯ '
                ),2, 'vim'),
                '.so':((
                    ' ╭━┓━┓╭━┓ \n'
                    ' │S┃O┃│Ξ┃ \n'
                    ' │█┃▒││▓╿ \n'
                    ' ╰━┘━┘╰━┘ ' 
                ),2),
                '.dll':((
                    ' ╭━┓━┓╭━┓ \n'
                    ' │D┃L┃│L┃ \n'
                    ' │█┃▒││▓╿ \n'
                    ' ╰━┘━┘╰━┘ ' 
                ),2),
                '.rar':((
                    ' ▃▃RAR▃▃╮ \n'
                    ' ▒▒░ ░▒▒┃ \n'
                    ' ▓▓░ ░▓▓┃ \n'
                    ' ▀▀░ ░▀▀┘ '
                ),2),
                '.zip':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' ZIP░░▀▀▀ '
                ),2),
                '.tar':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' TAR░░▀▀▀ '
                ),2),
                '.tar.gz':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' TAR░░▀▀▀ '
                ),2),
                '.tar.xz':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' TAR░░▀▀▀ '
                ),2),
                '.tar.bz2':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' TAR░░▀▀▀ '
                ),2),
                '.tar.zst':((
                    ' ▃▃▃░░▃▃▃ \n'
                    ' ▒▒▒░░▒▒▒ \n' 
                    ' ▓▓▓░░▓▓▓ \n' 
                    ' TAR░░▀▀▀ '
                ),2),
                '.gif':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃GIF╭▒█┫ \n'
                    ' ┠┇██┤☍ ┃ \n'
                    ' ┗━━━━━━╯ '
                ),2),
                '.mp4':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇MP4∴∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                '.3gp':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇3GP∴∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                
                '.avi':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇AVI∴∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                '.webm':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇WEBM∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                '.ogv':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇OGG∴∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                '.mov':((
                    ' ┏┳┳┳┳┳┳┓ \n'
                    ' ┇MOV∴∵◖┇ \n'
                    ' ┇_░▃_▓▆┇ \n'
                    ' ┗┻┻┻┻┻┻┛ '
                ),2),
                '.jpg':(( 
                    ' ┏━━━JPG╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ╰━━━━━━┛ '
                ),2),
                '.png':(( 
                    ' ┏━━━PNG╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ╰━━━━━━┛ '
                ),2),
                '.jpeg':(( 
                    ' ┏━━JPEG╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ╰━━━━━━┛ '
                ),2),
                '.bmp':(( 
                    ' ┏━━━BMP┓ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.webp':(( 
                    ' ┏━━WEBP╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.tiff':(( 
                    ' ┏━━TIFF╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.tif':(( 
                    ' ┏━━TIFF╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.tga':(( 
                    ' ┏━TARGA╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.heif':(( 
                    ' ┏━━HEIF╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.heifs':(( 
                    ' ┏━━HEIF╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.heic':(( 
                    ' ┏━━HEIC╮ \n'
                    ' ┇*.∴:∵◖┃ \n'
                    ' ┣┓░▃┏▓▆┇ \n'
                    ' ┗━━━━━━┛ '
                ),2),
                '.mp3':(( 
                    ' ┏┓━━━━┏┓ \n'
                    ' ┣╯MP3♪╰┫ \n'
                    ' ┇┓♯⦇⦈♯┏┇ \n'
                    ' ┗┛━━━━┗┛ '
                ),8),
                '.wav':(( 
                    ' ┏┓━━━━┏┓ \n'
                    ' ┣╯WAV♪╰┫ \n'
                    ' ┇┓♯⦇⦈♯┏┇ \n'
                    ' ┗┛━━━━┗┛ '
                ),8),
                '.mid':(( 
                    ' ┏┓━━━━┏┓ \n'
                    ' ┣╯MID♪╰┫ \n'
                    ' ┇┓♯⦇⦈♯┏┇ \n'
                    ' ┗┛━━━━┗┛ '
                ),8),
                '.aac':(( 
                    ' ┏┓━━━━┏┓ \n'
                    ' ┣╯AAC♪╰┫ \n'
                    ' ┇┓♯⦇⦈♯┏┇ \n'
                    ' ┗┛━━━━┗┛ '
                ),8),
                '.mdf':((
                    ' ╭━━━━━━╮ \n'
                    ' ┃┇DB╭▒█┫ \n'
                    ' ┠┇██┻▓▒┃ \n'
                    ' ┗━━━╯━━╯ '
                ),2),
                '.tuifi':((
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
    }, outfile, indent=4)
            
    with open(file) as f:
        data = json.load(f)
        for i in data:
            if len(data[i]) == 2: # I feel a bit ashamed of this code below but nvm, i've no time for optimizations and etc. right now  
                TUIFIProfiles[i] = TUIFIProfile(data[i][0],data[i][1])  
            else:
                TUIFIProfiles[i] = TUIFIProfile(data[i][0],data[i][1], data[i][2])  
load_config()



DEFAULT_PROFILE   = TUIFIProfiles['file'] 
LINK_SYMBOL       = '↩'  # Potential:⤶ ⤾ ↲ ⎌ ☍ ⧉ 
LINK_SYMBOL_COLOR = 1