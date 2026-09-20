import os
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
class TestEnsureDatasetExists:
    def test_returns_same_path(self):
        result = ensure_dataset_exists(csv_path=DATA_PATH)
        assert result == DATA_PATH

    def test_raises_for_missing_file(self):
        missing = Path("does_not_exist.csv")
        with pytest.raises(FileNotFoundError):
            ensure_dataset_exists(csv_path=missing)

class TestLoadCsv:
    def test_returns_dataframe(self):
        df = load_csv(csv_path=DATA_PATH)
        assert type(df) == pd.DataFrame

    def test_raises_on_empty_dataframe(self,mocker):
        mocker.patch("src.loaders.load_data.pd.read_csv", return_value=pd.DataFrame())

        with pytest.raises(ValueError, match="Dataframe has no rows"):
            load_csv(Path("fake.csv"))

class TestLoadFromDb:
    @pytest.fixture
    def db_path(self, tmp_path):
        return tmp_path / "fake.db"
    
    @pytest.fixture
    def db_with_empty_table(self, db_path):
        conn = sqlite3.connect(db_path)
        conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER, name TEXT)")
        conn.commit()
        conn.close()
        return db_path
    
    @pytest.fixture
    def db_with_filled_table(self, db_path):
        conn = sqlite3.connect(db_path)
        conn.execute(f"CREATE TABLE {REG_RAW_TABLE_NAME} (id INTEGER, name TEXT)")
        conn.execute(f"INSERT INTO {REG_RAW_TABLE_NAME} VALUES (1, 'a')")
        conn.commit()
        conn.close()
        return db_path
    
    def test_returns_df(self, db_with_filled_table):
        df = load_from_db(db_path=db_with_filled_table)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_raises_when_no_tables_exist(self, db_path):
        sqlite3.connect(db_path).close()

        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_path)

    def test_raises_on_wrong_table_name(self, db_with_filled_table):
        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_with_filled_table, table_name="nonexistent_table_name")

    @pytest.mark.skipif(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        reason="root bypasses filesystem permission checks",
    )
    def test_raises_on_unwritable_path(self, tmp_path):
        restricted_dir = tmp_path / "restricted"
        restricted_dir.mkdir()
        restricted_dir.chmod(0o444)  # read-only, no write/execute

        db_path = restricted_dir / "fake.db"

        with pytest.raises(ConnectionError):
            load_from_db(db_path=db_path)

    def test_returns_empty_df_when_table_has_no_rows(self, db_with_empty_table):
        df = load_from_db(db_path=db_with_empty_table)
        assert df.empty