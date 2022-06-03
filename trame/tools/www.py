r"""
From a list of trame modules name, gather and generate the required static
content that needs to be served for a trame application to work.
"""
import argparse
import importlib
import shutil
from pathlib import Path


class StaticContentGenerator:
    def __init__(self):
        self.www = None
        self.serve = {}

    def enable_all(self):
        import pkgutil

        root = importlib.import_module("trame.modules")
        self.enable_modules(*[m.name for m in pkgutil.iter_modules(root.__path__)])

    def enable_modules(self, *names):
        for module_name in names:
            module = None
            try:
                module = importlib.import_module(f"trame.modules.{module_name}")
            except ModuleNotFoundError:
                try:
                    print("module_name:", module_name)
                    module = importlib.import_module(module_name)
                except ModuleNotFoundError:
                    print(f" - Error: Skipping module {module_name}")

            if module is None:
                print(f"Skipping module: {module_name}")
                continue

            if "serve" in module.__dict__:
                self.serve.update(module.serve)

            if "www" in module.__dict__:
                self.www = module.www

    def write(self, output_directory=None):
        if output_directory is None:
            output_directory = Path.cwd()

        if self.www:
            shutil.copytree(self.www, output_directory, dirs_exist_ok=True)

        for sub_path, src_dir in self.serve.items():
            dst_dir = Path(output_directory) / sub_path
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description="Static Web Client generator for trame applications"
    )

    parser.add_argument(
        "--output",
        help="Directory to fill with trame client code",
    )

    args, module_names = parser.parse_known_args()
    generator = StaticContentGenerator()
    if len(module_names):
        generator.enable_modules(*module_names)
    else:
        generator.enable_all()
    generator.write(args.output)


if __name__ == "__main__":
    main()
