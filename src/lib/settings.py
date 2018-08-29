import os
import random
import string


MANIFEST_TEMPLATE = """package:
  {package_name}:
    root_url: {root_url}
    version: {package_version}
    readme: {readme_link}
    tar_download: {download_link}
    dependencies: {requirements}"""
HOME = "/etc/hacapt"
MANIFEST_FILES_PATH = "{}/manifests".format(HOME)
TOR_PROXY = "socks5://127.0.0.1:9050"
REQUESTS_PROXY = {"http": TOR_PROXY, "https": TOR_PROXY}
LOCKFILE_PATH = "{}/.haclock".format(HOME)
IS_LOCKED = os.path.exists(LOCKFILE_PATH)


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