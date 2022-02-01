#!/usr/bin/env python

import json
import subprocess


def run(apps_path, out_path):
    with open(apps_path, 'r') as rf:
        apps_dict = json.load(rf)

    for app_name, config in apps_dict.items():
        script_name = config['app']
        subprocess.run([script_name, '--www', f'{app_name}:{out_path}'])


if __name__ == '__main__':
    apps_path = '/opt/trame/apps.json'
    out_path = '/deploy/server/www'
    run(apps_path, out_path)
