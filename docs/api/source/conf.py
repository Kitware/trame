# Configuration file for the Sphinx documentation builder.

from pathlib import Path

from sphinx.ext import apidoc

import trame

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
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"


# -- Hooks for sphinx events -------------------------------------------------

def run_apidoc(_):

    # Override the apidoc options with what we want
    apidoc.OPTIONS.clear()
    apidoc.OPTIONS.extend([
        "members",
        "imported-members",
    ])

    ignore_paths = []

    cur_path = str(Path(__file__).parent)
    templates_path = str(Path(cur_path) / "apidoc_templates")
    module_path = str(Path(trame.__file__).parent)

    argv = [
        "-f",
        "-T",
        "-e",
        "-M",
        "-o", cur_path,
        "-t", templates_path,
        module_path,
    ] + ignore_paths

    apidoc.main(argv)


def maybe_skip_member(app, what, name, obj, skip, options):
    # Implement logic here for whether to skip certain members
    return skip


def setup(app):
    app.connect('builder-inited', run_apidoc)
    app.connect('autodoc-skip-member', maybe_skip_member)
