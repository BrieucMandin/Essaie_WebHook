import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../..'))  # Chemin vers la racine de ton projet Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Essaie_Webhook.settings'  # À adapter !
import django
django.setup()
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Essaie_WebHook'
copyright = '2025, Brieuc MANDIN'
author = 'Brieuc MANDIN'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Support des docstrings Google/Sphinx
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    ]

templates_path = ['_templates']
exclude_patterns = []

language = 'Fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme' #sphinx_rtd_theme
html_static_path = ['_static']
