import os
import re
import time
import shlex
import string
import random
import subprocess

import yaml

from .install_package import install
import src.lib.output
import src.lib.settings


def run_install(args, project_lang, user):
    # give the files time to catch up
    time.sleep(1)
    if project_lang.lower() == "python":
        command = shlex.split("pip install")
    elif project_lang.lower() == "ruby":
        os.setuid(user)
        command = shlex.split("bundle install")
    if args is not None:
        for arg in args:
            command.append(arg)
    src.lib.output.info("running command '{}'".format(" ".join(command)))
    try:
        proc = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        return False
    failed_identifier = re.compile("failed|error", re.I)
    for item in proc:
        if failed_identifier.search(item) is not None:
            return False
    return True


def generate_temporary_req_file(data_to_add, gemfile=False, requirements_file=False):
    if gemfile:
        filename = "{}/{}".format(os.getcwd(), "Gemfile")
    if requirements_file:
        filename = []
        for _ in range(5):
            filename.append(random.choice(string.ascii_letters))
        filename = ''.join(filename) + ".txt"
    with open(filename, "a+") as req:
        req.write(data_to_add)
    return filename


def install_dependencies(manifest_filename, language, tries=3):
    package_name = manifest_filename.split("/")[-1].split(".")[0]
    with open(manifest_filename) as manifest:
        data = yaml.safe_load(manifest.read())
        __dependency_check = lambda d: d["package"][manifest_filename.split("/")[-1]]["dependencies"] == "n/a"
        if language == "ruby":
            conf = yaml.safe_load(open(src.lib.settings.CONFIG_PATH).read())
            uid = conf["config"]["uid"]
            src.lib.output.warn("bundler will not be run behind Tor connection")
            set_opts = (["-V"], language, uid)
            if not __dependency_check:
                dependencies = data["package"][manifest_filename.split(".")[0].split("/")[-1]]["dependencies"]
                dependencies = "\n".join(dependencies)
                gemfile = generate_temporary_req_file(dependencies, gemfile=True)
            else:
                dependencies = None
        elif language == "python":
            set_opts = (["-vv", "--proxy", src.lib.settings.TOR_PROXY], language, None)
            if not __dependency_check:
                dependencies = data["package"][manifest_filename.split(".")[0].split("/")[-1]]["dependencies"]
                dependencies = "\n".join(dependencies)
                requirements_file = generate_temporary_req_file(dependencies, language)
            else:
                dependencies = None
                requirements_file = ""
            set_opts[0].append("-r")
            set_opts[0].append(requirements_file)
        if dependencies is not None:
            results = run_install(*set_opts)
        else:
            results = True
        if results:
            src.lib.output.info("dependencies installed successsully")
        else:
            if tries != 0:
                src.lib.output.error("failed to install dependencies, trying again ({})".format(tries))
                install_dependencies(manifest_filename, language, tries=tries-1)
            else:
                src.lib.output.fatal("attempted to install dependencies multiple times and failed, giving up")
        try:
            os.unlink(gemfile)
        except:
            pass
        try:
            os.unlink(requirements_file)
        except:
            pass

        src.lib.output.info("installing package now")
        installation_results = install(package_name, data["package"][package_name]["root url"], language)
        if installation_results:
            src.lib.output.info("installed successfully! just run `{} <ARGS>`".format(package_name))
        else:
            src.lib.output.error("failed to install package")