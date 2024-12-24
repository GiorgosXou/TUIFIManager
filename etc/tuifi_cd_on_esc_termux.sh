# You need to copy the content of this file to your shell rc file (e.g. `~/.bashrc` `~/.zshrc`)
# !!! This script defaults to cd-on-escape key

function _tuifi() {
  tuifi_cd_on_esc=True tuifi "$@"
  cd "$(</data/data/com.termux/files/usr/tmp/tuifi_last_path.txt)"
  # (prefer '/dev/shm/tuifi_last_path.txt' instead, if it exists)
}

alias tuifi='_tuifi'

