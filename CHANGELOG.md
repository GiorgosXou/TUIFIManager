# v.DEVELOPMENT

------------------------
# v.2.1.9
- ***Fixed:***
- - [`ALT_DOWN`](https://github.com/unicurses/unicurses/commit/a185cfb930d783f55c1efccd35e9ae23c0208a6e#diff-4f9493a5a3fb9e08d28013e7923bf5856d4368d076222caaa60c9a5e4a421f8c)
- - [ncurses not found but existing on macOS](https://github.com/GiorgosXou/TUIFIManager/issues/28)
- ***Improved:***
- - [chunk_str method](https://github.com/GiorgosXou/TUIFIManager/pull/31)
- - [Removed Whitespaces](https://github.com/GiorgosXou/TUIFIManager/pull/34)
- - [Deleting files now go to trash](https://github.com/GiorgosXou/TUIFIManager/pull/32)
- ***Extensions:***
- - ***Improved:***
- - - `gif`

# v.2.1.3
- Changed:
- - Search\\INPUT-mode in `vim_mode` doesn't change *(automatically to NORMAL)* anymore when entering a directory
- ***Fixed:***
- - Label text when exiting a from file
- - [Typo `SEAERCH` to `SEAERCH`](https://github.com/GiorgosXou/TUIFIManager/pull/29)
- - Issue in `vim_mode` when escaping search\\INPUT-mode without searching anything at all
- ***Added:***
- - [Using `EDITOR`-env-variable if no `tuifi_default_editor`](https://github.com/GiorgosXou/TUIFIManager/issues/30)
- ***Extensions:***
- - ***Fixed:***
- - - [typo at `conf`](https://github.com/GiorgosXou/TUIFIManager/issues/27)
- - ***Added:***
- - - `m4a` 
- - ***Improved:***
- - - `mp3`, `wav`, `mid`, `aac`, `bat`, `cmd`, `dll`, `so`

# v.2.0.5
- ***Fixed:***
- - Temporary FIX, conflicting with TERMUX ctrl keys 

# v.2.0.4
- ***Fixed:***
- - Annoying issue with keyboard movement after searching
- - Issue with Control keys when in search mode
- ***Added:***
- - Extra informations when copy/cut pasting

# v.2.0.2
- ***Fixed:***
- - Forgot to comment the first 3 lines of code in `__main__.py`

# v.2.0.1
- ***Fixed:***
- - Issue with `DEFAULT_OPENER`

# v.2.0.0 
- ***Changed:***
- - Introduced `TUItilities.py` and `Component`-class into the `TUIFIManager` [...]
- ***Added:***
- - [LICENSE](./README.md)
- - [Vim like motions](https://github.com/GiorgosXou/TUIFIManager/issues/19)
- - Dim effect on hidden files
- - Duplicate action on copy paste
- - Introduced `self.info_label` from `TUItilities.py`
- - `CTRL+O` open directory with `DEFAULT_WITH` = `DEFAULT_EDITOR`
- ***Fixed:***
- - [CTRL+C raises auto-search function](https://github.com/GiorgosXou/TUIFIManager/issues/24)
- - [Over-lapping files when exiting search mode](https://github.com/GiorgosXou/TUIFIManager/issues/25)
- - Major issue with dynamic resizing of the pad when used as a component
- - Permanently, fixed issue with keyname *(TODO: fix decode() inside uni-curses keyname())*
- - Replaced `cut`ing method 
- ***Extensions:*** 
- - ***Added:***
- - - `pyc`, `ttf`, `otf`, `woff`, `woff2`, `reg`, `gitignore`, `makefile`, `conf`, `config`
- - ***Improved:***
- - `ino`, `vb`, `pdf`, `html`, `md`, `bin`, `psd`, tar once

# v.1.3.3
* ***Fixed:***
* * TEMPORARILY the issue with double hidden files.

# v.1.3.2
* ***Fixed:***
* * Creation of new file immediately after opening a folder
 
# v.1.3.1
* ***Fixed:***
* * Scroll issues and etc. when finding

# v.1.3.0
* ***Added:***
* * Searching now is possible *(with a tiny issue when deleting files)*
* * Renaming now deletes the whole underlined name if no movement occurres
* ***Fixed:***
* * `HOME`\\`END` keys now work on renaming mode
* * No more *["Oppsie | re.error"](https://github.com/GiorgosXou/TUIFIManager/issues/13)*
* * `subprocess.Popen` *["OSError"](https://github.com/GiorgosXou/TUIFIManager/issues/14)*
* * `DEFAULT_OPENER` [issue 9](https://github.com/GiorgosXou/TUIFIManager/issues/9)
* * Now it doesn't clear everything when open()
* ***Extensions:*** 
* * ***Added:***
* * `apk`, `vim`, `tuifi3`

# v.1.2.6
* ***Added:***
* * `DEFAULT_OPENER` [issue 9](https://github.com/GiorgosXou/TUIFIManager/issues/9) but temporarily
* ***Removed:***
* * `DEFAULT_UNCOMPRESSOR`
* ***Extensions:*** 
* * ***Added:***
* * * `xlsx`, `ino`, `scss`
* * ***Improved:***
* * * `css`, `md`, `gif` and sound ones

# v.1.2.5
* ***Changed:***
* * Now hidden files are visible by default `suffixes=['*','.*']`
* ***Fixed:***
* * [Multiple instances when opening and closing a file](https://github.com/GiorgosXou/TUIFIManager/issues/10) Thanks to [this](https://github.com/michael-lazar/rtv/blob/b3d5bf16a70dba685e05db35308cc8a6d2b7f7aa/rtv/terminal.py#L164)
* ***Extensions:***
* Improved\Fixed typo in the corner of image-extensions
* * ***Added:***
* * * `json`, `md`

# v.1.2.3
* ***Fixed:***
* * Issue when renaming a folder
* ***Improved:***
* * code *(added: `get_profile()`)*
* ***Extensions:*** 
* * ***Added:***
* * * `h`, `fs`, `html`, `jar`
* * ***Improved:***
* * * `c`, `cpp`, `psd`
* *  ***Fixed:***
* * * [`.ogv`](https://github.com/GiorgosXou/TUIFIManager/issues/9) icon

# v.1.2.0
* ***Fixed:***
* * [Replace profile when renaming extension](https://github.com/GiorgosXou/TUIFIManager/issues/8)
* * Renaming to an already existing file-name *(temp-fix?)*
* * Renaming to "nothing"/''
* ***Added:***
* * Ability to create files and folders
* * ***Extensions:*** 
* * * `py`, `lua`, `vbs`, `go`, `rs`, `java`
* * * ***Improved:***
* * * * `vb`
* ***Changed:***
* * `is_on_reaname_mode` to `escape_event_consumed` *[(name inspired by java)](https://docs.oracle.com/javase/7/docs/api/java/awt/event/InputEvent.html#consume())*

# v.1.1.7
* ***Fixed:***
* * [Issue](https://github.com/GiorgosXou/TUIFIManager/issues/7) *(Kind of, I mean...)* 
* * *["Select mode navigation to '..'"](https://github.com/GiorgosXou/TUIFIManager/issues/6)* 
* * Copying folder and pasting it inside the copied folder
* ***Added:***
* * ***Extensions:*** 
* * * `psd`
* * ***Keybindings:***
* * * `CTRL + R` Rename selected file. *(Not the best implementation but nvm for now)* 
* ***Changed:***
* * `reload()`/refresh now works with `KEY_F5` insted of `CTRL+R`
* ***Removed:***
* * `tuifi_config.json` Ability to change default `TUIFIProfiles` | Reason: *(Bad Implementation)*

# v.1.1.6
* ***Fixed:***
* * [FINALLY I think I KIND OF Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

# v.1.1.5
* ***Fixed:***
* * [I think I Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

# v.1.1.4
* ***Fixed:***
* * [I think I Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

# v.1.1.3
* ***Fixed:***
* * [Now when running `tuifi`, it starts from the current working directory](https://github.com/GiorgosXou/TUIFIManager/issues/4)
* * Overall minor code improvments
* * [REMOVED: `CTRL + S`](https://github.com/GiorgosXou/TUIFIManager/issues/3)
* * [`CTRL + C`](https://github.com/GiorgosXou/TUIFIManager/issues/2) 
* ***Added:***
* * "Right-Click" menu
* * `tuifi_config.json` Ability to change default `TUIFIProfiles`
* * `TUIFIManager` > `double_click_DELAY` *(defaults to 0.4 seconds [[ISSUE ON WINDOWS](https://github.com/wmcbrine/PDCurses/issues/130)])*
* * ***Extensions:*** 
* * * `mp3`, `wav`, `mid`, `aac`, `webp`, `tiff`, `tif`, `tga`, `heif`, `heifs`, `heic`, `avi`, `webm`, `ogv`, `bat`, `tar`, `tar.gz`, `tar.xz`, `tar.bz2`, `tar.zst` [request request](https://github.com/GiorgosXou/TUIFIManager/pull/1)
* * ***Keybindings:***
* * * `KEY_HOME` *(Navigates to $HOME directory)*
* * * `ALT + DOWN` Opens the "Right-Click" menu
* * * ***TERMUX only:***
* * * * `CTRL + DOWN` *(Goes in&out of select-mode while also automatically copies the selected file(s))*
* * * * `CTRL + LEFT` *(Goes out of select-mode while also cuts the seleccted file(s))*
* * * * `CTRL + END` *(Goes out of select-mode while also deleting the selected file(s))*
* * * * `CTRL + UP` *(Same as`CTRL + V`, Pastes the copied/cutted files)*
* * * * `END` *(Deletes selected files)*

# v.1.0.0
* this version is (kinda) a beta version
