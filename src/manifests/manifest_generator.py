import os

import yaml
import requests

import hacapt.lib.settings
import hacapt.lib.errors


def generate_manifest_file(**kwargs):
    readme_link = kwargs.get("readme", "n/a")
    version = kwargs.get("version", "n/a")
    root_url = kwargs.get("root_url", None)
    tar_download_link = kwargs.get("tar_link", "self-extract")
    dependencies = kwargs.get("dependencies", "self-extract")

    try:
        split = root_url.split("/")
        username = split[-2]
        project_name = split[-1]
    except Exception:
        raise hacapt.lib.errors.RootURLNotProvidedException

    for arg in kwargs:
        if kwargs[arg] is None:
            # TODO:/ prompt for the root URL because it is needed in order to access the files
            pass
        elif kwargs[arg].lower() == "self-extract":
            if arg == "tar_link":
                tar_download_link = "{}/tarball/master".format(root_url)
            else:
                dependencies = "https://raw.githubusercontent.com/{}/{}/master/requirements.txt".format(
                    username, project_name
                )
                try:
                    req = requests.get(dependencies, proxies=hacapt.lib.settings.REQUESTS_PROXY).content
                    dependencies = req.split("\n")
                except Exception:
                    dependencies = "unknown"

    filename = "{}-manifest.yaml".format(project_name)
    file_path = "{}/{}".format(hacapt.lib.settings.MANIFEST_FILES_PATH, filename)
    if not os.path.exists(file_path):
        with open(file_path, "a+") as manifest:
            template = hacapt.lib.settings.MANIFEST_TEMPLATE.format(
                package_name=project_name, root_url=root_url,
                package_version=version, readme_link=readme_link,
                download_link=tar_download_link, requirements=dependencies
            )
            template = yaml.safe_load(template)
            manifest.write(yaml.safe_dump(template))
    return file_path
