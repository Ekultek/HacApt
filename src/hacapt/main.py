import os
import shutil

from src.cmd.arguments import HacaptParser
from src.manifests.manifest_generator import generate_manifest_file
from src.manifests.install_dependencies import install_dependencies
from src.lib.settings import IS_LOCKED, LOCKFILE_PATH, HOME, safe_delete, check_if_run, parse_manifest, output_infomation, MANIFEST_FILES_PATH
from src.lib.errors import LockFileExistsException, NonRootUserException
from src.lib.output import info, error, fatal, prompt, warn


def main():

    try:

        check_if_run()

        # if not os.getuid() == 0:
        #     raise NonRootUserException(
        #         'must be run as root'
        #     )

        opt = HacaptParser().optparse()

        if IS_LOCKED:
            raise LockFileExistsException(
                'you will need to delete the lock file out of \'{}\' this usually occurs when there is an issue '
                'downloading a package'.format(LOCKFILE_PATH))
        else:
            open(LOCKFILE_PATH, "a+").close()

        if opt.listManifestFiles:
            files = os.listdir(MANIFEST_FILES_PATH)
            info("there is a total of {} manifest file(s) installed".format(len(files)))
            print("{}\n{}\n{}".format("-" * 30, '\n'.join([f for f in files]), "-" * 30))

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
            error("there's nothing left to do..?")
        elif opt.install is None:
            info('generating manifest file for Github repo \'{}\''.format(opt.githubManifest))
            manifest_file, language_used = generate_manifest_file(
                root_url=opt.githubManifest,
                readme=opt.readMeLink,
                version=opt.repoVersion,
                tar_link=opt.tarDownloadLink,
                dependencies=opt.dependencyFile
            )
            info("manifest file generated and stored in '{}'".format(manifest_file))
            data = parse_manifest(manifest_file)
            if opt.runVerbose:
                output_infomation(data)
            info("attempting to install dependencies")
            install_dependencies(manifest_file, language_used)
    except AttributeError as e:
        print(e)


    try:
        os.unlink(LOCKFILE_PATH)
    except:
        pass