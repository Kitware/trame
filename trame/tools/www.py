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
        self.client_type = "vue2"

    def enable_all(self):
        import pkgutil

        root = importlib.import_module("trame.modules")
        self.enable_modules(*[m.name for m in pkgutil.iter_modules(root.__path__)])

    def add_protocol_to_configure(self, *args, **kwargs):
        """Fake server"""
        pass

    def enable_module(self, module, **kwargs):
        load_remaining = False
        if "setup" in module.__dict__:
            try:
                module.setup(self)
                load_remaining = True
            except TypeError:
                pass  # Skip incompatible modules
        else:
            load_remaining = True

        if load_remaining:
            if "serve" in module.__dict__:
                self.serve.update(module.serve)

            if "www" in module.__dict__:
                self.www = module.www

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

            self.enable_module(module)

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

    parser.add_argument(
        "--client-type",
        default="vue2",
        help="Type of client to use [vue2, vue3]",
    )

    args, module_names = parser.parse_known_args()
    generator = StaticContentGenerator()
    generator.client_type = args.client_type
    if len(module_names):
        generator.enable_modules(*module_names)
    else:
        generator.enable_all()
    generator.write(args.output)


if __name__ == "__main__":
    main()
