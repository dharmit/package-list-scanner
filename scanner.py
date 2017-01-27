#!/usr/bin/env python

import docker
import os
import sys

OUTDIR = "/scanout"
OUTFILE = {
    "pip": "pip-packages.txt",
    "npm": "npm-packages.txt",
    "gem": "gem-packages.txt"
}
IMAGE_NAME = os.environ.get("IMAGE_NAME")

# Client connecting to Docker socket
client = docker.Client(base_url="unix:///var/run/docker.sock")

# Argument passed to script. Decides package manager to check for.
cli_arg = sys.argv[1]

# image UUID
UUID = client.inspect_image(IMAGE_NAME)["Id"].split(':')[-1]


def binary_does_not_exist(response):
    """
    Used to figure if the npm, pip, gem binary exists in the container image
    """
    return 'executable file not found in' in response


def write_to_file(cli_arg, message):
    fout = os.path.join(OUTDIR, OUTFILE[cli_arg])

    with open(fout, "w") as f:
        f.write(message)

try:
    # Create the container before starting/running it
    container = client.create_container(image=IMAGE_NAME,
                                        command="tail -f /dev/null")

    # Running the container
    client.start(container.get('Id'))

    # Check for pip updates
    if cli_arg == "pip":
        # variable to store info about exec_start
        exe = client.exec_create(
            container=container.get("Id"),
            cmd="pip list"
        )

        response = client.exec_start(exe)

    # Check for rubygem updates
    elif cli_arg == "gem":
        exe = client.exec_create(
            container=container.get("Id"),
            cmd="gem outdated"
        )

        response = client.exec_start(exe)

    # Check for npm updates
    elif cli_arg == "npm":
        exe = client.exec_create(
            container=container.get("Id"),
            cmd="npm -g ls --depth=0 | awk 'NR>1 {print $2}'"
        )

        response = client.exec_start(exe)

    if binary_does_not_exist(response):
        write_to_file(
            cli_arg,
            "{} binary does not exist in container image".format(cli_arg)
        )
    else:
        write_to_file(
            cli_arg,
            response
        )

    # remove the container
    client.remove_container(container=container.get("Id"), force=True)
except Exception as e:
    pass
