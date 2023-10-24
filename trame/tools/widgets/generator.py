import yaml
import shutil
from pathlib import Path
import aiohttp

PKG_INIT = """__path__ = __import__("pkgutil").extend_path(__path__, __name__)"""

EXT_BY_TYPES = {
    "scripts": ".js",
    "styles": ".css",
}


async def generate_trame_package(config_path, output_path):
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=True)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    await create_base_structure(Path(config_path).parent.absolute(), config, output)


async def create_base_structure(ref_path, config, output):
    trame_plugins = {}

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

            # Create files
            for module in config[name][sub_name]:
                if sub_name == "module":
                    module_root = sub_package / module
                    module_root.mkdir(parents=True, exist_ok=True)
                    module_root_init = module_root / "__init__.py"
                    module_conf_init = {}
                    for web_dir in config[name][sub_name][module]:
                        module_conf_init[web_dir] = await create_web_content(
                            ref_path,
                            (module_root / web_dir),
                            config[name][sub_name][module][web_dir],
                        )
                    # Register trame/modules/{webdir}
                    trame_plugins[
                        f"trame/modules/{module}.py"
                    ] = f"from {name}.module.{module} import *\n"
                    create_module_init(module_root_init, module_conf_init)

                elif sub_name == "widgets":
                    file_path = sub_package / f"{module}.py"
                    with file_path.open("w") as file:
                        file.write(
                            "from trame_client.widgets.core import AbstractElement, Template  # noqa\n"
                        )
                        file.write(f"from ..module import {module}\n")
                        file.write("\nclass HtmlElement(AbstractElement):")
                        file.write(
                            "\n    def __init__(self, _elem_name, children=None, **kwargs):"
                        )
                        file.write(
                            "\n        super().__init__(_elem_name, children, **kwargs)"
                        )
                        file.write("\n        if self.server:")
                        file.write(f"\n            self.server.enable_module({module})")
                        file.write("\n\n")

                        all_class_names = []
                        for class_name, class_info in config[name][sub_name][
                            module
                        ].items():
                            if class_name == "directives":
                                for entry in class_info:
                                    if isinstance(entry, list):
                                        file.write(
                                            f'\nAbstractElement.register_directive("{entry[0]}", "{entry[1]}")'
                                        )
                                    else:
                                        file.write(
                                            f'\nAbstractElement.register_directive("{entry}")'
                                        )
                                file.write("\n\n")
                            else:
                                all_class_names.append(class_name)
                                component = class_info.get("component")
                                properties = class_info.get("properties", [])
                                events = class_info.get("events", [])
                                file.write(f"\nclass {class_name}(HtmlElement):")
                                to_py_help(file, class_info)
                                file.write(
                                    "\n    def __init__(self, children=None, **kwargs):"
                                )
                                file.write(
                                    f'\n        super().__init__("{component}", children, **kwargs)'
                                )
                                file.write("\n        self._attr_names += [")
                                for item in properties:
                                    to_py_attr(file, item, 4 * 3)
                                file.write("\n        ]")
                                file.write("\n        self._event_names += [")
                                for item in events:
                                    to_py_attr(file, item, 4 * 3)
                                file.write("\n        ]")
                                file.write("\n\n")

                        file.write("\n__all__ = [")
                        for class_name in all_class_names:
                            file.write(f'\n{" " * 4}"{class_name}",')
                        file.write("\n]")
                        file.write("\n")

                    # Register trame/modules/{webdir}
                    trame_plugins[
                        f"trame/widgets/{module}.py"
                    ] = f"from {name}.widgets.{module} import *\n\ndef initialize(server):\n    from {name}.module import {module}\n\n    server.enable_module({module})\n"

    # Create trame package connectors
    for file, content in trame_plugins.items():
        (output / file).write_text(content)


def create_module_init(init_path, init_conf):
    for name in init_conf:
        m_conf = init_conf[name]
        m = init_path.with_name(f"{name}.py")
        widget_name = init_path.parent.name
        with m.open("w") as file:
            file.write("from pathlib import Path\n")
            file.write("\n")
            file.write(
                f'serve_path = str(Path(__file__).with_name("{name}").resolve())\n'
            )
            file.write(f'serve = {{"__trame_{widget_name}": serve_path }}\n')
            for group in ["scripts", "styles"]:
                if group in m_conf:
                    file.write(f"{group} = [\n")
                    for f_name in m_conf[group]:
                        file.write(f'    "__trame_{widget_name}/{f_name}",\n')
                    file.write("]\n")
            if "vue_use" in m_conf:
                file.write("vue_use = [\n")
                for name in m_conf["vue_use"]:
                    file.write(f'    "{name}",\n')
                file.write("]\n")

    with init_path.open("w") as file:
        file.write("def setup(server, **kargs):\n")
        file.write('    client_type = "vue2"\n')
        file.write('    if hasattr(server, "client_type"):\n')
        file.write("        client_type = server.client_type\n")
        if "vue2" in init_conf:
            file.write('    if client_type == "vue2":\n')
            file.write("        from . import vue2\n")
            file.write("        server.enable_module(vue2)\n")

        if "vue3" in init_conf:
            file.write(
                f'    {"elif" if "vue2" in init_conf else "if" } client_type == "vue3":\n'
            )
            file.write("        from . import vue3\n")
            file.write("        server.enable_module(vue3)\n")
        file.write("    else:\n")
        file.write("        raise TypeError(\n")
        file.write(
            '            f"Trying to initialize trame_vuetify with unknown client_type={client_type}"\n'
        )
        file.write("        )\n")


async def create_web_content(ref_path, base_directory, web_config):
    out_conf = {}
    base_directory.mkdir(parents=True, exist_ok=True)
    for key in web_config:
        if key in ["scripts", "styles"]:
            local_conf = []
            out_conf[key] = local_conf
            for item in web_config[key]:
                if isinstance(item, str):
                    if item.startswith("http"):
                        local_conf.append(
                            await handle_url(base_directory, item, EXT_BY_TYPES[key])
                        )
                    else:
                        local_conf.append(
                            handle_relative_path(ref_path, base_directory, item)
                        )
                else:
                    # in-line JS file
                    local_conf.append(handle_inline(base_directory, item))
        else:
            out_conf[key] = web_config[key]

    return out_conf


URL_FILE_COUNT = 0


async def handle_url(base_directory, entry, ext):
    global URL_FILE_COUNT
    URL_FILE_COUNT += 1
    file_name = f"{URL_FILE_COUNT}{ext}"
    if "?" in file_name:
        file_name = file_name.split("?")[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(entry) as resp:
            if resp.status == 200:
                content = await resp.read()
                with (base_directory / file_name).open(mode="wb") as f:
                    f.write(content)
    return file_name


def handle_relative_path(ref_path, base_directory, entry):
    src = ref_path / entry
    file_name = src.name
    dst = base_directory / file_name
    shutil.copyfile(src, dst)
    return file_name


def handle_inline(base_directory, entry):
    file_name = entry.get("name")
    content = entry.get("content")
    dst = base_directory / file_name
    with dst.open(mode="w") as f:
        f.write(content)
    return file_name


def to_py_attr(file, item, indent=4):
    entry = item.get("name")
    if isinstance(entry, (list, tuple)):
        py_name, js_name = entry
        file.write(f'\n{" "*indent}("{py_name}", "{js_name}"),')
    else:
        file.write(f'\n{" "*indent}"{entry}",')


def to_py_help(file, class_info):
    indent = 4
    file.write(f'\n{" "*indent}"""')
    main_help = class_info.get("help", "")
    properties = class_info.get("properties", [])
    events = class_info.get("properties", [])

    if len(main_help):
        file.write(f'\n{" "* indent}{main_help}')

    if len(properties):
        file.write(f'\n{" "* indent}Properties\n')
        for prop in properties:
            name = prop.get("name")
            help = prop.get("help", "").replace("\n", " ")
            if isinstance(name, (list, tuple)):
                name = name[0]
            file.write(f'\n{" "* indent}:param {name}: {help}')

    if len(events):
        file.write(f'\n\n{" "* indent}Events\n')
        for prop in events:
            name = prop.get("name")
            help = prop.get("help", "").replace("\n", " ")
            if isinstance(name, (list, tuple)):
                name = name[0]
            file.write(f'\n{" "* indent}:param {name}: {help}')
    file.write(f'\n{" "*indent}"""')
