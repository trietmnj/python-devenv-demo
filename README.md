# python-devenv-demo

If using bind mount, add file sharing folder from Docker Settings > Resources > File Sharing

Build, run, and connect to devcontainer

    docker compose up -d
    docker exec -it PYTHON_DEV bash

Install Python plugin for VSCode

Setup launch.json to config debugger

To start script using the Python interpreter inside container without debugger:

    python convert.py --input_folder /workspaces/python-demo/test/in --output_folder /workspaces/python-demo/test/out

To rebuild image, remove container as well as image

    docker compose down
