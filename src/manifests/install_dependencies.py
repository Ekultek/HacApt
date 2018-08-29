from __future__ import print_function

import shlex
import subprocess

import yaml

import hacapt.lib.settings


def run_install(args):
    command = shlex.split("pip install")
    if args is not None:
        for arg in args:
            command.append(arg)
    print("running command '{}'".format(" ".join(command)))
    return subprocess.call(command)


def install_dependencies(manifest_filename):
    with open(manifest_filename) as manifest:
        data = yaml.safe_load(manifest.read())
        for depend in data["package"][manifest_filename.split("-")[0].split("/")[-1]]["dependencies"]:
            print("installing dependency: {}".format(depend))
            run_install([depend, "-vv", "--proxy", hacapt.lib.settings.TOR_PROXY])
