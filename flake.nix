{
  description = "cross-platform terminal-based termux-oriented file manager.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem [
      "aarch64-darwin"
      "aarch64-linux"
      "x86_64-darwin"
      "x86_64-linux"
    ]
      (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          devShells.default = pkgs.mkShell {
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.ncurses ];
            packages =
              let
                py-env = pkgs.python310.withPackages (p: [
                  p.send2trash
                  p.unicurses
                ]);
              in
              [
                py-env
                pkgs.gnumake
              ];
          };

          formatter = pkgs.nixpkgs-fmt;
          packages = rec {
            default = tuifi-manager;
            tuifi-manager = with pkgs.python3.pkgs; buildPythonApplication {
              pname = "tuifi-manager";
              version = "master";
              format = "pyproject";
              src = ./.;

              nativeBuildInputs = [
                setuptools
                setuptools-scm
              ];

              propagatedBuildInputs = [
                send2trash
                unicurses
              ];

              pythonImportsCheck = [ "TUIFIManager" ];
              postPatch = ''
                substituteInPlace pyproject.toml \
                  --replace "Send2Trash == 1.8.0" "Send2Trash >= 1.8.0"
              '';

              meta.mainProgram = "tuifi";
            };
          };
        });
}
