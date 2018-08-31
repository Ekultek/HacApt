import argparse


class HacaptParser(argparse.ArgumentParser):

    def __init__(self):
        super(HacaptParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        mandatory = parser.add_argument_group("mandatory")
        mandatory.add_argument("-i", "--install", dest="install", nargs="?", metavar="PACKAGE-NAME", help="install this package")
        mandatory.add_argument("-r", "--root", metavar="GITHUB-URL", dest="githubManifest", help="pass a Github URL to create a package manifest and install the repo")
        info = parser.add_argument_group("info")
        info.add_argument("-R", "--readme-link", metavar="README-URL", dest="readMeLink", default="n/a", help="pass the README link to add to the manifest")
        info.add_argument("-V", "--repo-version", metavar="REPO-VERSION-#", dest="repoVersion", default="n/a", help="pass the version of the repo")
        info.add_argument("-t", "--tar-download", metavar="LINK", dest="tarDownloadLink", default="self-extract", help="pass the link to the tar download")
        info.add_argument("-d", "--dependencies", metavar="DEPENDENCY=-FILE-LINK", dest="dependencyFile", default="self-extract", help="pass the link to the raw dependency file")
        etc = parser.add_argument_group("misc")
        etc.add_argument("--check-tor", action="store_true", dest="checkTor")
        etc.add_argument("-v", "--verbose", action="store_true", dest="runVerbose", help="run in verbose mode")
        etc.add_argument("-F", "--full-clean", action="store_true", default=False, dest="fullclean", help="clean the manifest files and all the cache")
        etc.add_argument("--force", action="store_true", default=False, dest="forceInstall", help="force an installation of a package")
        etc.add_argument("-l", "--list-manifests", action="store_true", default=False, dest="listManifestFiles", help="show a list of all installed manifest files")
        return parser.parse_args()
