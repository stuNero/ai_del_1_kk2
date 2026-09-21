import sqlite3
import subprocess
import sys
from pathlib import Path

from src.config.paths import (
    APP_PATH,
    ENDPOINTS_MODULE,
    DATA_PATH,
    DB_PATH,
    PROJECT_ROOT,
)


def run_step(command: list[str], working_directory: Path) -> None:
    subprocess.run(command, cwd=working_directory, check=True)


def start_process(command: list[str], working_directory: Path) -> subprocess.Popen:
    return subprocess.Popen(command, cwd=working_directory)


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at {DATA_PATH}. "
        "Download the CSV and place it in the project root data/ folder before running the app."
    )


# Check if database exist, and if not, executes load_data.py
raw_table_exists = None
clean_table_exists = None
model_table_exists = None

if not DB_PATH.exists():
    run_step([sys.executable, "-m", "src.loaders.load_data"], PROJECT_ROOT)

# Check if 'burnout_data' & 'models' tables exist in DB
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    cursor.execute(
        """
            SELECT EXISTS (
                SELECT 1 FROM sqlite_master
                WHERE type='table' AND name='burnout_data'
            );
        """
    )
    raw_table_exists = cursor.fetchone()
    
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

if raw_table_exists[0] != 1:
    run_step([sys.executable, "-m", "src.loaders.load_data"], PROJECT_ROOT)

if clean_table_exists[0] != 1:
    run_step([sys.executable, "-m", "src.loaders.clean_data"], PROJECT_ROOT)

if model_table_exists[0] != 1:
    run_step([sys.executable, "-m", "src.models.reg_model_eval"], PROJECT_ROOT)

backend_process = start_process([sys.executable, "-m", "uvicorn", ENDPOINTS_MODULE, "--reload"], PROJECT_ROOT)

try:
    run_step([sys.executable, "-m", "streamlit", "run", str(APP_PATH), "--server.headless", "true", ], PROJECT_ROOT)
finally:
    backend_process.terminate()
    backend_process.wait()