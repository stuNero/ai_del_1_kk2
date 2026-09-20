import pytest
import pandas as pd
import sqlite3
from src.config.constants import REG_RAW_TABLE_NAME

@pytest.fixture
def csv_path(tmp_path):
    return tmp_path / "fake.csv"

@pytest.fixture
def existing_csv_file_with_row(csv_path):
    # writes a csv file with 1 dummy row
    pd.DataFrame({"a": [1]}).to_csv(csv_path, index=False)
    return csv_path

@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "fake.db"

@pytest.fixture
def db_with_empty_table(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER, name TEXT)")
    conn.commit()
    conn.close()
    return db_path

@pytest.fixture
def db_with_filled_table(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER, name TEXT)")
    conn.execute(f"INSERT INTO {REG_RAW_TABLE_NAME} VALUES (1, 'a')")
    conn.commit()
    conn.close()
    return db_path