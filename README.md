


# TUIFI Manager
A cross-platform terminal-based termux-oriented file manager *(and component)*, meant to be used with a [Uni-Curses](https://github.com/unicurses/unicurses) project or as is. This project is mainly an attempt to get more attention to the [Uni-Curses](https://github.com/unicurses/unicurses) project.

## Installation
```terminal
sudo pip3 install tuifimanager --upgrade
```
```terminal
pip3 install TUIFIManager --upgrade
```
or just ^^^ if it works for you. *(eg. on termux?)*

## Usage
Run `tuifi` in your terminal to use it as is or import it in one of your [Uni-Curses](https://github.com/unicurses/unicurses) project as a component like:
```python
from TUIFIManager import *
```
for more details look into the `__main__.py`

<img src="/Peek.gif">
https://asciinema.org/a/gVD8T8nHCI4xaMHomwiR3m3hx 

## Features & Shortcuts  
### *Current:*
* Supports most of the common mouse events so far
* It is somewhat fully customizable?
* Can be used as a component
* It is pretty snappy
* Supports [Termux](https://github.com/termux) 
* Cross Platform 
* and more

### *Desired:*
* Undo\Redo
* tool-tips
* Scroll bar
* Search bar
* Information bar <!-- possibly i'll use mvwin_wch which i need to implement on unicurses-->
* Dim-Effect on cutted Files

### *Common Shortcuts\Keybindings*
| Shortcut      | Action                                        |
|----           |:----                                          |
|`SHIFT + TAB`  | Moves selected file to the previous directory |
|`KEY_BACKSPACE`| Opens\Goes to the previous directory          |
|`ALT + DOWN`   | Opens\Closes the "right-click menu"           |
|`KEY_HOME`     | Navigates to the $HOME directory              |
|`KEY_F5`       | Reload\Refresh current directory              |
|`CTRL + V`     | Pastes the Copied or Cuted files              |
|`DEL`          | Deletes the selected files                    |
|`CTRL + C`     | Copies the selected files                     |
|`CTRL + X`     | Cuts the selected files                       |
|`CTRL + R`     | Rename selected file                          | 
|`CTRL + N`     | Create new folder                             |
|`CTRL + W`     | Create new file                               |
|`ARROW KEYS`   | Navigates files                               |
|`KEY_ENTER`    | Opens files                                   |
|`ESCAPE`       | Exit                                          |

### *TERMUX only Shortcuts\Keybindings*
| Shortcut    | Action                                                                         |
|----         |:----                                                                           |
|`CTRL + DOWN`| Goes in&out of select-mode while also automatically copies the selected file(s)|
|`CTRL + LEFT`| Goes out of select-mode while also cuts the seleccted file(s)                  |
|`CTRL + END` | Goes out of select-mode while also deleting the selected file(s)               |
|`CTRL + UP`  | Same as `CTRL + V`, Pastes the Copied or Cuted files                           |
|`END`        | Deletes selected files                                                         |

# Documentation
<sub>Work in progress 🛠️🏗 ...</sub>
## Customization 
* How do I choose which program to use for opening files?
> navigate to `python -c "import TUIFIManager;print(TUIFIManager.__path__)"` and add `xdg-open` or change `DEFAULT_EDITOR` ,by editing `TUIFIProfile.py`.

* How do I toggle hidden files/folders?
> Navigate to `__main__.py` and specify `suffixes=['*','.*']` for hidden files.

<sub>[^Source](https://www.reddit.com/r/termux/comments/rsmdmc/comment/hu7t88g/?utm_source=share&utm_medium=web2x&context=3)</sub>

# Help
Any Idea with this issue https://github.com/unicurses/unicurses/issues/21 ?
