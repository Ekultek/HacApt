import os
import stat
import shlex
import subprocess

from src.lib.settings import (
    PACKAGE_LOCATIONS,
    SCRIPT_LOCATIONS
)


def install(package_name, root_url, language):
    ext = "py" if language.lower() == "python" else "rb"
    path = "{}/{}".format(PACKAGE_LOCATIONS, package_name)
    if not os.path.exists(path):
        os.makedirs(path)
    command = shlex.split("git clone {} {}".format(root_url, path))
    try:
        proc = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        proc = None

    if proc is None:
        return False
    else:
        script = "{}/{}".format(SCRIPT_LOCATIONS, package_name)
        text = "#!/bin/bash\n# this is the execution script for {}\n\ncd {}\nexec {} {}.{} $@".format(
                package_name, path, language, package_name, ext
            )
        with open(script, "a+") as package:
            package.write(text)
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)
        return True
