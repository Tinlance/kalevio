import sys
import os

# Add /app to path so 'backend' package is findable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app

__all__ = ["app"]
