"""Sphinx configuration."""
project = "Toolauth"
author = "Corey Rice"
copyright = "2022, Corey Rice"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
