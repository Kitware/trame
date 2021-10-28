# How do I use CLI arguments?

Trame uses python's `argparse` for CLI arguments. Examples are here: https://docs.python.org/3/library/argparse.html
```python
from trame import get_cli_parser

parser = get_cli_parser()
parser.add_argument("-o", "--output", help="Our working directory")
args = parser.parse_args()
```
