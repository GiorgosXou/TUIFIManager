

# TUIFI Manager
A cross-platform terminal-based file manager *(and component)*, meant to be used with a [Uni-Curses](https://github.com/unicurses/unicurses) project or as is. This project is mainly an attempt to get more attention to the [Uni-Curses](https://github.com/unicurses/unicurses) project.

## Installation
```terminal
sudo pip3 install tuifimanager --upgrade
```
or just `pip3 install TUIFIManager --upgrade` if it works for you.

## Usage
Run `tuifi` in your terminal to use it or import it in one of your [Uni-Curses](https://github.com/unicurses/unicurses) project as a component like:
```
from TUIFIManager import *
```
for more details look into the `__main__.py`

<img src="/Peek.gif">
https://asciinema.org/a/gVD8T8nHCI4xaMHomwiR3m3hx 

## Features & Shortcuts  
### *Current:*
* Supports most of the common mouse events so far
* It is somewhat fully customizable
* Can be used as a  component
* It is pretty snappy
* Supports [Termux](https://github.com/termux) 
* Cross Platform 
* and  more

### *Desired:*
* tool-tips
* Scroll bar
* Bottom bar
* Search bar
* Dim-Effect on cutted Files

### *Common Shortcuts\Keybindings*
| Shortcut | Action |
|----|:----|
|`SHIFT + TAB`  | Moves selected file to the previous directory
|`KEY_BACKSPACE`| Opens\Goes to the previous directory|
|`ALT + DOWN`   | Opens\Closes the "right-click menu"|
|`KEY_HOME`     | Navigates to the $HOME directory|
|`CTRL + V`     | Pastes the Copied or Cuted files|
|`DEL`          | Deletes the selected files
|`CTRL + C`     | Copies the selected files|
|`CTRL + X`     | Cuts the selected files|
|`ARROW KEYS`   | Navigates files|
|`KEY_ENTER`    | Opens files|
|`ESCAPE`       | Exit|

### *TERMUX only Shortcuts\Keybindings*
| Shortcut | Action |
|----|:----|
|`CTRL + DOWN`| Goes in&out of select-mode while also automatically copies the selected file(s)|
|`CTRL + LEFT`| Goes out of select-mode while also cuts the seleccted file(s)|
|`CTRL + END` | Goes out of select-mode while also deleting the selected file(s)|
|`CTRL + UP`  | Same as `CTRL + V`, Pastes the Copied or Cuted files|
|`END`        | Deletes selected files |

# Outro 
### Documentation and other things are coming ...  
[stackedit.io](https://stackedit.io/app) have been used for the editing of this MD file
