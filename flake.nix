{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils } @inputs:
    utils.lib.eachDefaultSystem (system:
      with import nixpkgs { inherit system; }; {
        devShells.default = mkShell {
          LD_LIBRARY_PATH = lib.makeLibraryPath [ncurses6];
          venvDir = "venv";
          buildInputs = [
            pkgs.gnumake
            pkgs.python310Full
            pkgs.ncurses6
            pkgs.python310Packages.venvShellHook
          ];
          postVenvCreation = ''
            pip install -r requirements.txt
            pip install -e .
          '';
        };
      });
}
