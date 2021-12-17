def get_cli_parser():
    """Run or add args to CLI parser

    :returns: Parser from argparse

    >>> parser = get_cli_parser()
    >>> parser.add_argument("-o", "--output", help="Working directory")
    >>> args, unknown = parser.parse_known_args()
    >>> print(args.output)
    """
    from trame.internal.app import get_app_instance

    _app = get_app_instance()
    return _app.cli_parser
