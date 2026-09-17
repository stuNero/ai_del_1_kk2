import pandas as pd
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paths import DB_PATH

DB_PATH.parent.mkdir(exist_ok=True)


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
    df = pd.read_csv("../../data/mental_health_burnout_prediction_dataset.csv")
    print(f"csv loaded with {len(df):,} rows")

    save_to_db(df)
    print("db created")
