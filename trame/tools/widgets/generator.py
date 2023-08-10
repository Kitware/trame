import yaml
from pathlib import Path

PKG_INIT = """__path__ = __import__("pkgutil").extend_path(__path__, __name__)"""


def generate_trame_package(config_path, output_path):
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=True)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    create_base_structure(config, output)
    create_module(config, output)
    create_widget(config, output)


def create_base_structure(config, output):
    # Trame structure
    for package_name in ["modules", "widgets"]:
        root_dir = output / "trame" / package_name
        root_dir.mkdir(parents=True, exist_ok=True)
        (root_dir / "__init__.py").write_text(PKG_INIT)
    (output / "trame" / "__init__.py").write_text(PKG_INIT)

    # Package structure
    for name in config:
        root_dir = output / name
        root_dir.mkdir(parents=True, exist_ok=True)
        (root_dir / "__init__.py").write_text("")
        for sub_name in config[name]:
            sub_package = root_dir / sub_name
            sub_package.mkdir(parents=True, exist_ok=True)
            (sub_package / "__init__.py").write_text("")


def create_module(config, output):

    pass


def create_widget(config, output):

    pass
