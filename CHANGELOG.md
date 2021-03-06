# v.1.0.0
* this version is (kinda) a beta version

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

# v.1.1.4
* ***Fixed:***
* * [I think I Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

# v.1.1.5
* ***Fixed:***
* * [I think I Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

# v.1.1.6
* ***Fixed:***
* * [FINALLY I think I KIND OF Fixed this issue](https://github.com/GiorgosXou/TUIFIManager/issues/5)

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

# v.1.2.5
* ***Changed:***
* * Now hidden files are visible by default `suffixes=['*','.*']`
* ***Fixed:***
* * [Multiple instances when opening and closing a file](https://github.com/GiorgosXou/TUIFIManager/issues/10) Thanks to [this](https://github.com/michael-lazar/rtv/blob/b3d5bf16a70dba685e05db35308cc8a6d2b7f7aa/rtv/terminal.py#L164)
* ***Extensions:***
* Improved\Fixed typo in the corner of image-extensions
* * ***Added:***
* * * `json`, `md`