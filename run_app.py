"""PyInstaller entry-point script.

Kept at the project root so PyInstaller has a simple, importable target that
sets up the package on sys.path and launches the app.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcautopilot.app import main

if __name__ == "__main__":
    sys.exit(main())
