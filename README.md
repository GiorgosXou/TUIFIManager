
# TUIFI Manager

A cross-platform terminal-based file manager *(and component)*, meant to be used with a [Uni-Curses](https://github.com/unicurses/unicurses) project or as is. This project is mainly an attempt to get more attention to the [Uni-Curses](https://github.com/unicurses/unicurses) project.

## Installation
```terminal
sudo pip3 install TUIFIManager
```
or just `pip3 install TUIFIManager` if it works for you.

## Usage

Run `tuifi` in your terminal to use it or import it in one of your [Uni-Curses](https://github.com/unicurses/unicurses) project as a component like:
```
from TUIFIManager import *
```
for more details look into the `__main__.py`

<img src="/Peek.gif">
https://asciinema.org/a/gVD8T8nHCI4xaMHomwiR3m3hx

## Shortcuts & Features 
| Shortcut | Action |
|----|:----|
|SHIFT + TAB| Moves selected file to the previous directory
|CTRL + S| Goes in & out of "Select Mode" for termux |
|`KEY_BACKSPACE`| Opens\Goes to the previous directory|
|CTRL + V| Pastes the Copied or Cuted files|
|DEL| Deletes the selected files
|CTRL + C| Copies the selected files|
|CTRL + X| Cuts the selected files|
|ARROW KEYS| Navigates files|
|`KEY_ENTER`| Opens files|
|ESCAPE| Exit|

* Supports most of the common mouse events so far
* It is somewhat fully customizable
* Supports [Termux](https://github.com/termux) *(Not fully yet)*
* It is quite snappy
* Cross Platform 
* and  more

# Outro 
### Documentation and other things are coming ...  
[stackedit.io](https://stackedit.io/app) have been used for the editing of this MD file
