import re
import pytest
import pandas as pd
import sqlite3
from pathlib import Path

from src.loaders.load_data import (ensure_dataset_exists, 
                                   load_csv,
                                   load_from_db)
from src.config.paths import DATA_PATH
from src.config.constants import REG_RAW_TABLE_NAME

# test
def test_ensure_dataset_exists_returns_same_path():
    result = ensure_dataset_exists(csv_path=DATA_PATH)
    assert result == DATA_PATH

def test_ensure_dataset_exists_raises_for_missing_file():
    missing = Path("does_not_exist.csv")
    with pytest.raises(FileNotFoundError):
        ensure_dataset_exists(csv_path=missing)

def test_load_csv_returns_dataframe():
    df = load_csv(csv_path=DATA_PATH)
    assert type(df) == pd.DataFrame

def test_load_csv_raises_on_empty_dataframe(mocker):
    mocker.patch("src.loaders.load_data.pd.read_csv", return_value=pd.DataFrame())

    with pytest.raises(ValueError, match="Dataframe has no rows"):
        load_csv(Path("fake.csv"))

class TestLoadFromDb:
    def test_returns_df(self, tmp_path):
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(db_path)
        conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER, name TEXT)")
        conn.execute(f"INSERT INTO {REG_RAW_TABLE_NAME} VALUES (1, 'a')")
        conn.commit()
        conn.close()

        df = load_from_db(db_path=db_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_raises_when_no_tables_exist(self, tmp_path):
        db_path = tmp_path / "fake.db"
        sqlite3.connect(db_path).close()

        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_path)

    def test_raises_on_wrong_table_name(self, tmp_path):
        db_path = tmp_path / "fake.db"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE some_other_table (id INTEGER)")
        conn.commit()
        conn.close()

        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_path, table_name=REG_RAW_TABLE_NAME)

    def test_raises_on_unwritable_path(self):
        with pytest.raises(ConnectionError):
            load_from_db(db_path=Path("/nonexistent_dir_xyz/fake.db"))

    def test_returns_empty_df_when_table_has_no_rows(self, tmp_path):
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(db_path)
        conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER)")
        conn.commit()
        conn.close()

        df = load_from_db(db_path=db_path)
        assert df.empty