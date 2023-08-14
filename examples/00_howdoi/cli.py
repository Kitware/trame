r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/howdoi/cli.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/abe8722c2299ccb9faebb72595665952e5479099

Installation requirements:
    pip install trame
"""

from trame.app import get_server

if __name__ == "__main__":
    server = get_server()
    parser = server.cli
    parser.add_argument("-o", "--output", help="Working directory")
    (args, _unknown) = parser.parse_known_args()
    print(args.output)
