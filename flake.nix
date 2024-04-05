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
    flake-utils.lib.eachSystem ["x86_64-linux"] (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.default = let
        py-env = pkgs.python310.withPackages (p: [
          p.send2trash
          p.unicurses
        ]);
      in
        pkgs.mkShell {
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [pkgs.ncurses];
          packages = [
            py-env
            py-env.pkgs.venvShellHook
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
        in with pkgs.python3.pkgs;
          buildPythonApplication {
            pname = "tuifi-manager";
            inherit version;

            src = ./.;
            format = "pyproject";

            nativeBuildInputs = [
              setuptools
              setuptools-scm
            ];

            propagatedBuildInputs = [
              send2trash
              unicurses
            ];

            pythonImportsCheck = ["TUIFIManager"];
            meta.mainProgram = "tuifi";
          };
      };
    });
}
