# python-devenv-demo

#### python-devenv-demo provides a tutorial to set up a VSCode-based Python development environment inside a Docker container 

If using bind mount, add file sharing folder from Docker Settings > Resources > File Sharing

Build, run, and connect to devcontainer

    docker compose up -d
    docker exec -it PYTHON_DEV bash

To start script using the Python interpreter inside container without debugger:

    python convert.py --input_folder /workspaces/python-demo/test/in --output_folder /workspaces/python-demo/test/out

To rebuild image, remove container as well as image

    docker compose down

Install Python and Remote Development plugin for VSCode

Setup .vscode/launch.json to config debugger

    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Python: Current File",
          "type": "python",
          "request": "launch",
          "program": "${file}",
          "console": "integratedTerminal",
          "args": [
            "--input_folder",
            "/workspaces/python-demo/test/in",
            "--output_folder",
            "/workspaces/python-demo/test/out",
          ]
        }
      ]
    }
