import sqlite3
import subprocess
import sys
from pathlib import Path

from src.config.paths import DATA_PATH

PROJECT_ROOT = Path(__file__).resolve().parent
LOADERS_DIR = PROJECT_ROOT / "src" / "data" / "loaders"
MODELS_DIR = PROJECT_ROOT / "src" / "models"
APP_PATH = PROJECT_ROOT / "src" / "app" / "app.py"
DB_DIR = PROJECT_ROOT / "db"


def run_step(command: list[str], working_directory: Path) -> None:
    subprocess.run(command, cwd=working_directory, check=True)


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at {DATA_PATH}. "
        "Download the CSV and place it in the project root data/ folder before running the app."
    )


# Check if database exist, and if not, executes load_data.py
file = Path(DB_DIR, "burnout_database.db")

clean_table_exists = None
model_table_exists = None

if not file.exists():
    run_step([sys.executable, str(LOADERS_DIR / "load_data.py")], PROJECT_ROOT)

# Check if 'burnout_data' & 'models' tables exist in DB
with sqlite3.connect(file) as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT EXISTS (
                SELECT 1 FROM sqlite_master
                WHERE type='table' AND name='burnout_data_clean'
            );
        """
    )
    clean_table_exists = cursor.fetchone()

    cursor.execute(
        """
            SELECT EXISTS (
                SELECT 1 FROM sqlite_master
                WHERE type='table' AND name='models'
            );
        """
    )
    model_table_exists = cursor.fetchone()

if clean_table_exists[0] != 1:
    run_step([sys.executable, str(LOADERS_DIR / "clean_data.py")], PROJECT_ROOT)

if model_table_exists[0] != 1:
    run_step([sys.executable, str(MODELS_DIR / "model_eval.py")], PROJECT_ROOT)

run_step([sys.executable, "-m", "streamlit", "run", str(APP_PATH), "--server.headless", "true"], PROJECT_ROOT)