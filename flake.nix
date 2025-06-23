{
  description = "DevShell con Terraform, Docker, Python y ECR login";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          pip
        ]);

        commonDeps = with pkgs; [
          pythonEnv
          poetry
          git
          terraform
          python311
          awscli
          gcc
          stdenv.cc.cc.lib
          awscli
          httpie
          go
          go-task
          docker
          amazon-ecr-credential-helper
          jq
          nodejs_20
          nodePackages.lerna
          google-chrome
          subfinder
          amass
          imagemagick
        ];
      in {
        devShells.default = pkgs.mkShell {
          packages = commonDeps;

          shellHook = ''
            pyenv global system
            export pythonEnv=${pythonEnv}
            export PATH=$PATH:${pythonEnv}/bin
            cd core && poetry env use ${pythonEnv}/bin/python && cd -
            cd core && poetry config virtualenvs.create true && cd -
            docker compose up --build -d
            docker compose ps -a
            task dependencies
            #task terraform:apply
            mkdir -p ~/.docker
            echo '{
              "credsStore": "ecr-login"
            }' > ~/.docker/config.json
            echo "Docker config set to use docker-credential-ecr-login"
          '';
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib

          ];

        };
      });

}
