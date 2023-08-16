import asyncio
import argparse
from .generator import generate_trame_package


async def main():
    parser = argparse.ArgumentParser(description="Trame component generator")

    parser.add_argument(
        "--config",
        default="trame",
        help="Path to config file that specify the widgets definition",
    )

    parser.add_argument(
        "--output",
        help="Directory where the generated files will be stored",
    )

    args, _ = parser.parse_known_args()

    await generate_trame_package(args.config, args.output)


if __name__ == "__main__":
    asyncio.run(main())
