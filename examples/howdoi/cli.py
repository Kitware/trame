from trame import get_cli_parser

if __name__ == "__main__":
    parser = get_cli_parser()
    parser.add_argument("-o", "--output", help="Working directory")
    args = parser.parse_args()
    print(args.output)
