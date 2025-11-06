"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

import nwm_region_mgr

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "nwm_region_mgr"
copyright = "2025, RTX"
author = "Yuqiong Liu, Matt Deshotel, Scott Lawson,"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinx.ext.doctest",
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "sphinxcontrib.rsvgconverter",
    "sphinx.ext.viewcode",  # adds [source] links
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# MyST
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
]

autosummary_generate = True
autosummary_generate_overwrite = True
templates_path = ["./_templates"]
exclude_patterns = ["production"]

master_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_css_files = ["custom.css"]

html_static_path = ["_static", "_images"]

html_js_files = [
    "form2yaml.js",
    "components/form-field.js",
    "https://unpkg.com/@popperjs/core@2",
    "https://unpkg.com/tippy.js@6",
]

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "navbar_start": ["navbar-logo", "navbar-version"],
    "navbar_center": ["navbar-nav"],
    "navbar_persistent": ["search-button"],
    "navbar_align": "content",
    "header_links_before_dropdown": 5,
}

html_sidebars = {
    "user_guide": [],
    "faq": [],
}


# Substitutions
version = str(nwm_region_mgr.__version__)
