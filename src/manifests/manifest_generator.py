import os

import yaml
import requests

import src.lib.settings
import src.lib.errors
import src.lib.output


def generate_manifest_file(**kwargs):
    readme_link = kwargs.get("readme", "n/a")
    version = kwargs.get("version", "n/a")
    root_url = kwargs.get("root_url", None)
    tar_download_link = kwargs.get("tar_link", "self-extract")
    dependencies = kwargs.get("dependencies", "self-extract")
    force = kwargs.get("force", False)

    try:
        split = root_url.split("/")
        username = split[-2]
        project_name = split[-1]
    except Exception:
        raise src.lib.errors.RootURLNotProvidedException

    project_language = src.lib.settings.determine_project_language(root_url)
    filename = "{}.manifest.yaml".format(project_name)
    file_path = "{}/{}".format(src.lib.settings.MANIFEST_FILES_PATH, filename)

    if os.path.exists(file_path) and not force:
        src.lib.output.info("manifest file exists using stored one")
    elif os.path.exists(file_path) and force or not os.path.exists(file_path):
        for arg in kwargs:
            if kwargs[arg] is None:
                root_url = src.lib.output.prompt("enter the root URL to the Github repo")
            elif kwargs[arg].lower() == "self-extract":
                if arg == "tar_link":
                    tar_download_link = "{}/tarball/master".format(root_url)
                else:
                    if project_language == "python":
                        dependencies = "https://raw.githubusercontent.com/{}/{}/master/requirements.txt".format(
                            username, project_name
                        )
                    elif project_language == "ruby":
                        dependencies = "https://raw.githubusercontent.com/{}/{}/master/Gemfile".format(
                            username, project_name
                        )
                    try:
                        req = requests.get(dependencies, proxies=src.lib.settings.REQUESTS_PROXY)
                        if req.status_code == 200:
                            dependencies = req.content.split("\n")
                        else:
                            dependencies = "n/a"
                    except Exception:
                        dependencies = "unknown"

        with open(file_path, "a+") as manifest:
            template = src.lib.settings.MANIFEST_TEMPLATE.format(
                package_name=project_name, root_url=root_url,
                package_version=version, readme_link=readme_link,
                download_link=tar_download_link, requirements=dependencies,
                language=project_language
            )
            template = yaml.safe_load(template)
            manifest.write(yaml.safe_dump(template))

    return file_path, project_language
