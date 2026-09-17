from pathlib import Path
import subprocess
import sys
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent
LOADERS_DIR = PROJECT_ROOT / "src" / "loaders"
SRC_DIR = PROJECT_ROOT / "src"
DB_DIR = PROJECT_ROOT / "db"

def run_step(command: list[str], working_directory: Path) -> None:
    subprocess.run(command, cwd=working_directory, check=True)


# Check if database exist, and if not, executes load_data.py
file = Path(DB_DIR, "burnout_database.db")

clean_table_exists = None 
model_table_exists = None 

if not file.exists():
    run_step([sys.executable, "load_data.py"], LOADERS_DIR)

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
    run_step([sys.executable, "clean_data.py"], LOADERS_DIR)

if model_table_exists[0] != 1:
    run_step([sys.executable, "model-evaluation.py"], SRC_DIR)

run_step([sys.executable, "-m", "streamlit", "run", "app.py","--server.headless", "true"], SRC_DIR)