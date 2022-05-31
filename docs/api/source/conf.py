# Configuration file for the Sphinx documentation builder.

import inspect
import os
from pathlib import Path
import re

from sphinx.ext import apidoc

import trame

HTML_ELEMENT_REGEX = re.compile(r"^trame.*\.widgets\..*HtmlElement$")

# -- Project information -----------------------------------------------------

project = "Trame"
copyright = "2022, Kitware"
author = "Kitware"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = "bysource"
autodoc_mock_imports = [
    "IPython",
    "mpld3",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

# -- Modify environment variables --------------------------------------------

os.environ.update(
    {
        "TRAME_PARAVIEW_FAIL_SILENTLY": "True",
    }
)

# -- Hooks for sphinx events -------------------------------------------------


def run_apidoc(_):

    # Override the apidoc options with what we want
    apidoc.OPTIONS.clear()
    apidoc.OPTIONS.extend(
        [
            "members",
            "imported-members",
            "show-inheritance",
        ]
    )

    exclude_paths = [
        "env/utils.py",
    ]

    cur_path = str(Path(__file__).parent)
    templates_path = str(Path(cur_path) / "apidoc_templates")
    module_path = str(Path(trame.__file__).parent)

    # Make the exclude paths absolute
    exclude_paths = [str(Path(module_path) / x) for x in exclude_paths]

    argv = [
        "-f",
        "-T",
        "-e",
        "-M",
        "-o",
        cur_path,
        "-t",
        templates_path,
        module_path,
    ] + exclude_paths

    apidoc.main(argv)


def maybe_skip_member(app, what, name, obj, skip, options):
    # Implement logic here for whether to skip certain members
    return skip


def autodoc_process_bases(app, name, obj, options, bases):
    if len(bases) == 1 and inspect.isclass(bases[0]):
        cls = bases[0]
        name_with_module = f"{cls.__module__}.{cls.__qualname__}"
        if HTML_ELEMENT_REGEX.match(name_with_module):
            # It is an HtmlElement. Use it's base class instead.
            bases[0] = cls.__bases__[0]


def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.connect("autodoc-skip-member", maybe_skip_member)
    app.connect("autodoc-process-bases", autodoc_process_bases)
