from unicurses    import OPERATING_SYSTEM
from .TUItilities import HOME_DIR, IS_MACOS, IS_WINDOWS, init_colorscheme
from shutil       import which
from os.path      import isfile
from os           import getenv, sep


CONFIG_PATH = getenv('tuifi_config_path',f'{HOME_DIR}{sep}.config{sep}tuifi')
THEMES_PATH = getenv('tuifi_themes',f'{CONFIG_PATH}{sep}themes')
TUIFI_THEME = getenv('tuifi_theme','')
THEME_PATH  = f'{THEMES_PATH}{sep}{TUIFI_THEME}{sep}'


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



DEFAULT_OPENER = 'start' if OPERATING_SYSTEM == IS_WINDOWS else 'open' if OPERATING_SYSTEM == IS_MACOS else 'xdg-open'   # meh.. # TODO: make an enviromental variable insted of those 2 vars, for everything
DEFAULT_EDITOR = which(getenv('tuifi_default_editor', getenv('EDITOR', 'nvim'))) or which('emacs') or which('vim') or which('micro') or which('nano')  or which('vi') or DEFAULT_OPENER
DEFAULT_WITH   = DEFAULT_EDITOR

TUIFIProfiles = { # TODO: ADD gitignore and etc. icons | TODO: open zip rar and etc. files on __init__.py as if they where kind of folders?
    ':all':TUIFIProfile(( # multiple tuifiles custom (grid like)-icon for use in tuiprop
        ' ┏━━━━━┳┓ \n'
        ' ┃▀┇▀┇╋╋┫ \n'
        ' ┃▀┇┇╋╋╋┫ \n'
        ' ┗━┻┻┻┻┻┛ '
    ),4),
    ':folder':TUIFIProfile(( # TODO: change folder and empty_folder to something containing illegal characters because if someone names a hidden file that way, there will be a conflict 2022-12-19 09:16:13 PM
        ' █████▒⎫⎫ \n'
        ' █████▒▐┇ \n'
        ' █████▒▐┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),4),
    ':folder_subfolder':TUIFIProfile((
        ' █████░⎫⎫ \n'
        ' █████░▐┇ \n'
        ' █████░▐┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),4),
    ':folder_single_file':TUIFIProfile((
        ' █████░⎫⎫ \n'
        ' █████░┇┃ \n'
        ' █████░┃┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),4),
    ':empty_folder':TUIFIProfile((
        ' █████ ⎫⎫ \n'
        ' █████ ┇┇ \n'
        ' █████ ┃┃ \n'
        ' ▀▀▀▀▀  ┘ '
    ),4),
    ':file':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇┛FILE ┃ \n'  # 𝗙𝗜𝗟𝗘
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),

    '.gitmodules':TUIFIProfile((
        '          \n'
        ' ┏━━━┏▄ ┓ \n'
        ' ┇█▓░┣┻▄┇ \n'
        ' ┗━━ ▀  ┛ '
    ),3, DEFAULT_EDITOR),
    '.gitattributes':TUIFIProfile((
        '          \n'
        ' ┏ATR┏▄ ┓ \n'
        ' ┇█▓░┣┻▄┇ \n'
        ' ┗━━ ▀  ┛ '
    ),3, DEFAULT_EDITOR),
    '.gitignore':TUIFIProfile((
        '          \n'
        ' ┏━ ┏▄ ━┓ \n'
        ' ┇▓░┣┻▄ ┇ \n'
        ' ┗━ ▀  ━┛ '
    ),3, DEFAULT_EDITOR),

    '.xauthority':TUIFIProfile((
        ' ╭╴╴╸━━━╮ \n'
        ' │🭣🭕🭑🭆🭠🭘│ \n'
        ' │🭈🭄🭜🭧🭏🬽│ \n'
        ' ╰━━━╸╸╴╯ '
    ),4, DEFAULT_EDITOR),
    '.xresources':TUIFIProfile((
        ' ╭╴╴╸━━━╮ \n'
        ' │🭣🭕🭑🭆🭠🭘│ \n'
        ' │🭈🭄🭜🭧🭏🬽│ \n'
        ' ╰━━━╸╸╴╯ '
    ),4, DEFAULT_EDITOR),

    'makefile':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃█▀▅▀█┣┫ \n'
        ' ┣━MAKE┻┫ \n'
        ' ┗━┻━━┻━┛ '
    ),4, DEFAULT_EDITOR),
    '/mk':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃█▀▅▀█┣┫ \n'
        ' ┣━MAKE┻┫ \n'
        ' ┗━┻━━┻━┛ '
    ),4, DEFAULT_EDITOR),
    'config':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    'license':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┃▄▀█▀▅┇┇ \n'
        ' ┃┻▂█▂┻┃┃ \n'
        ' ┗━━━━━┻┛ '
    ),4, DEFAULT_EDITOR),

    '/cfg':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/conf':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┇CONFIG┃ \n'
        ' ┃┋┇┃┃┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/ini':TUIFIProfile((
        ' ┏┏━━━━┳┓ \n'
        ' ┃┃INIT┃┃ \n'
        ' ┃┃┇┃┃┇┃┃ \n'
        ' ┗┻━━━━┛┛ '
    ),4, DEFAULT_EDITOR),
    '/ppt':TUIFIProfile((
        ' ╭━━━━┳╮╮ \n'
        ' ┇PPTX┃├┃ \n'
        ' ┃[▒▒]┃├┇ \n'
        ' ╰━━━━┻━╯ '
    ),5, DEFAULT_OPENER),
    '/pptx':TUIFIProfile((
        ' ╭━━━━┳╮╮ \n'
        ' ┇PPTX┃├┃ \n'
        ' ┃[▒▒]┃├┇ \n'
        ' ╰━━━━┻━╯ '
    ),5, DEFAULT_OPENER),
    '/xlsx':TUIFIProfile((
        ' ┏━━━━┳┳┓ \n'
        ' ┃██▓░┣╋┫ \n'
        ' ┃EXCEL╋┫ \n'
        ' ╰━━━━┻┻┛ '
    ),7, DEFAULT_OPENER),
    '/csv':TUIFIProfile((
        ' ┏━━━┳┳┳┓ \n'
        ' ┃█▓░┣╋╋┫ \n'
        ' ┃CSV┣╋╋┫ \n'
        ' ╰━━━┻┻┻┛ '
    ),3, DEFAULT_EDITOR),

    '/ino':TUIFIProfile((
        ' ┏┳┳┳━━━╮ \n'
        ' ┇ARDINO┃ \n'
        ' ┃━ ┗┛+┓┃ \n'
        ' ╰┻━━┻┻┻┛ '
    ),6, DEFAULT_EDITOR),
    '/o':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀█ ┃ \n'
        ' ┃ █▄▄█ ┃ \n'
        ' ┗━━━━━━┛ '
    ),3, DEFAULT_OPENER),
    '/out':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀█ ┇ \n'
        ' ┇ █▄▄█ ┇ \n'
        ' ┗━━━━━━┛ '
    ),3, DEFAULT_OPENER),
    '/h':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▂▂█ ┃ \n'
        ' ┃ █▔▔█ ┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/c':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇ █▀▀▀ ┃ \n'
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/cc':TUIFIProfile((
        ' ┏━━━cpp┓ \n'
        ' ┇ █▀▀▀ ┃ \n'
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/cpp':TUIFIProfile((
        ' ┏━━━cpp┓ \n'
        ' ┇ █▀▀▀ ┃ \n'
        ' ┃ █▄▄▄ ┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/toml':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┃░░┃┃░░┃ \n' 
        ' ┃░░┇┃░░┃ \n'
        ' ┗━━ ┛━━┛ '
    ),5, DEFAULT_EDITOR),
    '/js':TUIFIProfile((
        ' ┌━━━━━━┐ \n'
        ' │▀█▀▒▀▀│ \n'
        ' │▃█ ▃▃▓│ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/ts':TUIFIProfile((
        ' ┌━━━━━━┐ \n'
        ' │▀█▀▒▀▀│ \n'
        ' │ █ ▃▃▓│ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/html':TUIFIProfile((
        ' ┌┳━━━━┳┐ \n'
        ' ├┨HTML┠┤ \n'
        ' │┇</.>┇│ \n'
        ' ╰━━━━━━╯ '
    ),5, DEFAULT_EDITOR),
    '/xml':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┇┨<>XML┇ \n'
        ' ┃┠─<//>┨ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),

    '/vb':TUIFIProfile((
        ' ▃ ▃ ▃▃   \n'
        ' █ █ █▃█  \n'
        ' ▀▃▀ █▃▀┇ \n'
        '     ━━━┛ '
    ),6, DEFAULT_EDITOR),
    '/vbs':TUIFIProfile((
        '▃ ▃ ▃▃  ▃▃\n'
        '█ █ █▃█ █▃\n'
        '▀▃▀ █▃▀ ▃█\n'
        '          '
    ),6, DEFAULT_EDITOR),
    '/apk':TUIFIProfile((
        ' ┏▅▅▅▅▅▅┓ \n'    # ' ▃  ▃▃ ▃ ▃\n'
        ' ┇┏┓┏┓┒┒┇ \n'    # '█▃█ ██ █▃▀\n'
        ' ┃┣┫┣┛┣┓┃ \n'    # '█ █ █  █ █\n'
        ' ┗━━━━━━┛ '      # '          '
    ),7, DEFAULT_OPENER),
    '/php':TUIFIProfile((
        ' ╭──────╮ \n'
        ' │┏┓┇┇┏┓│ \n'
        ' │┣┛┣┫┣┛│ \n'
        ' ╰━━━━━━╯ '
    ),6, DEFAULT_EDITOR),
    '/bas':TUIFIProfile(( # is Giving me 60-70s Hippie vibes font (a wider version could be better?) 
        ' ╭┏┓┏┓┏┓╮ \n'
        ' │┃┫┣┫┗┓│ \n'
        ' │BAS┇┇┃│ \n'
        ' ╰┗┛╹╹┗┛╯ '
    ),8, DEFAULT_EDITOR),
    '/asm':TUIFIProfile((
        ' ┏┏┓┏┓┓┓┓ \n'
        ' ┇┣┫┗┓┃┇┃ \n'
        ' ┃┃┃┇┃ASM \n'
        ' ┗┻┻┗┛╹╹╹ '
    ),8, DEFAULT_EDITOR),
    '/s':TUIFIProfile((
        ' ┏┏┓┏┓┓┓┓ \n'
        ' ┇┣┫┗┓┃┇┃ \n'
        ' ┃┃┃┇┃ASM \n'
        ' ┗┻┻┗┛╹╹╹ '
    ),8, DEFAULT_EDITOR),
    '/a86':TUIFIProfile((
        ' ┏┏┓┏┓┏┓┓ \n'
        ' ┇┣┫┣┫┣┓┃ \n'
        ' ┃┃┃┃┇A86 \n'
        ' ┗╹╹┗┛┗┛┛ '
    ),8, DEFAULT_EDITOR),
    '/adb':TUIFIProfile((
        ' ┏━━━┏━━┓ \n'
        ' ┇┏┓┏┇┏┓┇ \n'
        ' ┃┣┫┇┛┣┫┃ \n'
        ' ┗━━┛━━━┛ '
    ),6, DEFAULT_EDITOR),
    '/ads':TUIFIProfile((
        ' ┏━━━┏━━┓ \n'
        ' ┇┏┓┏┇┏┓┇ \n'
        ' ┃┣┫┇┛DS┃ \n'
        ' ┗━━┛━━━┛ '
    ),8, DEFAULT_EDITOR),
    '/lisp':TUIFIProfile((
        ' ╭┳━┳━━┓╮ \n'
        ' │┣━┛┏━┓│ \n'
        ' │┗━┛┏━┫│ \n'
        ' ╰┗━━┻━┻╯ '
    ),3, DEFAULT_EDITOR),
    '/vim':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃VI━━━┫┇ \n'
        ' ┃█▀▅▀▄┃┃ \n'
        ' ╰━━━━━┻┛ '
    ),7, DEFAULT_EDITOR),
    '/md':TUIFIProfile((
        ' ┏━━━━━┓┓ \n'
        ' ┃█▀▅▀▄┃┇ \n'
        ' ┃DOWN━┫┫ \n'
        ' ╰━━━━━┻┛ '
    ),6, DEFAULT_EDITOR),

    '/json':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┏┇┏┏┓┓┃ \n'
        ' ┃┇┛JSON┃ \n'
        ' ┗━━━━┛━┛ '
    ),3, DEFAULT_EDITOR),
    '/yaml':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┏┇YAML┃ \n'
        ' ┃┇┛┗┗┛┛┃ \n'
        ' ┗━━━━┛━┛ '
    ),3, DEFAULT_EDITOR),
    '/yml':TUIFIProfile((
        ' ┏━━━━┓━┓ \n'
        ' ┃┇┓YAML┃ \n'
        ' ┃┗┇┗┗┛┛┃ \n'
        ' ┗━━━━┛━┛ '
    ),3, DEFAULT_EDITOR),

    '/lua':TUIFIProfile((
        '▃  ▃ ▃ ▃▃▃\n'
        '█  █ █ █▃█\n'
        '█▃▖█▃█ █ █\n'
        '          '
    ),6, DEFAULT_EDITOR),
    '/java':TUIFIProfile((
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '
    ),5, DEFAULT_EDITOR),
    '/jar':TUIFIProfile((
        '    Šƨ    \n'
        '  ⊏█▇▇█   \n'
        ' ▗▃▃▃▃▃▃▖ \n'
        '  ▔▔▔▔▔▔  '
    ),3, DEFAULT_EDITOR),
    '/cs':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' │ █▀▀▀ │ \n'
        ' │ █▄▄▄ │ \n'
        ' ┕━━━━━━╯ '
    ),7, DEFAULT_EDITOR),
    '/fs':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' │ █▀▀▀ │ \n'
        ' │ █▀▀ #│ \n'
        ' ┕━━━━━━╯ '
    ),6, DEFAULT_EDITOR),
    '/go':TUIFIProfile((
        ' ┏━━━━━━╮ \n'
        ' ┇█▀▀▒▀█│ \n'
        ' ┃█▃█▓▃█│ \n'
        ' ┗━━━━━━╯ ' 
    ),6, DEFAULT_EDITOR),
    '/rs':TUIFIProfile((
        ' ▃▃▃▃▃▃🬽╮ \n'
        ' ▃█🭑▃▃🭆🭞│ \n'
        ' ▃█▃🬽🭥🭓▄🭞 \n'
        ' ╰━━━━━━╯ '
    ),5, DEFAULT_EDITOR),
    '/py':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒·   █▒ \n'
        '          '
    ),4, DEFAULT_EDITOR),
    '/pyc':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒.101█▒ \n'
        '          '
    ),3, DEFAULT_EDITOR),
    '/pyw':TUIFIProfile((
        ' ▃▃▃ ▃ ▃. \n'
        ' █▃█▒█▃█▒ \n'
        ' █▒.wW.█▒ \n'
        '          '
    ),3, DEFAULT_EDITOR),
    '/tex':TUIFIProfile((
        ' ┏┏┏┏━━━┓ \n'
        ' ┃┃┏┓┳┏━┃ \n'
        ' ┃┇┣┫┃EX┃ \n'
        ' ┗━━━━━━┛ '
    ),3, DEFAULT_EDITOR),
    '/txt':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┏┇┃EΞ┃┇ \n'
        ' ┃┇┛┃ΞE┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),3, DEFAULT_EDITOR),
    '/log':TUIFIProfile((
        ' ┏━━┓┓┓┓┓ \n'
        ' ┃┋┇┃ΞE┃┇ \n'
        ' ┃┇┋┃EΞ┃┃ \n'
        ' ┗━━┛━━┛┛ '
    ),3, DEFAULT_EDITOR),
    '/qml':TUIFIProfile((
        ' ╭━━┯━━━┑ \n'
        ' ┝┳━┥QML│ \n'
        ' ┝┻━┷━━━┥ \n'
        ' ┕━━━━━━╯ '
    ),7, DEFAULT_EDITOR),
    '/css':TUIFIProfile((
        ' ┏┳━┳┓┑┑┑ \n'
        ' ┣┇▓┇┫▅▅│ \n'
        ' ┣┇▒┇┫ΞΞ│ \n'
        ' ┗┻━┻┛━━╯ '
   ),8, DEFAULT_EDITOR),
    '/scss':TUIFIProfile((
        ' ┏┳━┳┓┑┑┑ \n'
        ' ┣┇▓┇┫▅▅│ \n'
        ' ┣┇▒┇┫ΞΞ│ \n'
        ' ┗┻━┻┛━━╯ '
   ),8, DEFAULT_EDITOR),
    '/pdf':TUIFIProfile((
        ' ╭━━━━╮━╮ \n'
        ' │PDF┃==│ \n'
        ' │┇▒▓┃▒▒│ \n'
        ' ╰━━━━━━╯ '
    ),5, DEFAULT_OPENER),


    '/stl':TUIFIProfile((
        ' ╭─╭┰─╮─╮ \n'
        ' │╭╰┸─╯╮│ \n'
        ' │╰.STL╯│ \n'
        ' ╰━━━━━━╯ '
    ),6, DEFAULT_OPENER),
    '/gcode':TUIFIProfile((
        ' ╭─╭─┰╮─┒ \n'
        ' │[╰┬┸╯]┇ \n'
        ' │GCODE:┃ \n'
        ' ╰━━━━━━┛ '
    ),3, DEFAULT_OPENER),
    '/fcstd':TUIFIProfile((
        ' ┏━━━━━━┓ \n'
        ' ┃░█▀▀/:┃ \n'
        ' ┃░█▀CAD┇ \n'
        ' ┗━━━━━━┛ '
    ),5, DEFAULT_EDITOR),
    '/fcstd1':TUIFIProfile((
        ' ╭────━━┓ \n'
        ' │░█▀▀RE┫ \n'
        ' │░█▀STO┇ \n'
        ' ╰━━━━━━┛ '
    ),3, DEFAULT_EDITOR),

    '/img':TUIFIProfile((
        ' ┏•┓┓┓┏┓┓ \n'
        ' ┃▒┃┃┃┃┓┇ \n'
        ' ┃IMG┻╋┫┫ \n'
        ' ┗┻━┻┻┗┛┛ '
    ),8, DEFAULT_OPENER),

    '/lock':TUIFIProfile((
        ' ┏┏━━━━┓┓ \n'
        ' ┣┗━┏┓━┛┫ \n'
        ' ┃┋┇┗┛┇┋┃ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_EDITOR),
    '/bin':TUIFIProfile((
        ' ┏━━━┳━━┓ \n'
        ' ┃┏┓┓┃┇┇┃ \n'
        ' ┃┗┛┻┃┇┇┃ \n'
        ' ┗━━━┻━━┛ '
    ),3, DEFAULT_OPENER),
    '/sh':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ $_   ┃ \n'
        ' ┇ BASH ┇ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/cmd':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\\> ┃ \n'
        ' ┇ CMD_ ┇ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/bat':TUIFIProfile((
        ' ╭━━━━━━╮ \n'
        ' ┃ C:\\> ┃ \n'
        ' ┇ BAT_ ┇ \n'
        ' ╰━━━━━━╯ '
    ),4, DEFAULT_EDITOR),
    '/so':TUIFIProfile((
        ' ╭━╭━┳╭━╮ \n'
        ' │S│O┠│Ξ│ \n'
        ' │▒│█┠│▒│ \n'
        ' ╰━╰━┹╰━╯ '
    ),4, DEFAULT_OPENER),
    '/dll':TUIFIProfile((
        ' ╭━╭━┳╭━╮ \n'
        ' │D│L┠│L│ \n'
        ' │▒│█┠│▒│ \n'
        ' ╰━╰━┹╰━╯ '
    ),4, DEFAULT_OPENER),
    '/dylib':TUIFIProfile((
        ' ╭━╭━┳╭━╮ \n'
        ' │D│Y┠│L│ \n'
        ' │▒│█┠│▒│ \n'
        ' ╰━╰━┹╰━╯ '
    ),4, DEFAULT_OPENER),


    '/rar':TUIFIProfile((
        ' ▃▃RAR▃▃┓ \n'
        ' ▒▒░ ░▒▒┃ \n'
        ' ▓▓░ ░▓▓┃ \n'
        ' ▀▀───▀▀┛ '
    ),4, DEFAULT_OPENER),
    '/7z':TUIFIProfile((
        ' ────┒▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' 7Z ┗┃─── '
    ),4, DEFAULT_OPENER),
    '/zip':TUIFIProfile((
        ' ▃▃▃┃┓▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' ZIP┗┃▀▀▀ '
    ),4, DEFAULT_OPENER),
    '/tar':TUIFIProfile((
        ' ▃▃▃┏┓▃▃▃ \n'
        ' ▒▒▒┣┫▒▒▒ \n'
        ' ▓▓▓┣┫▓▓▓ \n'
        ' TAR┗┛▀▀▀ '
    ),4, DEFAULT_OPENER),
    '/gz':TUIFIProfile((
        ' ▃▃▃┏┓▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' GZ▀┗┛▀▀▀ '
    ),4, DEFAULT_OPENER),
    '/xz':TUIFIProfile((
        ' ▃▃▃┏┓▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' XZ▀┗┛▀▀▀ '
    ),4, DEFAULT_OPENER),
    '/bz2':TUIFIProfile((
        ' ▃▃▃┏┓▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' BZ2┗┛▀▀▀ '
    ),4, DEFAULT_OPENER),
    '/zst':TUIFIProfile((
        ' ▃▃▃┏┓▃▃▃ \n'
        ' ▒▒▒┃┃▒▒▒ \n'
        ' ▓▓▓┃┃▓▓▓ \n'
        ' ZST┗┛▀▀▀ '
    ),4, DEFAULT_OPENER),


    '/gif':TUIFIProfile((
        ' ┍━━━┳┳┳┓ \n'
        ' │GIF:∵◖┇ \n'
        ' ┝┓░▃_▓▆┇ \n'
        ' ╰━━━┻┻┻┛ '
    ),4, DEFAULT_OPENER),


    '/hex':TUIFIProfile((
        ' ┌┏━┓───┐ \n'
        ' │┃Ξ┃HEX│ \n'
        ' │┃┇┇░▓█│ \n'
        ' └┗━┛───┘ '
    ),8, DEFAULT_EDITOR),


    '/crt':TUIFIProfile((
        ' ┌─┏━┓──┐ \n'
        ' │C┃E┃RT│ \n'
        ' │I┃┇┇1C│ \n'
        ' └─┗━┛──┘ '
    ),8, DEFAULT_EDITOR),
    '/cert':TUIFIProfile((
        ' ┌─┏━┓──┐ \n'
        ' │C┃E┃RT│ \n'
        ' │I┃┇┇1C│ \n'
        ' └─┗━┛──┘ '
    ),8, DEFAULT_EDITOR),
    '/cer':TUIFIProfile((
        ' ┌─┏━┓──┐ \n'
        ' │C┃E┃RT│ \n'
        ' │I┃┇┇1C│ \n'
        ' └─┗━┛──┘ '
    ),8, DEFAULT_EDITOR),
    '/p12':TUIFIProfile((
        ' ┌─┏━┓──┐ \n'
        ' │C┃E┃RT│ \n'
        ' │P┃┇┇12│ \n'
        ' └─┗━┛──┘ '
    ),8, DEFAULT_EDITOR),
    '/pem':TUIFIProfile((
        ' ┌─┏━┓──┐ \n'
        ' │C┃E┃RT│ \n'
        ' │P┃┇┇EM│ \n'
        ' └─┗━┛──┘ '
    ),8, DEFAULT_EDITOR),


    '/torrent':TUIFIProfile((
        ' ╭──────╮ \n'
        ' │TORENT│ \n'
        ' │░▓██▓░│ \n'
        ' ╰━━━━━━╯ '
    ),7, DEFAULT_OPENER),


    '/desktop':TUIFIProfile((
        ' ╭──────╮ \n'
        ' │.:||[]│ \n'
        ' │[][][]│ \n'
        ' ╰━━━━━━╯ '
    ),3, DEFAULT_OPENER),

    '/appimage':TUIFIProfile((
        ' ╭─────┰╮ \n'
        ' │APP┇╋╋┥ \n'
        ' │▀┇┇╋╋╋┥ \n'
        ' ╰━┻┻┻┻┻╯ '
    ),3, DEFAULT_OPENER),


    '/mp4':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MP4∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/mkv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MKV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/3gp':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇3GP∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/avi':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇AVI∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/webm':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇WEBM∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/ogv':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇OGV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),
    '/mov':TUIFIProfile((
        ' ┏┳┳┳┳┳┳┓ \n'
        ' ┇MOV∴∵◖┇ \n'
        ' ┇_░▃_▓▆┇ \n'
        ' ┗┻┻┻┻┻┻┛ '
    ),4, DEFAULT_OPENER),


    '/otf':TUIFIProfile((
        '▃▃▃ ▃▃▃ ▃▃\n'
        '█ █  █  █▃\n'
        '█▃█  █  █ \n'
        '          '
    ),3, DEFAULT_OPENER),
    '/ttf':TUIFIProfile((
        '▃▃▃ ▃▃▃ ▃▃\n'
        ' █   █  █▃\n'
        ' █   █  █ \n'
        '          '
    ),3, DEFAULT_OPENER),
    '/woff':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃WOFF━┫┇ \n'
        ' ┃ ░░▓█┃┃ \n'
        ' ╰━━━━━┻┛ '
    ),3, DEFAULT_OPENER),
    '/woff2':TUIFIProfile((
        ' ┏━━━━━┳┓ \n'
        ' ┃WOFF2┫┇ \n'
        ' ┃ █▓░░┃┃ \n'
        ' ╰━━━━━┻┛ '
    ),3, DEFAULT_OPENER),


    '/reg':TUIFIProfile((
        ' ┏━━┳━┳━┓ \n'
        ' ┃▓█┣━╋━┫ \n'
        ' ┇REG━┻━┫ \n'
        ' ╰━━┻━━━┛ '
    ),6, DEFAULT_EDITOR),
    '/exe':TUIFIProfile((
        ' ┏━━┳━┳━┓ \n'
        ' ┃▓█┣━╋━┫ \n'
        ' ┇EXE━┻━┫ \n'
        ' ╰━━┻━━━┛ '
    ),3, DEFAULT_OPENER),


    '/jpg':TUIFIProfile((
        ' ┍━━━JPG╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/png':TUIFIProfile((
        ' ┍━━━PNG╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/ico':TUIFIProfile((
        ' ┍━━━ICO╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/jpeg':TUIFIProfile((
        ' ┍━━JPEG╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/bmp':TUIFIProfile((
        ' ┏━━━BMP┓ \n'
        ' ┇*.∴:∵◖┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/webp':TUIFIProfile((
        ' ┍━━WEBP╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/tiff':TUIFIProfile((
        ' ┍━━TIFF╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/tif':TUIFIProfile((
        ' ┍━━TIFF╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/tga':TUIFIProfile((
        ' ┍━TARGA╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/heif':TUIFIProfile((
        ' ┍━━HEIF╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/heifs':TUIFIProfile((
        ' ┍━━HEIF╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),
    '/heic':TUIFIProfile((
        ' ┍━━HEIC╮ \n'
        ' │*.∴:∵◖┃ \n'
        ' ┝┓░▃┏▓▆┇ \n'
        ' ╰━━━━━━┛ '
    ),4, DEFAULT_OPENER),


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
        ' ┏━━━━━━┓ \n'
        ' ┇PHSHOP┃ \n'
        ' ┣┓░▃┏▓▆┇ \n'
        ' ┗━━━━━━┛ '
    ),6, DEFAULT_OPENER),
    '/raw':TUIFIProfile(( # this gives me an-essence\vides of an old "raw"-filmstrip company's logo... it gives me XYZ-file-extension-vibes too...
        ' ┏┓▄┏━━━┓ \n'
        ' ┇┇▓┇RAW┃ \n'
        ' ┃┇░┇┏━━┫ \n'
        ' ┗━•━┛━━┛ '
    ),3, DEFAULT_OPENER),
    '/svg':TUIFIProfile(( # ... Aahh.. it feels nice for svg too (until I find a better one because those 2 might be in a same photoshop-path and then feel strange on the eye)
        ' ┏┓▄┏━━━┓ \n'
        ' ┇┇▓┇SVG┃ \n'
        ' ┃┇░┇┏━━┫ \n'
        ' ┗━•━┛━━┛ '
    ),3, DEFAULT_OPENER),


    '/sqlite3':TUIFIProfile((
        ' ┏━━━━━━  \n'
        ' ┃SQL┏▄ ┇ \n'
        ' ┇█▓░┣┻▄┃ \n'
        ' ┗━━ ▀ ━┛ '
    ),8, DEFAULT_EDITOR),
    '/mdf':TUIFIProfile((
        ' ┏━━━━━━  \n'
        ' ┃MDF┏▄ ┇ \n'
        ' ┇█▓░┣┻▄┃ \n'
        ' ┗━━ ▀ ━┛ '
    ),8, DEFAULT_EDITOR),
    '/db':TUIFIProfile((
        ' ┏━━┳━━━  \n'
        ' ┃DB┇┏▄ ┇ \n'
        ' ┇▓░ ┣┻▄┃ \n'
        ' ┗━━ ▀ ━┛ '
    ),8, DEFAULT_EDITOR),
    '/kch':TUIFIProfile(( # NOTE: Profiles of NoSQL databases seems intuative to be flipped
        '  ━━━━━━┓ \n'
        ' ┇ ▄┓KCH┃ \n'
        ' ┃▄┻┫░▓█┇ \n'
        ' ┗━ ▀ ━━┛ '
    ),8, DEFAULT_EDITOR),
    '/kct':TUIFIProfile(( # B+Tree
        '  ━━━━━━┓ \n'
        ' ┇ ▄┓B+T┃ \n'
        ' ┃▄┻┫░▓█┇ \n'
        ' ┗━ ▀ ━━┛ '
    ),8, DEFAULT_EDITOR),
    '/tkh':TUIFIProfile((
        '  ━━━━━━┓ \n'
        ' ┇ ▄┓KCH┃ \n'
        ' ┃▄┻┫░▓█┇ \n'
        ' ┗━ ▀ ━━┛ '
    ),8, DEFAULT_EDITOR),
    '/tkt':TUIFIProfile(( # B+Tree
        '  ━━━━━━┓ \n'
        ' ┇ ▄┓B+T┃ \n'
        ' ┃▄┻┫░▓█┇ \n'
        ' ┗━ ▀ ━━┛ '
    ),8, DEFAULT_EDITOR),
    '/gdbm':TUIFIProfile((
        '  ━━━━━━┓ \n'
        ' ┇ ▄┓GDB┃ \n'
        ' ┃▄┻┫░▓█┇ \n'
        ' ┗━ ▀ ━━┛ '
    ),8, DEFAULT_EDITOR),


    '/car':TUIFIProfile((
        ' ┏━━━┓━━┓ \n'
        ' ┇CAR┇▄┇┇ \n'
        ' ━ ━ ━┫┇┇ \n'
        ' ┗━━━ ▀ ┛ '
    ),5, DEFAULT_EDITOR),



    '/tuifi':TUIFIProfile((
        '             \\                                      [            \n'
        '              @                 ⟡                  ╢             \n'
        '      /       ╣▒                                  ]▒       \\     \n'
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
    ),4, DEFAULT_EDITOR),
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
    ),5, DEFAULT_EDITOR),
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
    ),8, DEFAULT_EDITOR)
}
DEFAULT_PROFILE   = TUIFIProfiles[':file']
LINK_SYMBOL       = '↩'  # Potential:⤶ ⤾ ↲ ⎌ ☍ ⧉
LINK_SYMBOL_COLOR = 3


def setup_profiles():
    if not isfile(f'{THEME_PATH}PROFILES'):return
    with open(f'{THEME_PATH}PROFILES', 'r', encoding="utf-8") as file:
        line = ''
        icon = ''
        pair = None
        call = ''
        name = ''
        tmpp = None
        for block_line in file:
            if not block_line.strip() == '{': continue # Start of a block
            while True:
                line = next(file)
                if line.startswith('name:'):
                    name = line[5:-1]
                    continue
                elif line.startswith('call:'):
                    call = line[5:-1]
                    if   call == 'DEFAULT_EDITOR': call = DEFAULT_EDITOR
                    elif call == 'DEFAULT_OPENER': call = DEFAULT_OPENER
                    continue
                elif line.startswith('pair:'):
                    pair = line[5:-1]
                    continue
                elif line.startswith('icon:'):
                    while True:
                        line = next(file)
                        if line.strip() == '}':break
                        icon += line
                    icon = icon[:-1]
                    break
                if line.strip() == '}':break
            if pair and call and icon:
                TUIFIProfiles[name] = TUIFIProfile(icon, int(pair), call)
            else: # Override existing profile
                tmpp = TUIFIProfiles[name]
                if pair: tmpp.color_map = int(pair)
                if icon: tmpp.text      = icon
                if call: tmpp.open_with = call
            icon = ''
            pair = None
            call = ''
            name = ''
            #TODO: setter getter to profile text


def load_theme():
    if not TUIFI_THEME: return
    init_colorscheme(f'{THEME_PATH}COLORS.csv')                    # Check if COLORS exist to init else ...
    init_colorscheme(f'{THEME_PATH}LIGHT_COLORS.csv', light=True) # Check if LIGHT_COLORS exist instead
    setup_profiles()


