

<div align="center">
<h1>TUIFI Manager</h1>
<p>
    <a href="https://github.com/GiorgosXou/TUIFIManager/pulse">
      <img src="https://img.shields.io/github/last-commit/GiorgosXou/TUIFIManager?color=%4dc71f&label=Last%20Commit&logo=github&style=flat-square"/>
    </a>
    <a href="https://github.com/GiorgosXou/TUIFIManager/blob/master/LICENSE.md">
      <img src="https://img.shields.io/github/license/GiorgosXou/TUIFIManager?label=License&logo=GNU&style=flat-square"/>
	</a>
</p>
</div>

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

<img src="./Peek.gif">
<sub>https://asciinema.org/a/gVD8T8nHCI4xaMHomwiR3m3hx</sub>

## Features & Shortcuts  
### *Current:*
* Supports most of the common mouse events so far
* It is somewhat fully customizable?
* Can be used as a component
* Uses only ~30MB of RAM
* It is pretty snappy <!-- Kinda lol -->
* Supports [Termux](https://github.com/termux) 
* Cross Platform 
* and more

### *Desired:*
* Undo\Redo
* tool-tips
* Scroll bar
* Effect on cutted Files
* [Drop files into GUI apps](https://github.com/GiorgosXou/TUIFIManager/issues/21)

### *Common Shortcuts\Keybindings*
| Shortcuts   | vim_mode | Action                                        |
|----         | ---- |:----                                          |
|`SHIFT + TAB`  |   |Moves selected file to the previous directory |
|`KEY_BACKSPACE`| `J` |Opens\Goes to the previous directory          |
|`ALT + DOWN`   |   |Opens\Closes the "right-click menu"           |
|`KEY_HOME`     | `H`  |Navigates to the $HOME directory              |
|`KEY_F5`       |   |Reload\Refresh current directory              |
|`CTRL + V`     | `p` |Pastes the Copied or Cuted files              |
|`DEL`          | `CTRL+d`  |Deletes the selected files                    |
|`CTRL + F`     | `i`  |Find Files *(if not auto_find_on_typing)*     |
|`CTRL + O`     | `O`  |Open whole directory in editor                |
|`CTRL + C`     | `y`  |Copies the selected files                     |
|`CTRL + K`     |   |Copies the selected files                     |
|`CTRL + X`     | `c`  |Cuts the selected files                       |
|`CTRL + R`     | `r` |Rename selected file                          | 
|`CTRL + N`     | `W` |Create new folder                             |
|`CTRL + W`     | `w` |Create new file                               |
|`ARROW KEYS`   | `l` `k` `j` `h`  |Navigates files                               |
|`KEY_ENTER`    | `K` `o` |Opens files                                   |
|`ESCAPE`       |   |Exit                                          |

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
***How do I enable vim_mode ?***
> Set `tuifi_vim_mode` enviroment variable to `True`

***How do I map keys in vim_mode?***
> This ain't possible right now althought you could play around with the content of `toggle_vim_mode` function under `__init__.py`

***How do I set the default editor ?***
> Set `tuifi_default_editor` enviroment variable to `vim` or whatever you prefer

***How do I toggle hidden files/folders?***
> Edit `__main__.py` and specify `suffixes=['*','.*']` for hidden files. [THIS NEEDS TO BE FIXED]

***How do I change the default colors?***
> A bit complicated to explain here just make an issue and I will explain it there

<sub>[^Source](https://www.reddit.com/r/termux/comments/rsmdmc/comment/hu7t88g/?utm_source=share&utm_medium=web2x&context=3)</sub>

# Donation
I do really need money to survive, I have no job, living in a basement, making things for free, because I love to.
- [***Paypal Address***](https://www.paypal.com/donate/?hosted_button_id=QNQN23M55EJVS)
- ***Monero Address:*** `897ehhSQJQpGF7tYDhQM51jiX7nnHmzuYAW4q8JGwJxu8JKXvaK6AivCzatuJxnifjZ2qy98ks2g2PhmTaYCMMta2Ga2LJx`

<div align="center">
<img src='./TUIFI.png'>
</div>

# Help
Any Idea with this issue https://github.com/unicurses/unicurses/issues/21 ?



