import sys
from pathlib import Path

# makes `pytest` work from any directory (tests import `main` from this folder)
sys.path.insert(0, str(Path(__file__).parent))
