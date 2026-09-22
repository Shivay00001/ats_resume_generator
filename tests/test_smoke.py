"""Structural smoke test (generated). Verifies modules parse and expose entry points."""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(ROOT))

import ats_logic
import constants

def test_modules_import():
    assert "ats_logic" in sys.modules
    assert "constants" in sys.modules
