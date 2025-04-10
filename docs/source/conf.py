# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'transcripts18xx'
copyright = '2025, Pascal Müller'
author = 'Pascal Müller'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # for Google/Numpy-style docstrings
    'sphinx_autodoc_typehints',
    'myst_parser',  # parse Markdown
    'sphinx_new_tab_link'  # open links in new tab
]

templates_path = ['_templates']
exclude_patterns = []

sys.path.insert(0, os.path.abspath('../../transcripts18xx'))

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
