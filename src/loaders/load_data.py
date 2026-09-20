import sqlite3
from contextlib import closing
from pathlib import Path
import pandas as pd
from src.config.paths import DB_PATH, DATA_PATH
from src.config.constants import REG_RAW_TABLE_NAME


def ensure_dataset_exists(csv_path: Path = DATA_PATH) -> Path:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            "Download the CSV and place it in the project root data/ folder before running the app."
        )
    return csv_path


def load_from_db(db_path=DB_PATH, table_name=REG_RAW_TABLE_NAME) -> pd.DataFrame:
    try:
        with closing(sqlite3.connect(db_path)) as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    except Exception as e:
        raise ConnectionError(f"Error while loading from database: {e}" ) from e
    return df

def save_to_db(df:pd.DataFrame, db_path:Path=DB_PATH, table_name:str=REG_RAW_TABLE_NAME):
    db_path = Path(db_path)
    db_existed = db_path.exists()

    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(db_path)) as connection:
            df.to_sql(table_name, connection, if_exists="replace", index=False)
            connection.commit()
    except Exception as e:
        raise ConnectionError(f'Error while saving to database: "{e}"') from e

    if not db_existed:
        print(f"Database [{db_path.name}] created!")
    print(f"Table [{table_name}] in database [{db_path.name}] saved successfully!")

def load_csv(csv_path:Path=DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    print(f"csv loaded with {len(df):,} rows")
    return df

def run_pipeline(csv_path:Path=DATA_PATH, db_path:Path=DB_PATH):
    
    csv_path = ensure_dataset_exists(csv_path=csv_path)
    
    df = load_csv(csv_path)

    save_to_db(df, db_path=db_path)

if __name__ == "__main__":
    run_pipeline()