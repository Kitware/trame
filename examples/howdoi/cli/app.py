from trame import get_cli_parser

parser = get_cli_parser()
parser.add_argument("-o", "--output", help="Our working directory")
args = parser.parse_args()
