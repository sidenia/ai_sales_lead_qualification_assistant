import pytest
import os
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault("OPENAI_API_KEY", "test_key_for_testing")