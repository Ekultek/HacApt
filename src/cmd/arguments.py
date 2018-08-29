import argparse


class HacaptParser(argparse.ArgumentParser):

    def __init__(self):
        super(HacaptParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        positional = parser.add_argument_group("positional")
        positional.add_argument('install', nargs='?', default=None, help="pass this to install the specified package")
        positional.add_argument("git", nargs='?', default=None, help="pass this to force download from Git repo")
        positional.add_argument("fullclean", default=False, help="pass this to clean all manifest files and cached data")
        mandatory = parser.add_argument_group("mandatory")
        mandatory.add_argument("-r", "--root", metavar="GITHUB-URL", dest="githubManifest", help="pass a Github URL to create a package manifest and install")
        etc = parser.add_argument_group("misc")
        etc.add_argument("--check-tor", action="store_true", dest="checkTor")
        etc.add_argument("-v", "--verbose", action="store_true", dest="runVerbose", help="run in verbose mode")
        return parser.parse_args()
