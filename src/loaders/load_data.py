import sqlite3
from pathlib import Path
import pandas as pd
from src.config.paths import DB_PATH, DATA_PATH
from src.config.constants import REG_RAW_TABLE_NAME

DB_PATH.parent.mkdir(exist_ok=True)


def ensure_dataset_exists(csv_path: Path = DATA_PATH) -> Path:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            "Download the CSV and place it in the project root data/ folder before running the app."
        )
    return csv_path


def load_from_db(db_file=DB_PATH, table_name=REG_RAW_TABLE_NAME):
    connection = sqlite3.connect(db_file)
    df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
    connection.close()
    return df

def save_to_db(df, db_file=DB_PATH, table_name=REG_RAW_TABLE_NAME):
    db_filename = str(db_file).split("\\")
    
    db_exist = True
    db_created_msg = f"Database [{db_filename[-1]}] created!"
    
    if not DB_PATH.exists():
        db_exist = False
        
    try:
        connection = sqlite3.connect(db_file)
        df.to_sql(table_name, connection, if_exists="replace", index=False)
        connection.close()
        
        if not db_exist:
            print(db_created_msg)
        
    except Exception as e:
        print("DB not created", e)
    finally:
        print(f"Table [{table_name}] in database [{db_filename[-1]}] saved succesfully!")

def load_csv(csv_path:Path=DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    print(f"csv loaded with {len(df):,} rows")
    return df

def run_pipeline():
    
    csv_path = ensure_dataset_exists()
    
    df = load_csv(csv_path)

    save_to_db(df)

if __name__ == "__main__":
    run_pipeline()