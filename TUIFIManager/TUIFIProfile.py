from unicurses import OPERATING_SYSTEM
from shutil    import which
from os        import getenv


class TUIFIProfile: #█┇▓┃▒┃░┃
    """
    Profile/Icon/Type
    """
    def __init__(self, text, color_map=1, open_with=None):
        self.text         = text
        self.color_map    = color_map  # I know it's not but i will in the future maybe? # TODO: __20221216043020PM
        self.open_with    = open_with
        temp_profileSplit = self.text.split('\n')
        self.width        = len(max(temp_profileSplit, key=len))
        self.height       = len(temp_profileSplit)
        #self.open_with    = ['']



DEFAULT_OPENER = 'start' if 'Windows' == OPERATING_SYSTEM else 'open' if 'Darwin' == OPERATING_SYSTEM  else 'xdg-open'   # meh.. # TODO: make an enviromental variable insted of those 2 vars, for everything
DEFAULT_EDITOR = which(getenv('tuifi_default_editor', getenv('EDITOR', 'nvim'))) or which('emacs') or which('vim') or which('micro') or which('nano')  or which('vi') or DEFAULT_OPENER
DEFAULT_WITH   = DEFAULT_EDITOR

TUIFIProfiles = { # TODO: ADD gitignore and etc. icons | TODO: open zip rar and etc. files on __init__.py as if they where kind of folders?
    ':folder':TUIFIProfile(( # TODO: change folder and empty_folder to something containing illegal characters because if someone names a hidden file that way, there will be a conflict 2022-12-19 09:16:13 PM
        ' █████▒⎫⎫ \n'
        ' █████▒▐┇ \n'
        ' █████▒▐┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),2),
    ':empty_folder':TUIFIProfile((
        ' █████ ⎫⎫ \n'
        ' █████ ┇┇ \n'
        ' █████ ┃┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),2),
    ':file':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇┛FILE ┃ \n'  # 𝗙𝗜𝗟𝗘
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),

    '.gitattributes':TUIFIProfile((
        '          \n'
        ' ┏ATR┏▄ ┓ \n'
        ' ┇█▓░┣┻▄┇ \n'
        ' ┗━━ ▀  ┛ '
    ),1, DEFAULT_EDITOR),
    '.gitignore':TUIFIProfile((
        '          \n'
        ' ┏━ ┏▄ ━┓ \n'
        ' ┇▓░┣┻▄ ┇ \n'
        ' ┗━ ▀  ━┛ '
    ),1, DEFAULT_EDITOR),

    'makefile':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃█▀▅▀█┣┫ \n'
        ' ┣━MAKE┻┫ \n'
        ' ┗━┻━━┻━┛ '
    ),2, DEFAULT_EDITOR),
    'config':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    'license':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┃▄▀█▀▅┇┇ \n'
        ' ┃┻▂█▂┻┃┃ \n'
        ' ┗━━━━━┻┛ '
    ),2, DEFAULT_EDITOR),

    '/cfg':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/conf':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/ini':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇┗INIT┛┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/ppt':TUIFIProfile((
        ' ╭━━━━┳╮╮ \n'
        ' ┇PPTX┃├┃ \n'
        ' ┃[▒▒]┃├┇ \n'
        ' ╰━━━━┻━╯ '
    ),3, DEFAULT_OPENER),
    '/pptx':TUIFIProfile((
        ' ╭━━━━┳╮╮ \n'
        ' ┇PPTX┃├┃ \n'
        ' ┃[▒▒]┃├┇ \n'
        ' ╰━━━━┻━╯ '
    ),3, DEFAULT_OPENER),
    '/xlsx':TUIFIProfile((
        ' ┏━━━━┳┳┓ \n'
        ' ┃██▓░┣╋┫ \n'
        ' ┃EXCEL╋┫ \n'
        ' ╰━━━━┻┻┛ '
    ),5, DEFAULT_OPENER),
    '/csv':TUIFIProfile((
        ' ┏━━━┳┳┳┓ \n'
        ' ┃█▓░┣╋╋┫ \n'
        ' ┃CSV┣╋╋┫ \n'
        ' ╰━━━┻┻┻┛ '
    ),1, DEFAULT_OPENER),

    '/ino':TUIFIProfile((
        ' ┏┳┳┳━━━╮ \n'
        ' ┇ARDINO┃ \n'
        ' ┃━ ┗┛+┓┃ \n'
        ' ╰┻━━┻┻┻┛ '
    ),4, DEFAULT_EDITOR),
    '/h':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▂▂█ ┃ \n'
        ' ┃ █▔▔█ ┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/c':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀▀ ┃ \n'
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/cpp':TUIFIProfile((
        ' ┏━━━━++┓ \n'
        ' ┇ █▀▀▀ ┃ \n'
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/toml':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┃░░┃┃░░┃ \n' 
        ' ┃░░┇┃░░┃ \n'
        ' ┗━━ ┛━━┛ '
    ),3, DEFAULT_EDITOR),
    '/js':TUIFIProfile((
        ' ┌━━━━━━┐ \n'
        ' │▀█▀▒▀▀│ \n'
        ' │▃█ ▃▃▓│ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/ts':TUIFIProfile((
        ' ┌━━━━━━┐ \n'
        ' │▀█▀▒▀▀│ \n'
        ' │ █ ▃▃▓│ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/html':TUIFIProfile((
        ' ┌━━━━━━┐ \n'
        ' ├┤HTML├┤ \n'
        ' │ </.> │ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/xml':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇┤XML ├┃ \n'
        ' ┃├ </.>┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),

    '/vb':TUIFIProfile((
        ' ▃ ▃ ▃▃   \n'
        ' █ █ █▃█  \n'
        ' ▀▃▀ █▃▀┇ \n'
        '     ━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/vbs':TUIFIProfile((
        '▃ ▃ ▃▃  ▃▃\n'
        '█ █ █▃█ █▃\n'
        '▀▃▀ █▃▀ ▃█\n'
        '          '
    ),4, DEFAULT_EDITOR),
    '/apk':TUIFIProfile((
        ' ▃  ▃▃ ▃ ▃\n'
        '█▃█ ██ █▃▀\n'
        '█ █ █  █ █\n'
        '          '
    ),5, DEFAULT_OPENER),
    '/vim':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃VI━━━┫┇ \n'
        ' ┃█▀▅▀▄┃┃ \n'
        ' ╰━━━━━┻┛ '
    ),5, DEFAULT_EDITOR),
    '/md':TUIFIProfile((
        ' ┏━━━━━┓┓ \n'
        ' ┃█▀▅▀▄┃┇ \n'
        ' ┃DOWN━┫┫ \n'
        ' ╰━━━━━┻┛ '
    ),4, DEFAULT_EDITOR),

    '/json':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┏┇┏┏┓┓┃ \n'
        ' ┃┇┛JSON┃ \n'
        ' ┗━━━━┛━┛ '
    ),1, DEFAULT_EDITOR),
    '/yaml':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┏┇YAML┃ \n'
        ' ┃┇┛┗┗┛┛┃ \n'
        ' ┗━━━━┛━┛ '
    ),1, DEFAULT_EDITOR),
    '/yml':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┇┓YAML┃ \n'
        ' ┃┗┇┗┗┛┛┃ \n'
        ' ┗━━━━┛━┛ '
    ),1, DEFAULT_EDITOR),

    '/lua':TUIFIProfile((
        '▃  ▃ ▃ ▃▃▃\n'
        '█  █ █ █▃█\n'
        '█▃▖█▃█ █ █\n'
        '          '
    ),4, DEFAULT_EDITOR),
    '/java':TUIFIProfile((
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '
    ),3, DEFAULT_EDITOR),
    '/jar':TUIFIProfile((
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '
    ),1, DEFAULT_EDITOR),
    '/cs':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' │ █▀▀▀ │ \n'
        ' │ █▄▄▄ │ \n'
        ' ┕━━━━━━╯ '
    ),5, DEFAULT_EDITOR),
    '/fs':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' │ █▀▀▀ │ \n'
        ' │ █▀▀ #│ \n'
        ' ┕━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/go':TUIFIProfile((
        ' ┏━━━━━━╮ \n'
        ' ┇█▀▀▒▀█│ \n'
        ' ┃█▃█▓▃█│ \n'
        ' ┗━━━━━━╯ ' 
    ),4, DEFAULT_EDITOR),
    '/rs':TUIFIProfile((
        ' ▄▄▄▄▄▃▂  \n'
        ' ▔█▄▃▃▟▛  \n'
        ' ▃█▃ ▀▆▄▅ \n'
        ' ▔▔▔   ▔  '
    ),3, DEFAULT_EDITOR),
    '/py':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒·   █▒ \n'
        '          '
    ),2, DEFAULT_EDITOR),
    '/pyc':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒.101█▒ \n'
        '          '
    ),1, DEFAULT_EDITOR),
    '/pyw':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒.wW.█▒ \n'
        '          '
    ),1, DEFAULT_EDITOR),
    '/txt':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┏┇┃☵☲┃┇ \n'
        ' ┃┇┛┃☲☵┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),1, DEFAULT_EDITOR),
    '/log':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┋┇┃☵☲┃┇ \n'
        ' ┃┇┋┃☲☵┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),1, DEFAULT_EDITOR),
    '/qml':TUIFIProfile((
        ' ╭━━┯━━━┑ \n'
        ' ┝┳━┥QML│ \n'
        ' ┝┻━┷━━━┥ \n'
        ' ┕━━━━━━╯ '
    ),5, DEFAULT_EDITOR),
    '/css':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃CSS┃▅▅┃ \n'
        ' ┃┇▒▒┃☲☰┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_EDITOR),
    '/scss':TUIFIProfile((
        ' ╭━━━━╮╮╮ \n'
        ' ┃SCS┃▅▅┃ \n'
        ' ┃┇▒▒┃S☲┃ \n'
        ' ┗━━━╯━━╯ '
    ),2, DEFAULT_EDITOR),
    '/pdf':TUIFIProfile((
        ' ╭━━━━╮━╮ \n'
        ' ┃PDF┃==│ \n'
        ' ┃┇▒█┃▒▒│ \n'
        ' ┗━━━━━━╯ '
    ),3, DEFAULT_OPENER),


    '/stl':TUIFIProfile((
        ' ╭─╭┰─╮─╮ \n'
        ' │╭╰┸─╯╮│ \n'
        ' │╰.STL╯│ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_OPENER),
    '/gcode':TUIFIProfile((
        ' ╭─╭─┰╮─┒ \n'
        ' │[╰┬┸╯]┇ \n'
        ' │GCODE:┃ \n'
        ' ╰━━━━━━┛ '
    ),1, DEFAULT_OPENER),
    '/fcstd':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┃░█▀▀/:┃ \n'
        ' ┃░█▀CAD┇ \n'
        ' ┗━━━━━━┛ '
    ),3, DEFAULT_EDITOR),
    '/fcstd1':TUIFIProfile((
        ' ╭────━━┓ \n'
        ' │░█▀▀ER┃ \n'
        ' │░█▀STO┇ \n'
        ' ╰━━━━━━┛ '
    ),1, DEFAULT_EDITOR),


    '/lock':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┣┗LOCK┛┫ \n'
        ' ┃┋┇[]┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_EDITOR),
    '/bin':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' │OIIOIO│ \n'
        ' │━━━BIN│ \n'
        ' ╰━━━━━━╯ '
    ),1, DEFAULT_OPENER),
    '/sh':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ $_   ┃ \n'
        ' ┇ BASH ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/cmd':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\> ┃ \n'
        ' ┇ CMD_ ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/bat':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\> ┃ \n'
        ' ┇ BAT_ ┇ \n'
        ' ╰━━━━━━╯ '
    ),2, DEFAULT_EDITOR),
    '/so':TUIFIProfile((
        ' ╭━╭━┳╭━╮ \n'
        ' │S│O┠│Ξ│ \n'
        ' │▒│█┠│▒│ \n'
        ' ╰━╰━┹╰━╯ '
    ),2, DEFAULT_OPENER),
    '/dll':TUIFIProfile((
        ' ╭━╭━┳╭━╮ \n'
        ' │D│L┠│L│ \n'
        ' │▒│█┠│▒│ \n'
        ' ╰━╰━┹╰━╯ '
    ),2, DEFAULT_OPENER),


    '/rar':TUIFIProfile((
        ' ▃▃RAR▃▃╮ \n'
        ' ▒▒░ ░▒▒┃ \n'
        ' ▓▓░ ░▓▓┃ \n'
        ' ▀▀░ ░▀▀┘ '
    ),2, DEFAULT_OPENER),
    '/zip':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' ZIP░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '/tar':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' TAR░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '/gz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' GZ▀░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '/xz':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' XZ▀░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '/bz2':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' BZ2░░▀▀▀ '
    ),2, DEFAULT_OPENER),
    '/zst':TUIFIProfile((
        ' ▃▃▃░░▃▃▃ \n'
        ' ▒▒▒░░▒▒▒ \n'
        ' ▓▓▓░░▓▓▓ \n'
        ' ZST░░▀▀▀ '
    ),2, DEFAULT_OPENER),


    '/gif':TUIFIProfile((
        ' ┍━━━┳┳┳┓ \n'
        ' │GIF:∵◖┇ \n'
        ' ┝┓░▃_▓▆┇ \n'
        ' ╰━━━┻┻┻┛ '
    ),2, DEFAULT_OPENER),


    '/torrent':TUIFIProfile((
        ' ╭──────╮ \n'
        ' │TORENT│ \n'
        ' │░▓██▓░│ \n'
        ' ╰━━━━━━╯ '
    ),5, DEFAULT_OPENER),


    '/mp4':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MP4∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/mkv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MKV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/3gp':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇3GP∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/avi':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇AVI∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/webm':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇WEBM∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/ogv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇OGV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),
    '/mov':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MOV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),2, DEFAULT_OPENER),


    '/otf':TUIFIProfile((
        '▃▃▃ ▃▃▃ ▃▃\n'
        '█ █  █  █▃\n'
        '█▃█  █  █ \n'
        '          '
     ),1, DEFAULT_OPENER),
    '/ttf':TUIFIProfile((
        '▃▃▃ ▃▃▃ ▃▃\n'
        ' █   █  █▃\n'
        ' █   █  █ \n'
        '          '
     ),1, DEFAULT_OPENER),
    '/woff':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃WOFF━┫┇ \n'
        ' ┃ ░░▓█┃┃ \n'
        ' ╰━━━━━┻┛ '
     ),1, DEFAULT_OPENER),
    '/woff2':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃WOFF2┫┇ \n'
        ' ┃ █▓░░┃┃ \n'
        ' ╰━━━━━┻┛ '
    ),1, DEFAULT_OPENER),


    '/reg':TUIFIProfile((
        ' ┏━━┳━┳━┓ \n'
        ' ┃▓█┣━╋━┫ \n'
        ' ┇REG━┻━┫ \n'
        ' ╰━━┻━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/exe':TUIFIProfile((
        ' ┏━━┳━┳━┓ \n'
        ' ┃▓█┣━╋━┫ \n'
        ' ┇EXE━┻━┫ \n'
        ' ╰━━┻━━━┛ '
    ),1, DEFAULT_OPENER),


    '/jpg':TUIFIProfile((
        ' ┏━━━JPG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/png':TUIFIProfile((
        ' ┏━━━PNG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/ico':TUIFIProfile((
        ' ┏━━━ICO╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/jpeg':TUIFIProfile((
        ' ┏━━JPEG╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/bmp':TUIFIProfile((
        ' ┏━━━BMP┓ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/webp':TUIFIProfile((
        ' ┏━━WEBP╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/tiff':TUIFIProfile((
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/tif':TUIFIProfile((
        ' ┏━━TIFF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/tga':TUIFIProfile((
        ' ┏━TARGA╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/heif':TUIFIProfile((
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/heifs':TUIFIProfile((
        ' ┏━━HEIF╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),
    '/heic':TUIFIProfile((
        ' ┏━━HEIC╮ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),2, DEFAULT_OPENER),


    '/m4a':TUIFIProfile((  # 8 = Aqua, just like the waves
        ' ┏━━━━━━╮ \n'
        ' ┇.:.M4A┫ \n'
        ' ╋┻╋┻╋┻━┇ \n'
        ' ╰━━━━━━┛ '
    ),8, DEFAULT_OPENER),
    '/mp3':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇.:.MP3┫ \n'
        ' ╋┻╋┻╋┻━┇ \n'
        ' ╰━━━━━━┛ '
    ),8, DEFAULT_OPENER),
    '/wav':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇.:.WAV┫ \n'
        ' ╋┻╋┻╋┻━┇ \n'
        ' ╰━━━━━━┛ '
    ),8, DEFAULT_OPENER),
    '/mid':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇.:.MID┫ \n'
        ' ╋┻╋┻╋┻━┇ \n'
        ' ┗━━━━━━┛ '
    ),8, DEFAULT_OPENER),
    '/aac':TUIFIProfile((
        ' ╭━━━━━━┓ \n'
        ' ┇.:.AAC┫ \n'
        ' ╋┻╋┻╋┻━┇ \n'
        ' ┗━━━━━━┛ '
    ),8, DEFAULT_OPENER),


    '/psd':TUIFIProfile((
        ' ┏▃▃▃▃▃▃┓ \n'
        ' ┃█▂█▒▃▃┃ \n'
        ' ┃█  ▃▃▒┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_OPENER),

    '/mdf':TUIFIProfile((
        ' ┏━━━━━━  \n'
        ' ┃MDF┏▄ ┇ \n'
        ' ┇█▓░┣┻▄┇ \n'
        ' ┗━━ ▀  ┛ '
    ),8, DEFAULT_EDITOR),
    '/db':TUIFIProfile((
        ' ┏━━┳━━━  \n'
        ' ┃DB┃┏▄ ┇ \n'
        ' ┇█▓░┣┻▄┇ \n'
        ' ┗━━ ▀  ┛ '
    ),8, DEFAULT_EDITOR),


    '/tuifi':TUIFIProfile((
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
    ),2),
    '/tuifi3':TUIFIProfile((
        '              .^        \n'
        '            ~GB^        \n'
        '          7B&G.         \n'
        '        !B&&J   oOo     \n'
        '      :G&&#~    oOo     \n'
        '     ?&&&G.             \n'
        '   :G&&&B7:  ^^^^^^^    \n'
        '  7#&&&&&&#7J&#&&&##G^  \n'
        '.5&&&G!!Y######J77P###? \n'
        'J&&##:   ^G##G:   .BBB#7\n'
        ' ?#&#B^    ??    ^GBBB7 \n'
        '  :G&##J        7BB#G:  \n'
        '    Y##&~     .5#BBJ    \n'
        '     ~BP.    ^GBBG^     \n'
        '  oOo       ?BBBJ       \n'
        '  oOo     .P#B5:        \n'
        '         ~B#P^          \n'
        '        JBY^            \n'
        '       .^.              \n'
        '                        '
    ),3),
    '/tuifi4':TUIFIProfile((
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⣀⣤⣤⣤⠀⢿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⢀⣾⣿⣿⣿⣿⣷⡀⠛⠿⠿⠿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⡰⠛⠀⠀⠀⠙⣿⣿⣿⣿⣿⠇⠀⠀⠘⣿⣿⣿⣶⣤⣤⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠃⠀⠀⠀⣾⣿⣿⠿⣋⣥⣤⣤⣤⣶⣶⣶⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⣼⣿⡿⠟⠀⠀⠀⢠⠾⠛⠁⣴⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠠⠶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡿⠋⠀⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠿⠿⠶⣤⣤⣤⣤⣤⣀⠈⠛⠻⠿⠿⠟⠛⠛⠉⠉⣠⣶⡿⠁⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⠇⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠀⠀⠀⠀⠀⠀⣀⣾⠁⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⠃⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣶⣾⣿⣿⣿⣿⣷⣶⣶⣄⠉⢿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠖⠒⠉⠋⠉⠉⠉⠋⠋⠉⠉⠙⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⡇⢸⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⣴⠞⠀⠀⠀⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣷⣶⣶⣿⣿⠋⣀⣤⣶⣶⡆⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡿⣡⣿⣿⣿⠟⢿⡇⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠟⢠⣿⣿⡿⠀⠀⠀⣿⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢸⣿⣿⠃⠀⠀⠀⣿⡆⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⠀⠀⠀⠀⢹⣿⣦⡀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠀⣴⣿⣷⠀⠈⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠿⢿⣿⣿⣾⣿⣿⣿⡆⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⠀⠀⠀⠀\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠁⠀⠀⠀'
    ),8)
}
DEFAULT_PROFILE   = TUIFIProfiles[':file']
LINK_SYMBOL       = '↩'  # Potential:⤶ ⤾ ↲ ⎌ ☍ ⧉
LINK_SYMBOL_COLOR = 1
