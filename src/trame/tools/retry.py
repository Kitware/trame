r"""
From the directory containing the static content for a trame application to work,
generate another application specific HTML file.
"""

import argparse
import re
import sys
from pathlib import Path

RETRY_PATTERN = re.compile(r'data-launcher-retry=".+"')


def update_retry_file(input_file, output_file, retry_array):
    # Read in the file
    with open(input_file, "r") as f_in:
        content = f_in.read()
        patched_content = RETRY_PATTERN.sub(
            f'data-launcher-retry="{retry_array}"', content
        )
        with open(output_file, "w") as f_out:
            f_out.write(patched_content)


def main():
    parser = argparse.ArgumentParser(
        description="HTML app file generator for trame applications"
    )

    parser.add_argument(
        "--retry",
        default="[]",
        help="Retry array for launcher. Times are in ms.",
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

    update_retry_file(input_file, input_file, args.retry)


if __name__ == "__main__":
    main()
