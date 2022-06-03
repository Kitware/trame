#!/usr/bin/env python3

import json
from pathlib import Path


def run(input_path, apps_path, out_path):
    default_command_flags = [
        "--host",
        "${host}",
        "--port",
        "${port}",
        "--authKey",
        "${secret}",
        "--server",
    ]
    default_ready_line = "App running at"

    with open(input_path, "r") as rf:
        input_dict = json.load(rf)

    if not Path(apps_path).exists():
        raise Exception(f"{apps_path} does not exist")

    with open(apps_path, "r") as rf:
        apps_dict = json.load(rf)

    if not apps_dict:
        raise Exception(f"{apps_path} is empty")

    for app_name, config in apps_dict.items():
        if "app" not in config and "cmd" not in config:
            msg = (
                f'In {apps_path}, every app must contain an "app" key if a "cmd" is not provided, but '
                f'"{app_name}" does not'
            )
            raise Exception(msg)

        if "cmd" in config and "args" in config:
            msg = (
                f'In {apps_path}, "args" and "cmd" cannot both be specified. '
                '"args" is for appending extra args to the default "cmd", but '
                '"cmd" is for overriding the command entirely. Error occurred '
                f'in "{app_name}".'
            )
            raise Exception(msg)

        default_cmd = [
            config.get("app", "your_trame_app_package_name")
        ] + default_command_flags
        cmd = config.get("cmd", default_cmd)
        cmd += config.get("args", [])
        ready_line = config.get("ready_line", default_ready_line)

        input_dict.setdefault("apps", {})
        input_dict["apps"][app_name] = {
            "cmd": cmd,
            "ready_line": ready_line,
        }

    if "trame" not in input_dict["apps"]:
        # Make a copy of the first app and put it in PyWebVue, so that
        # the default localhost:9000 web page will use that app.
        first_key = next(iter(input_dict["apps"]))
        input_dict["apps"]["trame"] = input_dict["apps"][first_key]

    with open(out_path, "w") as wf:
        json.dump(input_dict, wf, indent=2)


if __name__ == "__main__":
    default_input_path = "/opt/trame/default-launcher.json"
    override_input_path = "/deploy/setup/launcher.json"
    apps_path = "/opt/trame/apps.json"
    out_path = "/deploy/server/launcher.json"

    if Path(override_input_path).exists():
        input_path = override_input_path
    else:
        input_path = default_input_path

    run(input_path, apps_path, out_path)
