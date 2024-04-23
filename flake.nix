{
  description = "cross-platform terminal-based termux-oriented file manager.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachSystem [
      "x86_64-linux"
      "aarch64-linux"
      "aarch64-darwin"
      "x86_64-darwin"
    ] (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      py = {
        env = pkgs.python311.withPackages (p: py.deps);
        pkgs = pkgs.python311.pkgs;
        deps = with pkgs.python311.pkgs;
          [
            send2trash
            unicurses
          ]
          # pyinput is marked as broken for darwin
          # pkgs.gnome3.gnome-themes-extra
          ++ (pkgs.lib.optionals pkgs.stdenv.isLinux [
            pynput
            pyside6
            requests
            xlib
          ]);
      };
    in {
      devShells.default = pkgs.mkShell {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [pkgs.ncurses];
        packages = [
          py.env
          py.env.pkgs.venvShellHook
          pkgs.gnumake
        ];

        venvDir = "venv";
        postVenvCreation = ''
          pip install -r requirements.txt
          pip install -e .
        '';
      };

      formatter = pkgs.alejandra;
      packages = rec {
        default = tuifi-manager;
        tuifi-manager = let
          pyproject = builtins.readFile ./pyproject.toml;
          version = (builtins.fromTOML pyproject).project.version;
        in
          py.pkgs.buildPythonApplication {
            pname = "tuifi-manager";
            inherit version;

            src = ./.;
            format = "pyproject";

            nativeBuildInputs =
              (with py.pkgs; [
                setuptools
                setuptools-scm
              ])
              ++ (pkgs.lib.optionals pkgs.stdenv.isLinux [
                pkgs.qt6.wrapQtAppsHook
              ]);

            propagatedBuildInputs =
              py.deps
              ++ (with pkgs.kdePackages;
                pkgs.lib.optionals pkgs.stdenv.isLinux [
                  qtbase
                  qt6gtk2
                ]);

            pythonImportsCheck = ["TUIFIManager"];
            meta.mainProgram = "tuifi";
          };
      };
    });
}
