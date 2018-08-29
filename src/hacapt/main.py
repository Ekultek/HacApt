import os
import shutil

from cmd.arguments import HacaptParser
from manifests.manifest_generator import generate_manifest_file
from manifests.install_dependencies import install_dependencies
from lib.settings import IS_LOCKED, LOCKFILE_PATH, HOME, safe_delete
from lib.errors import LockFileExistsException, NonRootUserException


def main():

    try:

        if not os.getuid() == 0:
            raise NonRootUserException(
                'must be run as root'
            )

        opt = HacaptParser().optparse()

        if IS_LOCKED:
            raise LockFileExistsException(
                'you will need to delete the lock file out of \'{}\' this usually occurs when there is an issue '
                'downloading a package'.format(LOCKFILE_PATH))
        else:
            open(LOCKFILE_PATH, "a+").close()

        if opt.fullclean:
            print("cleaning home folder")
            files = []
            for root, _, filenames in os.walk(HOME):
                for f in filenames:
                    files.append(os.path.join(root, f))
            for f in files:
                safe_delete(f, verbose=opt.runVerbose)
            exit(-1)

        if opt.install is None and opt.githubManifest is None:
            print("you gave me nothing to do...")

        # generate_manifest_file(
        #     root_url="https://github.com/ekultek/whatwaf",
        #     readme="n/a",
        #     version="n/a",
        #     tar_link="self-extract",
        #     dependencies="self-extract"
        # )
    except AttributeError as e:
        print(e)


    try:
        os.unlink(LOCKFILE_PATH)
    except:
        pass