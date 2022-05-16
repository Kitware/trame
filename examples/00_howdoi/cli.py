from trame.app import get_server

if __name__ == "__main__":
    server = get_server()
    parser = server.cli
    parser.add_argument("-o", "--output", help="Working directory")
    (args, _unknown) = parser.parse_known_args()
    print(args.output)
