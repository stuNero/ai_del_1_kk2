import sqlite3
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.paths import DB_PATH, DATA_PATH

DB_PATH.parent.mkdir(exist_ok=True)


def ensure_dataset_exists(csv_path: Path = DATA_PATH) -> Path:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            "Download the CSV and place it in the project root data/ folder before running the app."
        )
    return csv_path


def load_from_db(db_file=DB_PATH, table_name="burnout_data"):
    connection = sqlite3.connect(db_file)
    df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
    connection.close()
    return df


def save_to_db(df, db_file=DB_PATH, table_name="burnout_data"):
    connection = sqlite3.connect(db_file)
    df.to_sql(table_name, connection, if_exists="replace", index=False)
    connection.close()
    print("db saved succesfully!")


if __name__ == "__main__":
    csv_path = ensure_dataset_exists()
    df = pd.read_csv(csv_path)
    print(f"csv loaded with {len(df):,} rows")

    save_to_db(df)
    print("db created")
