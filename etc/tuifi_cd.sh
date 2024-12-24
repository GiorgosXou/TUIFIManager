# You need to copy the content of this file to your shell rc file (e.g. `~/.bashrc` `~/.zshrc`)

function _tuifi(){
  # Run tuifi. Optionally enable escape-key to cd if set to True
  tuifi_cd_on_esc=False tuifi "$@"

  # Check if path exists in this virtual file system (stored in RAM) and cd...
  if [ -e /dev/shm/tuifi_last_path.txt ]; then
    cd "$(</dev/shm/tuifi_last_path.txt)"
    rm /dev/shm/tuifi_last_path.txt
  fi
}

# Alias for TUIFIManager with cd functionality on exit (Ctrl+E)
alias tuifi='_tuifi'
