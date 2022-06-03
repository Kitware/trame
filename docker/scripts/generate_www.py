#!/usr/bin/env python

import json
import subprocess


def run(apps_path, out_path):
    # Generate www content
    cmd = ["python", "-m", "trame.tools.www", "--output", out_path]
    subprocess.run(cmd)

    # Generate app files index.html => {app_name}.html
    with open(apps_path, "r") as rf:
        apps_dict = json.load(rf)  # noqa

        for app_name, config in apps_dict.items():
            name = config["app"]
            web_modules = config.get("www_modules")
            if web_modules is not None:
                cmd = [
                    "python",
                    "-m",
                    "trame.tools.www",
                    "--output",
                    out_path,
                    *web_modules,
                ]
                subprocess.run(cmd)
            print(" => create app: ", app_name, name)
            cmd = [
                "python",
                "-m",
                "trame.tools.app",
                "--input",
                out_path,
                "--name",
                name,
            ]
            subprocess.run(cmd)


if __name__ == "__main__":
    apps_path = "/opt/trame/apps.json"
    out_path = "/deploy/server/www"
    run(apps_path, out_path)
