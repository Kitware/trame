#!/usr/bin/env python

import json
import subprocess


def run(apps_path, out_path, *modules):
    # generate www content
    cmd = ["python", "-m", "trame.tools.www", "--output", f'{out_path}', *modules]
    subprocess.run(cmd)

    with open(apps_path, 'r') as rf:
        apps_dict = json.load(rf)

    # FIXME need to generate index.html => {app_name}.html
    # for app_name, config in apps_dict.items():
    #     name = config['app']
    #     => cp out_path/index.html out_path/{name}.html
    #     => replace data-app-name="trame" => data-app-name="{name}"


if __name__ == '__main__':
    apps_path = '/opt/trame/apps.json'
    out_path = '/deploy/server/www'
    modules = ["client", "trame", "vtk", "vuetify", "plotly", "router", "vega", "markdown"]
    run(apps_path, out_path, *modules)
