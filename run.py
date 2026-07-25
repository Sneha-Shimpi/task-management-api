import runpy
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent / "task-manager-api"
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

runpy.run_path(str(project_dir / "run.py"), run_name="__main__")
