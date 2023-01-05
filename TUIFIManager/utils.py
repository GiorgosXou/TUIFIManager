import os
import shutil
import subprocess

import unicurses


STTY_EXISTS    = shutil.which('stty')
IS_WINDOWS     = unicurses.OPERATING_SYSTEM == 'Windows'
HOME_DIR       = os.getenv('UserProfile') if IS_WINDOWS else os.getenv('HOME')
CONFIG_PATH    = os.getenv('tuifi_config_path', f'{HOME_DIR}{os.sep}.config{os.sep}tuifi')
IS_TERMUX      = 'com.termux' in HOME_DIR

UP             = -1
DOWN           =  1

BEGIN_MOUSE = "\033[?1003h"
END_MOUSE   = "\033[?1003l"


def stty_a(key=None):  # whatever [...]
    if not STTY_EXISTS:
        return None

    if not key:
        return [s.strip() for s in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';')[4:-3]] # risky? i've no idea.. thats why i've not done the same when "if key:"

    for sig in subprocess.Popen("stty -a", shell=True, stdout=subprocess.PIPE).stdout.read().decode().split(';'):
        if sig.endswith(key):
            return sig.split('=')[0].strip()
    return None
