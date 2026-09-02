{
  description = "bci-BKI323 dev shell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        nixpkgs.follows = "nixpkgs";
      };
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs =
    {
      nixpkgs,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      ...
    }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };

      python = pkgs.python311;

      pythonSet = (pkgs.callPackage pyproject-nix.build.packages { inherit python; }).overrideScope (
        pkgs.lib.composeManyExtensions [
          pyproject-build-systems.overlays.default
          overlay

          # .so files that need to be maually linked
          (final: prev: {
            torchaudio = prev.torchaudio.overrideAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ [
                pkgs.ffmpeg_6
                pkgs.sox
              ];

              preFixup = (old.preFixup or "") + ''
                addAutoPatchelfSearchPath "${final.torch}/${python.sitePackages}/torch"

                # only ffmpeg_6 is provided above; drop the other bundled
                # ffmpeg-version shims so autoPatchelf doesn't try to resolve them
                rm -f $out/${python.sitePackages}/torio/lib/*torio_ffmpeg4*.so
                rm -f $out/${python.sitePackages}/torio/lib/*torio_ffmpeg5*.so
                rm -f $out/${python.sitePackages}/torio/lib/*torio_ffmpeg7*.so
              '';
            });
          })
        ]
      );

      venv = pythonSet.mkVirtualEnv "bci-BKI323-env" workspace.deps.all;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          venv
          pkgs.uv
        ];

        env = {
          UV_NO_SYNC = "1";
          UV_PYTHON = "${venv}/bin/python";
          UV_PYTHON_DOWNLOADS = "never";

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            # Numpy
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
          ];
        };
      };
    };
}
