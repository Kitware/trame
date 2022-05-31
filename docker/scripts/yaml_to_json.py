#!/usr/bin/env python3

import json
import sys
import yaml

if len(sys.argv) < 3:
    sys.exit("Usage: <script> <input_yaml> <output_json>")

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as rf:
    input_dict = yaml.safe_load(rf)

with open(output_file, "w") as wf:
    json.dump(input_dict, wf, indent=2)
