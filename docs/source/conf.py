# docs/conf.py

import os
import sys
import django


# Add project root to path

sys.path.insert(0, os.path.abspath('/home/himanshu/Documents/project/ottermap_project'))
# print(sys.path.insert(0, os.path.abspath('../../ottermap_project')))


# Set the Django settings module so that autodoc can work properly
os.environ['DJANGO_SETTINGS_MODULE'] = 'ottermap_project.settings'
django.setup()

# -- Project information -----------------------------------------------------
project = 'ottermap project'
author = 'Himanshu Sharma'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # Support for Google/NumPy style docstrings
    'sphinx_autodoc_typehints',  # For type hints
    'sphinx.ext.intersphinx',
]

# Paths that contain templates, relative to this directory
templates_path = ['_templates']

# The master toctree document
master_doc = 'index'

# Include type hints
autodoc_typehints = 'description'

# HTML theme (you can switch to other themes like sphinx_rtd_theme)
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
