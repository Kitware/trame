#!/usr/bin/env python

import os
import json
import subprocess

CLIENT_TYPE = os.environ.get("TRAME_CLIENT_TYPE", "vue3")


def run(apps_path, out_path):
    # Generate www content
    cmd = [
        "python",
        "-m",
        "trame.tools.www",
        "--output",
        out_path,
        "--client-type",
        CLIENT_TYPE,
    ]
    subprocess.run(cmd)

    # Generate app files index.html => {app_name}.html
    with open(apps_path, "r") as rf:
        apps_dict = json.load(rf)  # noqa

        for app_name, config in apps_dict.items():
            # handle custom modules for www
            web_modules = config.get("www_modules")
            client_type = config.get("client_type", CLIENT_TYPE)
            if web_modules is not None:
                cmd = [
                    "python",
                    "-m",
                    "trame.tools.www",
                    "--output",
                    out_path,
                    "--client-type",
                    client_type,
                    *web_modules,
                ]
                subprocess.run(cmd)

            # Create app.html file from index.html
            cmd = [
                "python",
                "-m",
                "trame.tools.app",
                "--input",
                out_path,
                "--name",
                app_name,
            ]
            subprocess.run(cmd)


if __name__ == "__main__":
    apps_path = "/opt/trame/apps.json"
    out_path = "/deploy/server/www"
    run(apps_path, out_path)
