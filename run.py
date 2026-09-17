from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
LOADERS_DIR = PROJECT_ROOT / "src" / "loaders"
SRC_DIR = PROJECT_ROOT / "src"


def run_step(command: list[str], working_directory: Path) -> None:
    subprocess.run(command, cwd=working_directory, check=True)


run_step([sys.executable, "load_data.py"], LOADERS_DIR)
run_step([sys.executable, "clean_data.py"], LOADERS_DIR)
run_step([sys.executable, "model-evaluation.py"], SRC_DIR)
run_step([sys.executable, "-m", "streamlit", "run", "app.py","--server.headless", "true"], SRC_DIR)