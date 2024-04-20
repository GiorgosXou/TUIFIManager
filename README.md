

<div align="center">
<h1>TUIFI Manager</h1>
<p>
    <a href="https://github.com/GiorgosXou/TUIFIManager/pulse">
      <img src="https://img.shields.io/github/last-commit/GiorgosXou/TUIFIManager?color=%4dc71f&label=Last%20Commit&logo=github&style=flat-square"/>
    </a>
    <a href="https://github.com/GiorgosXou/TUIFIManager/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/GiorgosXou/TUIFIManager?label=License&logo=GNU&style=flat-square"/>
	</a>
</p>
</div>

A cross-platform terminal-based termux-oriented file manager *(and component)*, meant to be used with a [Uni-Curses](https://github.com/unicurses/unicurses) project or as is. This project is mainly an attempt to get more attention to the [Uni-Curses](https://github.com/unicurses/unicurses) project. 

##
<div align="center">
<p>
<img src="./Peek.gif">
</p>
<p>
<sub>FONT: Cartograph CF</sub>
</p>
</div>


# ⚙️ Installation
```terminal
sudo pip3 install tuifimanager --upgrade
```
```terminal
pip3 install TUIFIManager --upgrade
```
or just ^^^ if it works for you. *(eg. on termux?)*


# 💥 Usage
Run `tuifi` in your terminal to use it as is or import it in one of your [Uni-Curses](https://github.com/unicurses/unicurses) project as a component like:
```python
from TUIFIManager import *
```
for more details look into the `__main__.py`


# 📦 Features 
### • 📌 *Current:*
- [Supports X11 Drag&Drop from terminals](#-customization 'set `tuifi_synth_dnd` enviroment variable to `True`. `pip install pynput PySide6 python-xlib`...')
- Supports most common mouse events 
- Can be used as a component
- Uses about [~30MB](## '80mb with synthetic xdnd') of RAM
- Strong [C TUI backend](https://github.com/unicurses/unicurses 'Via Uni-Curses, a NCurses\\PDCurses wrapper')
- It is pretty snappy <!-- Kinda lol -->
- Supports [Termux](https://github.com/termux) 
- Cross Platform 
- and more

### • 🔮 *Desired:*
- Macros
- [Treeview](## 'Via a `WindowPad`')
- Undo\Redo
- Improved UI
- Multiple tabs
- [Sixel support](https://github.com/GiorgosXou/TUIFIManager/issues/86#issuecomment-2016846146)
- Effect on cutted Files
- Multithread performance

# ⌨️ Keybindings
In `vim_mode` both normal and vim shortcuts work 
| Normal      | vim_mode | Action                                        |
|----         | ---- |----                                          |
|`SHIFT + TAB`  |   |Moves selected file to the previous directory |
|`KEY_BACKSPACE`| `J` |Opens\Goes to the previous directory          |
|`ALT + DOWN`   |   |Opens\Closes the "right-click menu"           |
|`KEY_HOME`     | `H`  |Navigates to the $HOME directory              |
|`KEY_F5`       |   |Reload\Refresh current directory              |
|`KEY_F3`       | `o`  |(descending) order-type switch|
|`KEY_F1`       | `O`  |(ascending) order-type switch|
|`CTRL + V`     | `p` |Pastes the Copied or Cuted files              |
|`DEL`          | `CTRL+d`  |Deletes the selected files                    |
|`CTRL + F`     | `i`  |Find Files *(if not auto_find_on_typing)*     |
|`CTRL + O`     |   |Open whole directory in editor                |
|`CTRL + A`     |  |Select all files in current folder|
|`CTRL + C`     | `yy`  |Copies the selected files                     |
|`CTRL + K`     |   |Copies the selected files                     |
|`CTRL + X`     | `c`  |Cuts the selected files                       |
|`CTRL + R`     | `r` |Rename selected file                          | 
|`CTRL + T`     | | Toggle hidden files|
|`CTRL + N`     | `W` |Create new folder                             |
|`CTRL + W`     | `w` |Create new file                               |
|`ARROW KEYS`   | `l` `k` `j` `h`  |Navigates files                               |
|`KEY_ENTER`    | `K`|Opens files                                   |
|`CTRL + E`     | `e` |Exit with `cd`                                  |
|`ESCAPE`       |   |Exit                                          |

**(*TIP:** 🐁 use `ALT + CLICK` for multiple mouse selection if `SHIFT` not working)*

***TERMUX only Shortcuts\Keybindings***
| Shortcut    | Action                                                                         |
|----         |:----                                                                           |
|`CTRL + DOWN`| Goes in&out of select-mode while also automatically copies the selected file(s)|
|`CTRL + LEFT`| Goes out of select-mode while also cuts the seleccted file(s)                  |
|`CTRL + END` | Goes out of select-mode while also deleting the selected file(s)               |
|`CTRL + UP`  | Same as `CTRL + V`, Pastes the Copied or Cuted files                           |
|`END`        | Deletes selected files                                                         |


# 👨‍💻 Commands
**(Default & Custom Comands)** - To perform a command under the normal-mode, you first have to press the space-bar and then type the command. Alternatively, use `vim_mode` or enable the `tuifi_auto_command_on_typing` env-variable *(notice: it disables `tuifi_auto_find_on_typing`)*. **The default commands can be seen below and can be found under the `~/.config/tuifi/cmds.conf` where you can add your custom ones too:**

| Cmd | Type | Attributes | Label Information|
|---|---|---|---|
|`gt` | open | 'directory':'~/.config/tuifi'           | - tuifi -|
|`gh` | open | 'directory':'~/'                        | - Home -|
|`owv` | open | 'directory':None,'\_with':'vim'         |Opened With Vim|
|`yat` | copy | 'pattern':'.+\.txt'                     ||
|`yy` | copy | 'pattern':None                          ||

**Available Type-keywords:** `open`, `copy`, `cut`, [`find`](## 'Attributes: `filename`')

**important note:** `o` is also used for ordering in `vim_mode`. In this case you can first press space-bar before proceeding with `owv` or with any other already reserved starting key, or just change it. 

**Additionally** there are also some "static" ones like the `m`+character which marks the current directory into the character, so you can navigate back to it by using \` or `;`+that_character 



# 📜 Documentation
<sub>Work in progress 🛠️🏗 ...</sub>


# 💭 Customization 
<details>
<summary><i>How do I enable vim_mode?</i></summary>

> Set `tuifi_vim_mode` enviroment variable to `True`

</details>
<details>
<summary><i>How do I enable synthetic XDND?</i></summary>

> set `tuifi_synth_dnd` enviroment variable to `True`. `pip install pynput PySide6 python-xlib`. Know it's expirimental! You'll need to adapt to it slightly, **use it as: Drag&drop + click afterwords where you want the file to be dropped.** [See also](https://github.com/GiorgosXou/TUIFIManager/discussions/92) and [this issue](https://github.com/GiorgosXou/TUIFIManager/issues/21)

</details>
<details>
<summary><i>How do I set the default editor?</i></summary>

> Set `tuifi_default_editor` enviroment variable to `vim` or whatever you prefer

</details>
<details>
<summary><i>How do I disable the auto-find-mode?</i></summary>

> You can just set `tuifi_auto_find_on_typing` enviroment variable to `False`

</details>
<details>
<summary><i>How do I change the scroll sensitivity?</i></summary>

> You can set either or both `tuifi_scroll_sensitivity`, `tuifi_ctrl_scroll_sensitivity` enviromental variables, to the disered number of characters per scroll action *(they default to 1 and 7)*

</details>
<details>
<summary><i>How do I change the default keys (besides commands)?</i></summary>

> This is not possible right now althought you could play around with the content of `toggle_vim_mode` function under `__init__.py`

</details>
<details>
<summary><i>How do I change the number of visible lines of filenames that are visible?</i></summary>

> You can set how mnay lines you want using `tuifi_visible_filename_lines` *(Defaults to 4)*

</details>
<details>
<summary><i>How do I change the default configuration path?</i></summary>

> Set `tuifi_config_path` enviroment variable to whatever you prefer most

</details>
<details>
<summary><i>How do I toggle hidden files/folders?</i></summary>

> You can either `CTRL + T` or set `tuifi_show_hidden` enviroment variable to `True`

</details>
<details>
<summary><i>How do I change the default colors?</i></summary>

> [look here for more informations](https://github.com/GiorgosXou/TUIFIManager/issues/38)

</details>


# 💗 Donation
I do really need money to survive, I have no job, living in a basement, making things for free, because I love to.
- [***Paypal Address***](https://www.paypal.com/donate/?hosted_button_id=QNQN23M55EJVS)
- ***Monero Address:*** `897ehhSQJQpGF7tYDhQM51jiX7nnHmzuYAW4q8JGwJxu8JKXvaK6AivCzatuJxnifjZ2qy98ks2g2PhmTaYCMMta2Ga2LJx`

<div align="center">
<img src='./TUIFI.png'>
</div>


# 🫶 Special thanks to
- [@KORBEN for this article](https://korben.info/gestionnaire-fichiers-terminal-tuifimanager-multiplateforme-leger-personnalisable.html)
- [Bryan Lunduke for this article](https://lunduke.substack.com/p/tuifi-manager-a-file-manager-in-the)
- [Brodie Robertson for this video](https://youtu.be/9laxdMKTZLA)
- [r/linux community for their comments](https://www.reddit.com/r/linux/comments/zzf5rx)
- [r/cyberDeck community for their comments](https://www.reddit.com/r/cyberDeck/comments/zttur0)
- [r/commandline community for their comments](https://www.reddit.com/r/commandline/comments/zt30v9)

# 🕳️ Outro
- Any Idea with this issue https://github.com/unicurses/unicurses/issues/21 ?
- Btw I use TUIFI in a daily basis. As crazy as it might sound: It's my primary file manager.




