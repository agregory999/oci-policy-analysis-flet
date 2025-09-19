import os
import sys
sys.path.insert(0, os.path.abspath("../"))

project = "NavRail OCI Management App"
author = "Your Name"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # Google/NumPy docstrings
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
