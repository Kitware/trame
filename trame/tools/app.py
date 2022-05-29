r"""
From the directory containing the static content for a trame application to work,
generate another application specific HTML file.
"""
import argparse
import re
from pathlib import Path
import sys

APP_PATTERN = re.compile(r'data-app-name="\w+"')


def create_app_file(input_file, output_file, app_name):
    # Read in the file
    with open(input_file, "r") as f_in:
        content = f_in.read()
        patched_content = APP_PATTERN.sub(f'data-app-name="{app_name}"', content)
        with open(output_file, "w") as f_out:
            f_out.write(patched_content)


def main():
    parser = argparse.ArgumentParser(
        description="HTML app file generator for trame applications"
    )

    parser.add_argument(
        "--name",
        default="trame",
        help="Application name to encode inside HTML {name}.html",
    )

    parser.add_argument(
        "--input",
        help="Input file to use as template",
    )

    args, _ = parser.parse_known_args()

    # Handle input
    input_file = Path(args.input)
    if not input_file.exists():
        parser.print_help()
        sys.exit(0)

    if input_file.is_dir():
        input_file = input_file / "index.html"

    if not input_file.exists():
        parser.print_help()
        sys.exit(0)

    output_file = input_file.with_stem(args.name)
    create_app_file(input_file, output_file, args.name)


if __name__ == "__main__":
    main()
