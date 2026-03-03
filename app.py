"""Vercel/FastAPI root entrypoint.

This module keeps a root-level `app` object so Vercel can auto-detect and run
the FastAPI application without extra configuration.
"""

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shelfshift_demo.main import app  # noqa: E402

__all__ = ["app"]
