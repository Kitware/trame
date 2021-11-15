# How do I use CLI arguments?

trame uses Python's [`argparse`](https://docs.python.org/3/library/argparse.html) for CLI argument handling.

## Code

```python
from trame import get_cli_parser

parser = get_cli_parser()
parser.add_argument("-o", "--output", help="Working directory")
args = parser.parse_known_args()
print(args.output)
```

## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/cli.py)
- [VTK/Applications/ZarrContourViewer](https://github.com/Kitware/trame/blob/master/examples/VTK/Applications/ZarrContourViewer/app.py#L25-L28) uses a `--data` argument to load a file from disk.
