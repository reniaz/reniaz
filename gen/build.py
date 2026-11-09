"""Regenerate assets/*.svg.

    python3 gen/build.py            # every module
    python3 gen/build.py banner     # only the named modules
"""
import importlib
import sys

from common import ROOT, write

MODULES = ["banner", "terminal", "footer"]

for name in sys.argv[1:] or MODULES:
    for asset, build in importlib.import_module(name).ASSETS.items():
        print(write(asset, build).relative_to(ROOT))
