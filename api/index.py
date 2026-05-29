import sys
import traceback
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from app.main import app
except Exception as e:
    print("FAILED TO IMPORT FASTAPI APP")
    print("ERROR:", repr(e))
    traceback.print_exc()
    raise
