import os
import re
import random
import string
import getpass

import requests
import yaml
from bs4 import BeautifulSoup

import output


MANIFEST_TEMPLATE = """package:
  {package_name}:
    root url: {root_url}
    version: {package_version}
    readme: {readme_link}
    tar download: {download_link}
    dependencies: {requirements}
    language: {language}"""
INIT_CONFIG_TEMPLATE = """config:
  username: {username}
  uid: {uuid}
  gid: {guid}
  home: {home_location}"""
HOME = "/usr/local/etc/hacapt"
SCRIPT_LOCATIONS = "/usr/local/bin"
CONFIG_PATH = "{}/.conf.yaml".format(HOME)
MANIFEST_FILES_PATH = "{}/manifests".format(HOME)
PACKAGE_LOCATIONS = "{}/packages".format(HOME)
TOR_PROXY = "socks5://127.0.0.1:9050"
REQUESTS_PROXY = {"http": TOR_PROXY, "https": TOR_PROXY}
LOCKFILE_PATH = "{}/.haclock".format(HOME)
IS_LOCKED = os.path.exists(LOCKFILE_PATH)
VERSION = "0.0.1"


def safe_delete(path, passes=3, verbose=False):
    import struct

    length = os.path.getsize(path)
    data = open(path, "w")
    # fill with random printable characters
    if verbose:
        print("filling '{}' with random printable".format(path))
    for _ in xrange(passes):
        data.seek(0)
        data.write(''.join(random.choice(string.printable) for _ in range(length)))
    # fill with random data from the OS
    if verbose:
        print("filling '{}' with urandom".format(path))
    for _ in xrange(passes):
        data.seek(0)
        data.write(os.urandom(length))
    # fill with null bytes
    if verbose:
        print("filling '{}' with null bytes".format(path))
    for _ in xrange(passes):
        data.seek(0)
        data.write(struct.pack("B", 0) * length)
    data.close()
    if verbose:
        print("removing file")
    os.remove(path)


def check_if_run():
    paths = [HOME, MANIFEST_FILES_PATH]
    if not os.path.exists(HOME):
        output.info("initializing hacapt")
        if os.getuid() == 0:
            output.error("initializing as root")
        current_uid = os.getuid()
        current_gid = os.getgid()
        current_user = getpass.getuser()
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        with open(CONFIG_PATH, "a+") as conf:
            conf.write(INIT_CONFIG_TEMPLATE.format(
                username=current_user,
                uuid=current_uid,
                guid=current_gid,
                home_location=HOME
            ))
        output.info("initialized successfully")
        exit(1)


def parse_manifest(file_path):
    with open(file_path) as manifest:
        return yaml.safe_load(manifest.read())


def output_infomation(data):
    seperator = "-" * 50
    package_information = []
    for item in data["package"]:
        package_information.append(("package name", item))
        for key in data["package"][item]:
            package_information.append((key, data["package"][item][key]))
    print(seperator)
    for item in package_information:
        print("{}: {}".format(item[0].title(), item[1]))
    print(seperator)


def determine_project_language(root_url):
    temp, cleaned = [], []
    __clean_entity = lambda html: html.split(">")[1].split("<")[0]
    identifier = re.compile(r"<span class=.lang.>\w+(\S+)?</span>", re.I)
    req = requests.get(root_url, proxies=REQUESTS_PROXY)
    soup = BeautifulSoup(req.content, "html.parser")
    language_stats = str(soup.findAll("div", {"class": "repository-lang-stats"})[0]).split("\n")
    for i, entity in enumerate(language_stats):
        if identifier.search(entity) is not None:
            temp.append((entity, language_stats[i+1]))
    for item in temp:
        lang = __clean_entity(item[0])
        amount = __clean_entity(item[1])
        cleaned.append((lang, amount))
    most_used_language = cleaned[0][0]
    return most_used_language.lower()




